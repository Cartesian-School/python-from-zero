#!/usr/bin/env python3
"""Собирает EPUB-издание книги из готовых HTML-страниц site/ (book/python-s-nulya.epub).

Извлекает содержимое <article> (для обычных страниц) или .chapter-hero+.section-list
(для страниц-открывашек глав) из уже собранных HTML-файлов, убирает элементы навигации
сайта (breadcrumb, section-nav, header, sidebar), а также любые узлы с классом
"web-presentation" (веб-only материал вроде расширенной hero-секции автора, не входящий
в принятую публикацию), и собирает главы в EPUB со сквозным оглавлением, обложкой и
общим стилем.
"""

import datetime
import importlib
import json
import mimetypes
import os
import re
import sys
from functools import lru_cache
from pathlib import Path

from ebooklib import epub

sys.path.insert(0, str(Path(__file__).resolve().parent))

import book_shared as bs
from chapter_metadata import chapter_title
from site_structure import SITE_ORIGIN

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "book" / "epub" / "python-s-nulya-ru.epub"
LANG = "ru"

# Reproducible-builds timestamp (see build_pdf.py's own SOURCE_DATE_EPOCH,
# which this mirrors) — a fixed instant, never datetime.now()/time.time(),
# so two builds from identical source produce a byte-identical EPUB. ZIP's
# DOS-based date_time field cannot represent anything before 1980-01-01
# (raises ValueError), so unlike build_pdf.py's epoch-0 constant this floors
# at the earliest valid ZIP timestamp instead of the Unix epoch.
_ZIP_EPOCH_FLOOR = 315532800  # 1980-01-01T00:00:00Z as a Unix timestamp
_SOURCE_DATE_EPOCH_ENV = os.environ.get("SOURCE_DATE_EPOCH")
EPUB_BUILD_MTIME = datetime.datetime.fromtimestamp(
    max(int(_SOURCE_DATE_EPOCH_ENV), _ZIP_EPOCH_FLOOR) if _SOURCE_DATE_EPOCH_ENV else _ZIP_EPOCH_FLOOR,
    tz=datetime.UTC,
).replace(tzinfo=None)

PROJECTS = json.loads((ROOT / "manifest" / "projects_manifest.json").read_text(encoding="utf-8"))["projects"]

BOOK_TITLE = "Python с нуля"
BOOK_SUBTITLE = "программирование, графика, приложения и игры"
BOOK_AUTHOR = "Siergej Sobolewski"

# Shared by build_pdf.py (via `import build_epub as be`) so the PDF copyright
# page and this EPUB's own copyright page/DC:rights metadata state the exact
# same licensing model — never two independently-typed copies that could
# drift. Prose/explanations/diagrams/assignments are CC BY-NC-SA 4.0. ALL
# code is MIT (LICENSE-CODE.md) unless a file/directory states otherwise —
# this explicitly includes inline code snippets/listings printed inside the
# book text itself, not just standalone scripts/projects: code never becomes
# CC-licensed merely by being shown inside a CC-licensed page. The two are
# never merged into one blanket grant. See /front-matter/litsenziya.html
# (scripts/build_license_page.py) for the full human-readable explanation
# this notice summarizes.
RIGHTS_HOLDER = "Siergej Sobolewski / Cartesian School"
CONTENT_LICENSE_NAME = (
    "Creative Commons Attribution-NonCommercial-ShareAlike "
    "4.0 International (CC BY-NC-SA 4.0)"
)
CONTENT_LICENSE_URL = "https://creativecommons.org/licenses/by-nc-sa/4.0/"

RIGHTS_NOTICE_PLAIN = (
    f"© {RIGHTS_HOLDER}. "
    f"Текст книги и оригинальные учебные материалы: {CONTENT_LICENSE_NAME}. "
    f"{CONTENT_LICENSE_URL} "
    "Программный код — включая фрагменты кода и листинги внутри текста "
    "книги, а не только отдельные проекты и скрипты, — если прямо не "
    "указано иное, распространяется на условиях MIT License."
)

RIGHTS_NOTICE_PARAGRAPHS_HTML = (
    f"<p>© {RIGHTS_HOLDER}</p>"
    "<p>Текст книги и оригинальные учебные материалы: "
    f'<a href="{CONTENT_LICENSE_URL}">{CONTENT_LICENSE_NAME}</a>.</p>'
    f"<p>{CONTENT_LICENSE_URL}</p>"
    "<p>Программный код — включая фрагменты кода и листинги внутри текста "
    "книги, а не только отдельные проекты и скрипты, — если прямо не "
    "указано иное, распространяется на условиях MIT License.</p>"
)

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


def build_copyright_item() -> epub.EpubHtml:
    """The EPUB's own copyright/rights page — a root-level spine item, read
    first, mirroring build_pdf.py's copyright page (both draw on the exact
    same RIGHTS_NOTICE_PARAGRAPHS_HTML constant above, so the two publication
    formats can never independently drift on the licensing model)."""
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
    item = CaseSafeEpubHtml(title="Правовая информация", file_name="copyright.xhtml", lang=LANG)
    item.content = content
    item.add_link(href="assets/css/theory.css", rel="stylesheet", type="text/css")
    return item


@lru_cache(maxsize=1)
def included_html_paths() -> frozenset[str]:
    paths = {rel_path for rel_path, _title in FRONT_MATTER}
    for number in range(1, 25):
        paths.update(rel_path for rel_path, _title in chapter_pages(number))
    paths.update(f"projects/{entry['slug']}/index.html" for entry in PROJECTS)
    paths.add("predmetnyj-ukazatel.html")
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
    book.set_identifier("cartesian-school-python-s-nulya-2026")
    book.set_title(f"{BOOK_TITLE}: {BOOK_SUBTITLE}")
    book.set_language(LANG)
    book.add_author(BOOK_AUTHOR)
    book.add_metadata("DC", "description", "Книга для начинающих: Python 3.14, графика на Turtle, приложения на Tkinter, игры на Pygame и веб-разработка на Flask.")
    book.add_metadata("DC", "publisher", "Cartesian School")
    book.add_metadata("DC", "rights", RIGHTS_NOTICE_PLAIN)

    css_text = strip_has_selector_rules((SITE / "assets" / "css" / "theory.css").read_text(encoding="utf-8"))
    css_bytes = css_text.encode("utf-8")
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

    copyright_item = build_copyright_item()
    book.add_item(copyright_item)
    spine.append(copyright_item)
    toc.append(epub.Link(copyright_item.file_name, "Правовая информация", ncx_id(copyright_item.file_name)))

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
    epub.write_epub(str(OUT), book, {"mtime": EPUB_BUILD_MTIME})
    normalize_epub_zip_determinism(OUT, EPUB_BUILD_MTIME)
    print(f"Записано: {OUT.relative_to(ROOT)} ({len(spine) - 1} страниц)")


if __name__ == "__main__":
    main()
