"""The EPUB publication adapter.

Owns exactly what docs/contracts/BOOK-BUILD-PIPELINE-CONTRACT.md section 12
assigns to an EPUB adapter: reflowable XHTML normalization, EPUB
navigation/spine/package metadata, and EPUB-specific asset packaging. It
receives the same ``CanonicalBookModel`` the PDF adapter receives (see
book_pipeline.model) and must not maintain independent chapter content,
translated strings, or chapter ordering of its own.
"""

from __future__ import annotations

import datetime
import mimetypes
import os
import re
from pathlib import Path

import book_shared as bs
from ebooklib import epub
from site_structure import SITE_ORIGIN

from .config import BookLocaleConfig
from .model import CanonicalBookModel, PageModel, ProjectModel, included_html_paths

ROOT = Path(__file__).resolve().parent.parent.parent

# Reproducible-builds timestamp (mirrors the PDF adapter's own
# PDF_SOURCE_DATE_EPOCH) — a fixed instant, never datetime.now()/time.time(),
# so two builds from identical source produce a byte-identical EPUB. ZIP's
# DOS-based date_time field cannot represent anything before 1980-01-01
# (raises ValueError), so unlike the PDF adapter's epoch-0 constant this
# floors at the earliest valid ZIP timestamp instead of the Unix epoch.
_ZIP_EPOCH_FLOOR = 315532800  # 1980-01-01T00:00:00Z as a Unix timestamp
_SOURCE_DATE_EPOCH_ENV = os.environ.get("SOURCE_DATE_EPOCH")
EPUB_BUILD_MTIME = datetime.datetime.fromtimestamp(
    max(int(_SOURCE_DATE_EPOCH_ENV), _ZIP_EPOCH_FLOOR) if _SOURCE_DATE_EPOCH_ENV else _ZIP_EPOCH_FLOOR,
    tz=datetime.UTC,
).replace(tzinfo=None)

# A small curated stylesheet for the project appendix's markup, rather than
# copying the full homepage.css: that file targets the homepage layout
# (course journey, practice filters, hero, etc. — all irrelevant here) and
# uses :has() — valid modern CSS for browsers, but not supported by
# epubcheck's stricter CSS3 parser (fails as CSS-008) nor guaranteed in
# e-reader rendering engines. Identical for every language: this is
# presentation of the shared ProjectCard component, not book content.
PROJECT_CSS = """
.project-hero { width: 100%; aspect-ratio: 16 / 9; overflow: hidden; }
.project-hero svg { display: block; width: 100%; height: 100%; }
.project-meta-row { margin: 8px 0 16px; }
.project-topic { display: inline-block; font-size: 0.8em; font-weight: 600; background: var(--gray-100); color: var(--gray-600); padding: 2px 10px; border-radius: 999px; margin: 0 6px 6px 0; }
.reference-board { margin: 16px 0; }
.reference-card { display: block; padding: 10px 0; text-decoration: none; color: var(--color-text-primary); border-top: 1px solid var(--color-border-default); }
.reference-card .rt { font-weight: 600; }
.reference-card .rs { font-size: 0.85em; color: var(--color-text-muted); }
"""


def _build_copyright_item(config: BookLocaleConfig, included_paths: frozenset[str]) -> epub.EpubHtml:
    """The EPUB's own copyright/rights page — a root-level spine item, read
    first, mirroring the PDF adapter's copyright page (both draw on the
    exact same config.rights_notice_paragraphs_html, so the two publication
    formats can never independently drift on the licensing model)."""
    content = bs.normalize_epub_content(
        "<html><body>"
        '<div class="copyright-page-epub">'
        f"<h1>{config.book_title}: {config.book_subtitle}</h1>"
        f"<p>{config.book_author} — Cartesian School</p>"
        f"{config.rights_notice_paragraphs_html}"
        "</div></body></html>",
        "copyright.html",
        included_paths,
        site_origin=SITE_ORIGIN,
        output_xhtml_path="copyright.xhtml",
    )
    item = bs.CaseSafeEpubHtml(title=config.epub_copyright_title, file_name="copyright.xhtml", lang=config.html_lang)
    item.content = content
    item.add_link(href="assets/css/theory.css", rel="stylesheet", type="text/css")
    return item


def _build_item(page: PageModel, included_paths: frozenset[str], config: BookLocaleConfig) -> epub.EpubHtml:
    content = bs.normalize_epub_content(page.content, page.rel_path, included_paths, site_origin=SITE_ORIGIN)
    file_name = page.rel_path.replace(".html", ".xhtml")
    item = bs.CaseSafeEpubHtml(title=page.title, file_name=file_name, lang=config.html_lang)
    item.content = content
    if re.search(r"<svg\b", content):
        item.properties.append("svg")
    if re.search(r"<math\b", content):
        item.properties.append("mathml")
    depth = page.rel_path.count("/")
    css_href = "../" * depth + "assets/css/theory.css"
    item.add_link(href=css_href, rel="stylesheet", type="text/css")
    return item


def _build_project_item(project: ProjectModel, included_paths: frozenset[str], config: BookLocaleConfig) -> epub.EpubHtml:
    file_name = f"projects/{project.slug}.xhtml"
    content = bs.normalize_epub_content(
        project.content, project.rel_path, included_paths, site_origin=SITE_ORIGIN, output_xhtml_path=file_name
    )
    item = bs.CaseSafeEpubHtml(title=project.title, file_name=file_name, lang=config.html_lang)
    item.content = content
    if re.search(r"<svg\b", content):
        item.properties.append("svg")
    if re.search(r"<math\b", content):
        item.properties.append("mathml")
    item.add_link(href="../assets/css/theory.css", rel="stylesheet", type="text/css")
    item.add_link(href="../assets/css/project.css", rel="stylesheet", type="text/css")
    return item


def build(model: CanonicalBookModel, config: BookLocaleConfig) -> None:
    book = epub.EpubBook()
    book.set_identifier(config.epub_identifier)
    book.set_title(f"{config.book_title}: {config.book_subtitle}")
    book.set_language(config.html_lang)
    book.add_author(config.book_author)
    book.add_metadata("DC", "description", config.book_description)
    book.add_metadata("DC", "publisher", "Cartesian School")
    book.add_metadata("DC", "rights", config.rights_notice_plain)

    css_text = bs.strip_has_selector_rules(
        (config.assets_root / "assets" / "css" / "theory.css").read_text(encoding="utf-8")
    )
    css_item = epub.EpubItem(
        uid="theory_css", file_name="assets/css/theory.css", media_type="text/css", content=css_text.encode("utf-8")
    )
    book.add_item(css_item)

    project_css_item = epub.EpubItem(
        uid="project_css", file_name="assets/css/project.css", media_type="text/css", content=PROJECT_CSS.encode("utf-8")
    )
    book.add_item(project_css_item)

    # Assets are shared verbatim between locales (config.assets_root is
    # always the RU site/ tree — PL never duplicates them).
    for asset_root in (
        config.assets_root / "assets" / "img",
        config.assets_root / "assets" / "brand",
        config.assets_root / "assets" / "icons",
    ):
        for asset_path in sorted(path for path in asset_root.rglob("*") if path.is_file()):
            relative = asset_path.relative_to(config.assets_root).as_posix()
            media_type = mimetypes.guess_type(asset_path.name)[0]
            if asset_path.suffix.lower() == ".svg":
                media_type = "image/svg+xml"
            if not media_type:
                raise RuntimeError(f"cannot determine EPUB media type: {asset_path}")
            book.add_item(
                epub.EpubItem(
                    uid=bs.ncx_id(relative),
                    file_name=relative,
                    media_type=media_type,
                    content=asset_path.read_bytes(),
                )
            )

    book.set_cover("cover.png", config.cover_png_path.read_bytes())

    included_paths = included_html_paths(model)
    toc = []
    spine = ["nav"]

    copyright_item = _build_copyright_item(config, included_paths)
    book.add_item(copyright_item)
    spine.append(copyright_item)
    toc.append(epub.Link(copyright_item.file_name, config.epub_copyright_title, bs.ncx_id(copyright_item.file_name)))

    fm_links = []
    for page in model.front_matter:
        item = _build_item(page, included_paths, config)
        book.add_item(item)
        spine.append(item)
        fm_links.append(epub.Link(item.file_name, page.title, bs.ncx_id(item.file_name)))
    toc.append((epub.Section(config.toc_intro_label), tuple(fm_links)))

    for chapter in model.chapters:
        ch_links = []
        for page in chapter.pages:
            item = _build_item(page, included_paths, config)
            book.add_item(item)
            spine.append(item)
            ch_links.append(epub.Link(item.file_name, page.title, bs.ncx_id(item.file_name)))
        toc.append((epub.Section(f"{config.chapter_word} {chapter.number}: {chapter.title}"), tuple(ch_links)))

    project_links = []
    for project in model.projects:
        item = _build_project_item(project, included_paths, config)
        book.add_item(item)
        spine.append(item)
        project_links.append(epub.Link(item.file_name, project.title, bs.ncx_id(item.file_name)))
    toc.append((epub.Section(config.toc_projects_label), tuple(project_links)))

    index_item = _build_item(model.index_page, included_paths, config)
    book.add_item(index_item)
    spine.append(index_item)
    toc.append(epub.Link(index_item.file_name, model.index_page.title, bs.ncx_id(index_item.file_name)))

    book.toc = tuple(toc)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = spine

    out = config.epub_output_path
    out.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(str(out), book, {"mtime": EPUB_BUILD_MTIME})
    bs.normalize_epub_zip_determinism(out, EPUB_BUILD_MTIME)
    print(f"Wrote: {out.relative_to(ROOT)} ({len(spine) - 1} pages)")
