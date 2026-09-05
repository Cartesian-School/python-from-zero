#!/usr/bin/env python3
"""Собирает EPUB-издание книги из готовых HTML-страниц site/ (book/python-s-nulya.epub).

Извлекает содержимое <article> (для обычных страниц) или .chapter-hero+.section-list
(для страниц-открывашек глав) из уже собранных HTML-файлов, убирает элементы навигации
сайта (breadcrumb, section-nav, header, sidebar), а также любые узлы с классом
"web-presentation" (веб-only материал вроде расширенной hero-секции автора, не входящий
в принятую публикацию), и собирает главы в EPUB со сквозным оглавлением, обложкой и
общим стилем.
"""

import importlib
import json
import mimetypes
import posixpath
import re
import sys
from functools import lru_cache
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
from ebooklib import epub

sys.path.insert(0, str(Path(__file__).resolve().parent))

from chapter_metadata import chapter_title
from site_structure import SITE_ORIGIN

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "book" / "epub" / "python-s-nulya.epub"

PROJECTS = json.loads((ROOT / "manifest" / "projects_manifest.json").read_text(encoding="utf-8"))["projects"]

FRONT_MATTER = [
    ("front-matter/ob-avtore.html", "Об авторе"),
    ("front-matter/o-tehnicheskom-recenzente.html", "О техническом рецензенте"),
    ("front-matter/vvedenie.html", "Введение"),
]


def chapter_pages(num: int) -> list[tuple[str, str]]:
    mod = importlib.import_module(f"build_chapter_{num:02d}")
    # Chapter 23 additionally stores a stable curriculum sequence number as the
    # third tuple item. EPUB/PDF navigation consumes only URL and title.
    return [
        (f"chapters/glava-{num:02d}/{entry[0]}", entry[1])
        for entry in mod.PAGES
    ]


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
    # Web-only richer presentation (e.g. the front-matter author page's portrait
    # hero, domain grid, and project list) that would shift accepted PDF/EPUB
    # pagination if included — mirrors the project_illustration() /
    # project_publication_illustration() presentation/publication split, just
    # expressed as a class marker instead of a second function.
    for node in article.find_all(class_="web-presentation"):
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


class CaseSafeEpubHtml(epub.EpubHtml):
    """Preserve case-sensitive SVG names after EbookLib serializes XHTML.

    EbookLib parses ``EpubHtml.content`` with lxml's HTML parser inside
    :meth:`EpubHtml.get_content`.  That second HTML parse happens after our
    normalizer and lowercases SVG foreign-content names again.  XHTML readers
    treat ``viewBox`` and related SVG names as case-sensitive, so applying the
    repair only before assigning ``item.content`` is insufficient: diagrams
    fall back to SVG's 300x150 default viewport and are visibly clipped.

    Repair the final serialized bytes returned to EbookLib's ZIP writer.  This
    keeps EbookLib's template, metadata, stylesheet links, and spine handling
    while ensuring the XHTML stored in the EPUB has valid SVG names.
    """

    def get_content(self, default=None) -> bytes:
        serialized = super().get_content(default)
        if not serialized:
            return serialized
        return fix_svg_case(serialized.decode("utf-8")).encode("utf-8")


def extract_project(html_text: str) -> str:
    """Extract the stable project fragment used by the accepted publication.

    Project pages embed ``.project-hero`` and ``.project-detail-body`` inside an
    inert publication-source template.  The visible web layout may evolve, while
    this compatibility fragment keeps the PDF/EPUB representation stable.  Its
    factual title, description, topics, and source path still originate from the
    canonical project manifest rather than an independently authored book copy.
    """
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


@lru_cache(maxsize=1)
def included_html_paths() -> frozenset[str]:
    paths = {rel_path for rel_path, _title in FRONT_MATTER}
    for number in range(1, 25):
        paths.update(rel_path for rel_path, _title in chapter_pages(number))
    paths.update(f"projects/{entry['slug']}/index.html" for entry in PROJECTS)
    paths.add("predmetnyj-ukazatel.html")
    return frozenset(paths)


def _literalize_pseudotags(soup: BeautifulSoup) -> None:
    """Repair traceback/URL literals that permissive HTML parsed as elements."""
    for code in soup.find_all(["code", "pre"]):
        for tag in list(code.find_all("module")):
            tag.insert_before(NavigableString("<module>"))
            tag.unwrap()
        for tag in list(code.find_all("class")):
            type_name = next(iter(tag.attrs), "object")
            tag.insert_before(NavigableString(f"<class {type_name}>"))
            tag.unwrap()
        for tag in list(code.find_all("svg")):
            tag.replace_with(NavigableString(str(tag)))
    for tag in list(soup.find_all("id")):
        tag.replace_with(NavigableString("<id>"))


def _namespace_and_uniquify_svg(soup: BeautifulSoup) -> None:
    for svg_index, svg in enumerate(soup.find_all("svg"), start=1):
        svg["xmlns"] = "http://www.w3.org/2000/svg"
        replacements: dict[str, str] = {}
        for node in svg.find_all(id=True):
            old_id = node["id"]
            new_id = f"epub-{svg_index}-{old_id}"
            node["id"] = new_id
            replacements[old_id] = new_id
        if not replacements:
            continue
        for node in svg.find_all(True):
            for attribute, value in list(node.attrs.items()):
                if not isinstance(value, str):
                    continue
                for old_id, new_id in replacements.items():
                    value = value.replace(f"url(#{old_id})", f"url(#{new_id})")
                    if value == f"#{old_id}":
                        value = f"#{new_id}"
                node[attribute] = value
    for math in soup.find_all("math"):
        math["xmlns"] = "http://www.w3.org/1998/Math/MathML"


def normalize_epub_content(
    content: str,
    rel_html_path: str,
    output_xhtml_path: str | None = None,
) -> str:
    """Convert permissive site HTML to deterministic, self-contained XHTML."""
    soup = BeautifulSoup(content, "lxml")
    _literalize_pseudotags(soup)
    for caption in soup.find_all("figcaption"):
        if caption.find_parent("figure") is None:
            caption.name = "p"
            caption["class"] = [*caption.get("class", []), "figcaption"]
    _namespace_and_uniquify_svg(soup)

    current_xhtml = output_xhtml_path or (
        rel_html_path.removesuffix(".html") + ".xhtml"
    )
    depth = current_xhtml.count("/")
    asset_prefix = "../" * depth
    for node in soup.find_all(True):
        for attribute in ("src", "href", "xlink:href"):
            value = node.get(attribute)
            if isinstance(value, str) and value.startswith("/assets/"):
                node[attribute] = asset_prefix + value.lstrip("/")

    included = included_html_paths()
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        if href.startswith(("http://", "https://", "mailto:", "#")):
            continue
        href_without_fragment, separator, fragment = href.partition("#")
        if not href_without_fragment.endswith((".html", ".xhtml")):
            continue
        resolved = posixpath.normpath(
            posixpath.join(posixpath.dirname(rel_html_path), href_without_fragment)
        ).lstrip("/")
        resolved_html = re.sub(r"\.xhtml$", ".html", resolved)
        if resolved_html in included:
            target_xhtml = resolved_html.removesuffix(".html") + ".xhtml"
            relative = posixpath.relpath(
                target_xhtml, start=posixpath.dirname(current_xhtml) or "."
            )
            anchor["href"] = relative + (separator + fragment if separator else "")
        else:
            anchor["href"] = (
                f"{SITE_ORIGIN}/{resolved_html}" + (separator + fragment if separator else "")
            )

    body = soup.find("body")
    normalized = "".join(str(child) for child in body.contents) if body else str(soup)
    return resolve_svg_css_vars(f"<html><body>{normalized}</body></html>")


def build_item(rel_html_path: str, title: str, *, is_opener: bool) -> epub.EpubHtml:
    src = SITE / rel_html_path
    html_text = src.read_text(encoding="utf-8")
    content = normalize_epub_content(
        (extract_opener if is_opener else extract_article)(html_text),
        rel_html_path,
    )
    file_name = rel_html_path.replace(".html", ".xhtml")
    item = CaseSafeEpubHtml(title=title, file_name=file_name, lang="ru")
    item.content = content
    if re.search(r"<svg\b", content):
        item.properties.append("svg")
    if re.search(r"<math\b", content):
        item.properties.append("mathml")
    depth = rel_html_path.count("/")
    css_href = "../" * depth + "assets/css/theory.css"
    item.add_link(href=css_href, rel="stylesheet", type="text/css")
    return item


def build_project_item(entry: dict) -> epub.EpubHtml:
    slug = entry["slug"]
    rel_html_path = f"projects/{slug}/index.html"
    html_text = (SITE / rel_html_path).read_text(encoding="utf-8")
    file_name = f"projects/{slug}.xhtml"
    content = normalize_epub_content(
        extract_project(html_text), rel_html_path, file_name
    )
    item = CaseSafeEpubHtml(title=entry["title"], file_name=file_name, lang="ru")
    item.content = content
    if re.search(r"<svg\b", content):
        item.properties.append("svg")
    if re.search(r"<math\b", content):
        item.properties.append("mathml")
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

    for asset_root in (SITE / "assets" / "img", SITE / "assets" / "brand", SITE / "assets" / "icons"):
        for asset_path in sorted(path for path in asset_root.rglob("*") if path.is_file()):
            relative = asset_path.relative_to(SITE).as_posix()
            media_type = mimetypes.guess_type(asset_path.name)[0]
            if asset_path.suffix.lower() == ".svg":
                media_type = "image/svg+xml"
            if not media_type:
                raise RuntimeError(f"cannot determine EPUB media type: {asset_path}")
            book.add_item(
                epub.EpubItem(
                    uid=ncx_id(relative),
                    file_name=relative,
                    media_type=media_type,
                    content=asset_path.read_bytes(),
                )
            )

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
        toc.append((epub.Section(f"Глава {num}: {chapter_title(num)}"), tuple(ch_links)))

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
