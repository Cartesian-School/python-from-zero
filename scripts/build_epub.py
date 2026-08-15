#!/usr/bin/env python3
"""Собирает EPUB-издание книги из готовых HTML-страниц site/ (book/python-s-nulya.epub).

Извлекает содержимое <article> (для обычных страниц) или .chapter-hero+.section-list
(для страниц-открывашек глав) из уже собранных HTML-файлов, убирает элементы навигации
сайта (breadcrumb, section-nav, header, sidebar) и собирает главы в EPUB со сквозным
оглавлением, обложкой и общим стилем.
"""

import importlib
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from ebooklib import epub

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_structure import SITE_ORIGIN

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "book" / "epub" / "python-s-nulya.epub"

MANIFEST = json.loads((ROOT / "manifest" / "coverage_manifest.json").read_text(encoding="utf-8"))
PROJECTS = json.loads((ROOT / "manifest" / "projects_manifest.json").read_text(encoding="utf-8"))["projects"]

FRONT_MATTER = [
    ("front-matter/ob-avtore.html", "Об авторе"),
    ("front-matter/o-tehnicheskom-recenzente.html", "О техническом рецензенте"),
    ("front-matter/vvedenie.html", "Введение"),
]


def chapter_title(num: int) -> str:
    for ch in MANIFEST["chapters"]:
        if ch.get("number") == num:
            return ch["title"].replace("*", "")
    raise KeyError(num)


def chapter_pages(num: int) -> list[tuple[str, str]]:
    mod = importlib.import_module(f"build_chapter_{num:02d}")
    return [(f"chapters/glava-{num:02d}/{href}", title) for href, title in mod.PAGES]


def rewrite_links(tag) -> None:
    # Notebooks, project source files, and interactive /practice/ pages live
    # outside the EPUB/PDF package (on the live site or in the git repo), so a
    # package-relative link to them would be dead. Point these at the real,
    # stable production site instead of unwrapping to plain dead text — that
    # keeps the reference genuinely useful (readers can tap/click through to
    # the interactive practice runner, download the notebook, or view the
    # project source) rather than losing the reference entirely.
    for a in list(tag.find_all("a", href=True)):
        href = a["href"]
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        marker = next((m for m in ("/notebooks/", "/projects/", "/practice/", "/chapters/") if m in href), None)
        if marker is not None:
            # hrefs from theory pages are site-relative ("../../practice/03-01/...");
            # hrefs from project detail pages are root-relative ("/practice/03-01/...").
            # Normalize both to the same absolute production URL.
            site_relative_path = marker + href.split(marker, 1)[1]
            a["href"] = SITE_ORIGIN + site_relative_path
            continue
        if ".html" in href:
            a["href"] = href.replace(".html", ".xhtml")


def extract_article(html_text: str) -> str:
    soup = BeautifulSoup(html_text, "lxml")
    article = soup.find("article")
    for cls in ("breadcrumb", "section-kicker", "section-nav"):
        node = article.find("div", class_=cls)
        if node:
            node.decompose()
    # copy-to-clipboard buttons rely on onclick JS with no purpose in an e-reader —
    # drop them so pages don't need to be flagged as "scripted" content.
    for btn in article.find_all("button", class_="copy-btn"):
        btn.decompose()
    # practice_card()/local_required_card() append a small inline <script> that
    # reads localStorage to show live completion status — meaningless (and inert)
    # outside a browser, and would otherwise flag the package as containing script.
    for script in article.find_all("script"):
        script.decompose()
    rewrite_links(article)
    inner = "".join(str(c) for c in article.contents)
    return resolve_svg_css_vars(f"<html><body>{inner}</body></html>")


def extract_opener(html_text: str) -> str:
    soup = BeautifulSoup(html_text, "lxml")
    hero = soup.find("div", class_="chapter-hero")
    section_list = soup.find("div", class_="section-list")
    if section_list:
        for script in section_list.find_all("script"):
            script.decompose()
        rewrite_links(section_list)
    inner = (str(hero) if hero else "") + (str(section_list) if section_list else "")
    return resolve_svg_css_vars(f"<html><body>{inner}</body></html>")


# Mirrors theory.css's :root primitives — see that file for provenance. Needed
# because WeasyPrint's (and most e-reader engines') SVG renderer does not
# reliably resolve CSS custom properties referenced inside SVG presentation
# attributes (e.g. stop-color="var(--navy-950)") the way a browser does.
# project_illustration() in site_lib.py uses var(--token) throughout since
# it's shared with the live site, where real browsers resolve it fine.
SVG_COLOR_TOKENS = {
    "navy-950": "#08011C", "navy-900": "#0D0230", "navy-800": "#15104A",
    "violet-300": "#B9A0FC", "violet-400": "#8355FA", "violet-500": "#5B24F9",
    "blue-300": "#8FB7FE", "blue-500": "#185DFA", "blue-600": "#0C43F1",
    "white": "#FFFFFF", "offwhite": "#FAFAFC",
    "gray-100": "#F2F2F6", "gray-200": "#E4E4EC", "gray-400": "#B4B4C4",
    "gray-600": "#6B6B7D", "gray-800": "#2B2B3D",
    "amber-500": "#F59E0B", "red-500": "#EF4444", "green-500": "#22C55E",
}


# BeautifulSoup's "lxml" parser is libxml2's plain HTML parser, not an HTML5
# parser — it doesn't implement the HTML5 spec's "adjust SVG tag names" step
# that restores camelCase for foreign (SVG) content, so it silently lowercases
# every element/attribute name. Real browsers correct this automatically,
# which is why project_illustration() works fine live on the site; WeasyPrint
# (and EPUB e-readers) don't, so <linearGradient> becomes <lineargradient> —
# an unrecognized element, silently breaking the gradient fill reference —
# and viewBox/preserveAspectRatio become lowercase and stop applying.
_SVG_CASE_FIXES = {"lineargradient": "linearGradient", "viewbox": "viewBox", "preserveaspectratio": "preserveAspectRatio"}


def fix_svg_case(html_fragment: str) -> str:
    if "<svg" not in html_fragment:
        return html_fragment
    for wrong, right in _SVG_CASE_FIXES.items():
        html_fragment = re.sub(rf"<{wrong}(?=[ >])", f"<{right}", html_fragment)
        html_fragment = re.sub(rf"</{wrong}>", f"</{right}>", html_fragment)
        html_fragment = re.sub(rf"\b{wrong}=", f"{right}=", html_fragment)
    return html_fragment


def resolve_svg_css_vars(html_fragment: str) -> str:
    if "<svg" not in html_fragment:
        return html_fragment
    html_fragment = re.sub(
        r"var\(--([a-z0-9-]+)\)",
        lambda m: SVG_COLOR_TOKENS.get(m.group(1), m.group(0)),
        html_fragment,
    )
    return fix_svg_case(html_fragment)


def extract_project(html_text: str) -> str:
    """Extracts .project-hero + .project-detail-body from a real, already-built
    site/projects/<slug>/index.html — same single-source-of-truth approach as
    extract_opener(), reused rather than re-authored, so book and site can never
    drift on a project's real title/description/topics/source path."""
    soup = BeautifulSoup(html_text, "lxml")
    hero = soup.find("div", class_="project-hero")
    body = soup.find("div", class_="project-detail-body")
    if body:
        for cls in ("breadcrumb", "section-nav"):
            node = body.find(["div", "p"], class_=cls)
            if node:
                node.decompose()
        for script in body.find_all("script"):
            script.decompose()
        rewrite_links(body)
    inner = (str(hero) if hero else "") + (str(body) if body else "")
    return resolve_svg_css_vars(f"<html><body>{inner}</body></html>")


def ncx_id(file_name: str) -> str:
    """XML NCName-safe id for use in toc.ncx (no '/' or '.')."""
    return "nav_" + file_name.replace("/", "_").replace(".", "_")


def build_item(rel_html_path: str, title: str, *, is_opener: bool) -> epub.EpubHtml:
    src = SITE / rel_html_path
    html_text = src.read_text(encoding="utf-8")
    content = (extract_opener if is_opener else extract_article)(html_text)
    file_name = rel_html_path.replace(".html", ".xhtml")
    item = epub.EpubHtml(title=title, file_name=file_name, lang="ru")
    item.content = content
    if "<svg" in content:
        item.properties.append("svg")
    depth = rel_html_path.count("/")
    css_href = "../" * depth + "assets/css/theory.css"
    item.add_link(href=css_href, rel="stylesheet", type="text/css")
    return item


def build_project_item(entry: dict) -> epub.EpubHtml:
    slug = entry["slug"]
    rel_html_path = f"projects/{slug}/index.html"
    html_text = (SITE / rel_html_path).read_text(encoding="utf-8")
    content = extract_project(html_text)
    file_name = f"projects/{slug}.xhtml"
    item = epub.EpubHtml(title=entry["title"], file_name=file_name, lang="ru")
    item.content = content
    if "<svg" in content:
        item.properties.append("svg")
    item.add_link(href="../assets/css/theory.css", rel="stylesheet", type="text/css")
    item.add_link(href="../assets/css/project.css", rel="stylesheet", type="text/css")
    return item


def main() -> None:
    book = epub.EpubBook()
    book.set_identifier("cartesian-school-python-s-nulya-2026")
    book.set_title("Python с нуля: программирование, графика, приложения и игры")
    book.set_language("ru")
    book.add_author("Siergej Sobolewski")
    book.add_metadata("DC", "description", "Книга для начинающих: Python 3.14, графика на Turtle, приложения на Tkinter, игры на Pygame и веб-разработка на Flask.")
    book.add_metadata("DC", "publisher", "Cartesian School")

    css_bytes = (SITE / "assets" / "css" / "theory.css").read_bytes()
    css_item = epub.EpubItem(uid="theory_css", file_name="assets/css/theory.css", media_type="text/css", content=css_bytes)
    book.add_item(css_item)

    # A small curated stylesheet for the project appendix's markup, rather than
    # copying the full homepage.css: that file targets the homepage layout
    # (course journey, practice filters, hero, etc. — all irrelevant here) and,
    # as of the visual-polish pass, uses :has() — valid modern CSS for browsers,
    # but not supported by epubcheck's stricter CSS3 parser (fails as CSS-008)
    # nor guaranteed in e-reader rendering engines.
    project_css = """
.project-hero { width: 100%; aspect-ratio: 16 / 9; overflow: hidden; }
.project-hero svg { display: block; width: 100%; height: 100%; }
.project-meta-row { margin: 8px 0 16px; }
.project-topic { display: inline-block; font-size: 0.8em; font-weight: 600; background: var(--gray-100); color: var(--gray-600); padding: 2px 10px; border-radius: 999px; margin: 0 6px 6px 0; }
.reference-board { margin: 16px 0; }
.reference-card { display: block; padding: 10px 0; text-decoration: none; color: var(--color-text-primary); border-top: 1px solid var(--color-border-default); }
.reference-card .rt { font-weight: 600; }
.reference-card .rs { font-size: 0.85em; color: var(--color-text-muted); }
"""
    project_css_item = epub.EpubItem(uid="project_css", file_name="assets/css/project.css", media_type="text/css", content=project_css.encode("utf-8"))
    book.add_item(project_css_item)

    cover_path = ROOT / "design" / "exports" / "cover_concept_v1.png"
    book.set_cover("cover.png", cover_path.read_bytes())

    toc = []
    spine = ["nav"]

    fm_links = []
    for rel_path, title in FRONT_MATTER:
        item = build_item(rel_path, title, is_opener=False)
        book.add_item(item)
        spine.append(item)
        fm_links.append(epub.Link(item.file_name, title, ncx_id(item.file_name)))
    toc.append((epub.Section("Вводные материалы"), tuple(fm_links)))

    for num in range(1, 25):
        pages = chapter_pages(num)
        ch_links = []
        for i, (rel_path, title) in enumerate(pages):
            item = build_item(rel_path, title, is_opener=(i == 0))
            book.add_item(item)
            spine.append(item)
            ch_links.append(epub.Link(item.file_name, title, ncx_id(item.file_name)))
        toc.append((epub.Section(f"Глава {num}: {chapter_title(num).split(': ', 1)[-1]}"), tuple(ch_links)))

    project_links = []
    for entry in PROJECTS:
        item = build_project_item(entry)
        book.add_item(item)
        spine.append(item)
        project_links.append(epub.Link(item.file_name, entry["title"], ncx_id(item.file_name)))
    toc.append((epub.Section("Проекты"), tuple(project_links)))

    idx_item = build_item("predmetnyj-ukazatel.html", "Предметный указатель", is_opener=False)
    book.add_item(idx_item)
    spine.append(idx_item)
    toc.append(epub.Link(idx_item.file_name, "Предметный указатель", ncx_id(idx_item.file_name)))

    book.toc = tuple(toc)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = spine

    OUT.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(str(OUT), book)
    print(f"Записано: {OUT.relative_to(ROOT)} ({len(spine) - 1} страниц)")


if __name__ == "__main__":
    main()
