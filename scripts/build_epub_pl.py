#!/usr/bin/env python3
"""Собирает EPUB-издание книги из уже готовых PL HTML-страниц site/pl/
(book/epub/python-od-zera-pl.epub).

PL pages are machine-translated derivatives of the RU pages written by
scripts/build_polish_course.py — same filenames, same page order, just
under site/pl/chapters/rozdzial-NN/ instead of site/chapters/glava-NN/ (and
correspondingly for front matter/projects). There is no PL equivalent of
each RU chapter's build_chapter_NN.py PAGES list, so this reuses build_epub's
own RU chapter_pages()/FRONT_MATTER/PROJECTS purely for page identity (slugs,
filenames, ordering — all locale-neutral) and rewrites the site path prefix;
PL titles are read back from the already-translated PL HTML itself (each
page's own <h1>), never re-derived independently, so the EPUB nav/TOC can
never drift from what a PL reader actually sees on the page.

Content extraction, link rewriting, SVG repair, and EPUB packaging reuse
scripts/book_shared.py verbatim (locale-agnostic) — see build_epub.py (the
RU counterpart) for the shared mechanics this mirrors.
"""

import mimetypes
import re
import sys
from functools import lru_cache
from pathlib import Path

from bs4 import BeautifulSoup
from ebooklib import epub

sys.path.insert(0, str(Path(__file__).resolve().parent))

import book_shared as bs
import build_epub as be
from build_polish_course import FRONT_MATTER_NAMES
from site_structure import SITE_ORIGIN

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site" / "pl"
OUT = ROOT / "book" / "epub" / "python-od-zera-pl.epub"
LANG = "pl"

EPUB_BUILD_MTIME = be.EPUB_BUILD_MTIME

BOOK_TITLE = "Python od zera"
BOOK_SUBTITLE = "programowanie, grafika, aplikacje i gry"
BOOK_AUTHOR = "Siergej Sobolewski"

RIGHTS_HOLDER = "Siergej Sobolewski / Cartesian School"
CONTENT_LICENSE_NAME = (
    "Creative Commons Uznanie autorstwa-Użycie niekomercyjne-Na tych samych "
    "warunkach 4.0 Międzynarodowe (CC BY-NC-SA 4.0)"
)
CONTENT_LICENSE_URL = "https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pl"

RIGHTS_NOTICE_PLAIN = (
    f"© {RIGHTS_HOLDER}. "
    f"Tekst książki i oryginalne materiały dydaktyczne: {CONTENT_LICENSE_NAME}. "
    f"{CONTENT_LICENSE_URL} "
    "Kod źródłowy — w tym fragmenty kodu i listingi w tekście książki, a nie "
    "tylko osobne projekty i skrypty — o ile nie wskazano inaczej, jest "
    "udostępniany na warunkach licencji MIT."
)

RIGHTS_NOTICE_PARAGRAPHS_HTML = (
    f"<p>© {RIGHTS_HOLDER}</p>"
    "<p>Tekst książki i oryginalne materiały dydaktyczne: "
    f'<a href="{CONTENT_LICENSE_URL}">{CONTENT_LICENSE_NAME}</a>.</p>'
    f"<p>{CONTENT_LICENSE_URL}</p>"
    "<p>Kod źródłowy — w tym fragmenty kodu i listingi w tekście książki, a "
    "nie tylko osobne projekty i skrypty — o ile nie wskazano inaczej, jest "
    "udostępniany na warunkach licencji MIT.</p>"
)


def _pl_path(ru_rel_path: str) -> str:
    """chapters/glava-NN/x.html -> pl/chapters/rozdzial-NN/x.html; a bare
    front-matter/x.html gets its PL-named counterpart via FRONT_MATTER_NAMES."""
    if ru_rel_path.startswith("chapters/glava-"):
        rest = ru_rel_path[len("chapters/glava-"):]
        num, _, tail = rest.partition("/")
        return f"pl/chapters/rozdzial-{num}/{tail}"
    if ru_rel_path.startswith("front-matter/"):
        fname = ru_rel_path.split("/", 1)[1]
        return f"pl/front-matter/{FRONT_MATTER_NAMES[fname]}"
    raise ValueError(f"no PL path mapping for {ru_rel_path!r}")


def _extract_title(html_text: str) -> str:
    soup = BeautifulSoup(html_text, "lxml")
    hero_h1 = soup.select_one(".chapter-hero h1")
    if hero_h1:
        return hero_h1.get_text(strip=True)
    article_h1 = soup.select_one("article h1")
    if article_h1:
        return article_h1.get_text(strip=True)
    any_h1 = soup.find("h1")
    if any_h1:
        return any_h1.get_text(strip=True)
    raise RuntimeError("no <h1> found to derive a PL page title")


FRONT_MATTER: list[tuple[str, str]] = []
for ru_rel_path, _ru_title in be.FRONT_MATTER:
    pl_rel_path = _pl_path(ru_rel_path)[len("pl/"):]
    pl_title = _extract_title((SITE / pl_rel_path).read_text(encoding="utf-8"))
    FRONT_MATTER.append((pl_rel_path, pl_title))


@lru_cache(maxsize=None)
def chapter_pages(num: int) -> list[tuple[str, str]]:
    ru_pages = be.chapter_pages(num)
    pages: list[tuple[str, str]] = []
    for ru_rel_path, _ru_title in ru_pages:
        pl_rel_path = _pl_path(ru_rel_path)[len("pl/"):]
        pl_title = _extract_title((SITE / pl_rel_path).read_text(encoding="utf-8"))
        pages.append((pl_rel_path, pl_title))
    return pages


def chapter_title(num: int) -> str:
    return chapter_pages(num)[0][1]


PROJECTS: list[dict] = []
for entry in be.PROJECTS:
    slug = entry["slug"]
    rel_path = f"projects/{slug}/index.html"
    pl_title = _extract_title((SITE / rel_path).read_text(encoding="utf-8"))
    PROJECTS.append({**entry, "title": pl_title})


def extract_article(html_text: str) -> str:
    return bs.extract_article(html_text, site_origin=SITE_ORIGIN)


def extract_opener(html_text: str) -> str:
    return bs.extract_opener(html_text, site_origin=SITE_ORIGIN)


def extract_project(html_text: str) -> str:
    return bs.extract_project(html_text, site_origin=SITE_ORIGIN)


CaseSafeEpubHtml = bs.CaseSafeEpubHtml
ncx_id = bs.ncx_id
strip_has_selector_rules = bs.strip_has_selector_rules
normalize_epub_zip_determinism = bs.normalize_epub_zip_determinism


@lru_cache(maxsize=1)
def included_html_paths() -> frozenset[str]:
    paths = {rel_path for rel_path, _title in FRONT_MATTER}
    for number in range(1, 25):
        paths.update(rel_path for rel_path, _title in chapter_pages(number))
    paths.update(f"projects/{entry['slug']}/index.html" for entry in PROJECTS)
    paths.add("indeks-rzeczowy.html")
    return frozenset(paths)


def normalize_epub_content(
    content: str,
    rel_html_path: str,
    output_xhtml_path: str | None = None,
) -> str:
    return bs.normalize_epub_content(
        content,
        rel_html_path,
        included_html_paths(),
        site_origin=SITE_ORIGIN,
        output_xhtml_path=output_xhtml_path,
    )


def build_copyright_item() -> epub.EpubHtml:
    content = normalize_epub_content(
        "<html><body>"
        '<div class="copyright-page-epub">'
        f"<h1>{BOOK_TITLE}: {BOOK_SUBTITLE}</h1>"
        f"<p>{BOOK_AUTHOR} — Cartesian School</p>"
        f"{RIGHTS_NOTICE_PARAGRAPHS_HTML}"
        "</div></body></html>",
        "copyright.html",
        "copyright.xhtml",
    )
    item = CaseSafeEpubHtml(title="Informacje prawne", file_name="copyright.xhtml", lang=LANG)
    item.content = content
    item.add_link(href="assets/css/theory.css", rel="stylesheet", type="text/css")
    return item


def build_item(rel_html_path: str, title: str, *, is_opener: bool) -> epub.EpubHtml:
    src = SITE / rel_html_path
    html_text = src.read_text(encoding="utf-8")
    content = normalize_epub_content(
        (extract_opener if is_opener else extract_article)(html_text),
        rel_html_path,
    )
    file_name = rel_html_path.replace(".html", ".xhtml")
    item = CaseSafeEpubHtml(title=title, file_name=file_name, lang=LANG)
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
    item = CaseSafeEpubHtml(title=entry["title"], file_name=file_name, lang=LANG)
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
    book.set_identifier("cartesian-school-python-od-zera-2026")
    book.set_title(f"{BOOK_TITLE}: {BOOK_SUBTITLE}")
    book.set_language(LANG)
    book.add_author(BOOK_AUTHOR)
    book.add_metadata(
        "DC", "description",
        "Książka dla początkujących: Python 3.14, grafika w Turtle, aplikacje "
        "w Tkinter, gry w Pygame i tworzenie stron internetowych we Flasku.",
    )
    book.add_metadata("DC", "publisher", "Cartesian School")
    book.add_metadata("DC", "rights", RIGHTS_NOTICE_PLAIN)

    css_text = strip_has_selector_rules((be.SITE / "assets" / "css" / "theory.css").read_text(encoding="utf-8"))
    css_bytes = css_text.encode("utf-8")
    css_item = epub.EpubItem(uid="theory_css", file_name="assets/css/theory.css", media_type="text/css", content=css_bytes)
    book.add_item(css_item)

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

    # Assets are shared verbatim between locales (site/assets/, not
    # site/pl/assets/) — build_polish_course.py never duplicates them.
    for asset_root in (be.SITE / "assets" / "img", be.SITE / "assets" / "brand", be.SITE / "assets" / "icons"):
        for asset_path in sorted(path for path in asset_root.rglob("*") if path.is_file()):
            relative = asset_path.relative_to(be.SITE).as_posix()
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

    cover_path = ROOT / "design" / "exports" / "cover_concept_v1_pl.png"
    book.set_cover("cover.png", cover_path.read_bytes())

    toc = []
    spine = ["nav"]

    copyright_item = build_copyright_item()
    book.add_item(copyright_item)
    spine.append(copyright_item)
    toc.append(epub.Link(copyright_item.file_name, "Informacje prawne", ncx_id(copyright_item.file_name)))

    fm_links = []
    for rel_path, title in FRONT_MATTER:
        item = build_item(rel_path, title, is_opener=False)
        book.add_item(item)
        spine.append(item)
        fm_links.append(epub.Link(item.file_name, title, ncx_id(item.file_name)))
    toc.append((epub.Section("Materiały wprowadzające"), tuple(fm_links)))

    for num in range(1, 25):
        pages = chapter_pages(num)
        ch_links = []
        for i, (rel_path, title) in enumerate(pages):
            item = build_item(rel_path, title, is_opener=(i == 0))
            book.add_item(item)
            spine.append(item)
            ch_links.append(epub.Link(item.file_name, title, ncx_id(item.file_name)))
        toc.append((epub.Section(f"Rozdział {num}: {chapter_title(num)}"), tuple(ch_links)))

    project_links = []
    for entry in PROJECTS:
        item = build_project_item(entry)
        book.add_item(item)
        spine.append(item)
        project_links.append(epub.Link(item.file_name, entry["title"], ncx_id(item.file_name)))
    toc.append((epub.Section("Projekty"), tuple(project_links)))

    idx_item = build_item("indeks-rzeczowy.html", "Indeks rzeczowy", is_opener=False)
    book.add_item(idx_item)
    spine.append(idx_item)
    toc.append(epub.Link(idx_item.file_name, "Indeks rzeczowy", ncx_id(idx_item.file_name)))

    book.toc = tuple(toc)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = spine

    OUT.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(str(OUT), book, {"mtime": EPUB_BUILD_MTIME})
    normalize_epub_zip_determinism(OUT, EPUB_BUILD_MTIME)
    print(f"Zapisano: {OUT.relative_to(ROOT)} ({len(spine) - 1} stron)")


if __name__ == "__main__":
    main()
