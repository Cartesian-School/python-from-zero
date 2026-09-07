"""The canonical locale configuration contract.

A :class:`BookLocaleConfig` instance is the *only* thing a language edition
may contribute to the book-build pipeline: content location, canonical
content-discovery callables, and localized labels/metadata (see
docs/contracts/BOOK-BUILD-PIPELINE-CONTRACT.md, section 4). It MUST NOT
contain rendering, packaging, or pagination logic — that belongs to
:mod:`book_pipeline.model` (shared) and :mod:`book_pipeline.pdf_adapter` /
:mod:`book_pipeline.epub_adapter` (format-specific).
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ProjectEntry:
    slug: str
    title: str


@dataclass(frozen=True, slots=True)
class BookLocaleConfig:
    # -- identity ---------------------------------------------------------
    language: str
    html_lang: str
    site: Path
    assets_root: Path  # site tree that physically owns the shared assets/CSS this locale reuses

    # -- book metadata ------------------------------------------------------
    book_title: str
    book_subtitle: str
    book_author: str
    book_author_role: str
    book_description: str
    site_url_display: str

    # -- licensing ----------------------------------------------------------
    rights_holder: str
    content_license_name: str
    content_license_url: str
    rights_notice_plain: str
    rights_notice_paragraphs_html: str

    # -- localized labels -----------------------------------------------------
    chapter_word: str  # "Глава" / "Rozdział"
    title_page_kicker: str
    page_abbrev: str  # "СТР." / "STR."
    toc_title: str
    toc_intro_label: str
    toc_projects_label: str
    toc_reference_label: str
    toc_index_label: str
    copyright_edition_line: str
    copyright_electronic_line: str
    projects_intro_html: str
    epub_copyright_title: str
    epub_identifier: str

    # -- locale-specific site path mapping ----------------------------------
    url_path_prefix: str  # "" for ru, "/pl" for pl
    index_relpath: str  # e.g. "predmetnyj-ukazatel.html" / "indeks-rzeczowy.html"

    # -- localized output filenames -------------------------------------------
    pdf_output_path: Path
    pagination_output_path: Path
    cover_pdf_path: Path
    epub_output_path: Path
    cover_png_path: Path

    # -- canonical content discovery (language-specific SOURCE, not logic) --
    front_matter: Sequence[tuple[str, str]]
    project_entries: Sequence[ProjectEntry]
    chapter_pages: Callable[[int], list[tuple[str, str]]]
    chapter_title: Callable[[int], str]
    chapter_canonical_url: Callable[[int], str]
