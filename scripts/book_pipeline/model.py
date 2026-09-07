"""The canonical, format-independent book model and its loader.

Per docs/contracts/BOOK-BUILD-PIPELINE-CONTRACT.md section 3, every one of
these stages is shared by every language and every publication format:

    selected language -> locale configuration -> canonical content discovery
    -> canonical book model -> common normalization -> common semantic
    rendering -> [format adapter]

``CanonicalBookLoader.load`` performs all of it up to and including common
semantic rendering: it reads each page's HTML from disk exactly once and
extracts its stable content fragment (article body, chapter opener hero, or
project detail) via the same book_shared functions for every language and
every format. The PDF and EPUB adapters each receive the identical
``CanonicalBookModel`` and apply only their own format-specific presentation
transform on top (print pagination markers vs. reflowable XHTML packaging).
"""

from __future__ import annotations

from dataclasses import dataclass

import book_shared as bs
from site_structure import SITE_ORIGIN

from .config import BookLocaleConfig


@dataclass(frozen=True, slots=True)
class PageModel:
    rel_path: str
    title: str
    content: str  # already extract_article()/extract_opener()-rendered


@dataclass(frozen=True, slots=True)
class ChapterModel:
    number: int
    pages: tuple[PageModel, ...]  # pages[0] is always the chapter opener
    title: str
    canonical_url: str


@dataclass(frozen=True, slots=True)
class ProjectModel:
    slug: str
    title: str
    rel_path: str
    content: str


@dataclass(frozen=True, slots=True)
class CanonicalBookModel:
    language: str
    front_matter: tuple[PageModel, ...]
    chapters: tuple[ChapterModel, ...]  # numbers 1..24, in canonical order
    projects: tuple[ProjectModel, ...]
    index_page: PageModel


def _read(site, rel_path: str) -> str:
    return (site / rel_path).read_text(encoding="utf-8")


class CanonicalBookLoader:
    """Locale-independent source loader. Every language goes through this
    exact same algorithm; a language contributes only its config's content
    discovery callables/data (see BookLocaleConfig)."""

    @staticmethod
    def load(config: BookLocaleConfig) -> CanonicalBookModel:
        front_matter = tuple(
            PageModel(
                rel_path=rel_path,
                title=title,
                content=bs.extract_article(_read(config.site, rel_path), site_origin=SITE_ORIGIN),
            )
            for rel_path, title in config.front_matter
        )

        chapters = []
        for number in range(1, 25):
            pages = []
            for index, (rel_path, title) in enumerate(config.chapter_pages(number)):
                html_text = _read(config.site, rel_path)
                content = (
                    bs.extract_opener(html_text, site_origin=SITE_ORIGIN)
                    if index == 0
                    else bs.extract_article(html_text, site_origin=SITE_ORIGIN)
                )
                pages.append(PageModel(rel_path=rel_path, title=title, content=content))
            chapters.append(
                ChapterModel(
                    number=number,
                    pages=tuple(pages),
                    title=config.chapter_title(number),
                    canonical_url=config.chapter_canonical_url(number),
                )
            )

        projects = tuple(
            ProjectModel(
                slug=entry.slug,
                title=entry.title,
                rel_path=f"projects/{entry.slug}/index.html",
                content=bs.extract_project(
                    _read(config.site, f"projects/{entry.slug}/index.html"),
                    site_origin=SITE_ORIGIN,
                ),
            )
            for entry in config.project_entries
        )

        index_page = PageModel(
            rel_path=config.index_relpath,
            title=config.toc_index_label,
            content=bs.extract_article(_read(config.site, config.index_relpath), site_origin=SITE_ORIGIN),
        )

        return CanonicalBookModel(
            language=config.language,
            front_matter=front_matter,
            chapters=tuple(chapters),
            projects=projects,
            index_page=index_page,
        )


def included_html_paths(model: CanonicalBookModel) -> frozenset[str]:
    """Every site-root-relative HTML path bundled inside this book — derived
    from the canonical model itself, so it can never drift from what the
    model actually contains."""
    paths = {page.rel_path for page in model.front_matter}
    for chapter in model.chapters:
        paths.update(page.rel_path for page in chapter.pages)
    paths.update(project.rel_path for project in model.projects)
    paths.add(model.index_page.rel_path)
    return frozenset(paths)
