"""RU locale content discovery and metadata.

Contains only what docs/contracts/BOOK-BUILD-PIPELINE-CONTRACT.md section 4
permits a language edition to contribute: content location, page
discovery/ordering, and localized labels. No rendering, packaging, or
pagination logic lives here — that is shared (book_pipeline.model) or
format-specific (book_pipeline.pdf_adapter / book_pipeline.epub_adapter).
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path

import chapter_metadata

from book_pipeline.config import BookLocaleConfig, ProjectEntry

ROOT = Path(__file__).resolve().parent.parent.parent
SITE = ROOT / "site"

_PROJECTS_MANIFEST = json.loads(
    (ROOT / "manifest" / "projects_manifest.json").read_text(encoding="utf-8")
)["projects"]

BOOK_TITLE = "Python с нуля"
BOOK_SUBTITLE = "программирование, графика, приложения и игры"
BOOK_AUTHOR = "Siergej Sobolewski"
BOOK_AUTHOR_ROLE = "Software & AI Engineer, основатель Cartesian School"
BOOK_DESCRIPTION = (
    "Книга для начинающих: Python 3.14, графика на Turtle, приложения на "
    "Tkinter, игры на Pygame и веб-разработка на Flask."
)
SITE_URL_DISPLAY = "cartesianschool.org"

RIGHTS_HOLDER = "Siergej Sobolewski / Cartesian School"
CONTENT_LICENSE_NAME = (
    "Creative Commons Attribution-NonCommercial-ShareAlike "
    "4.0 International (CC BY-NC-SA 4.0)"
)
CONTENT_LICENSE_URL = "https://creativecommons.org/licenses/by-nc-sa/4.0/"

# Prose/explanations/diagrams/assignments are CC BY-NC-SA 4.0. ALL code is
# MIT (see LICENSE-CODE.md at the repository root) unless a file/directory
# states otherwise — including inline code snippets printed inside this very
# book's text, not just the standalone projects appendix. Shared verbatim by
# the PDF and EPUB adapters so the two publication formats can never
# independently drift on the licensing model.
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

FRONT_MATTER: list[tuple[str, str]] = [
    ("front-matter/ob-avtore.html", "Об авторе"),
    ("front-matter/o-tehnicheskom-recenzente.html", "О техническом рецензенте"),
    ("front-matter/vvedenie.html", "Введение"),
]

PROJECT_ENTRIES = [
    ProjectEntry(slug=entry["slug"], title=entry["title"]) for entry in _PROJECTS_MANIFEST
]


def chapter_pages(num: int) -> list[tuple[str, str]]:
    mod = importlib.import_module(f"build_chapter_{num:02d}")
    # Chapter 23 additionally stores a stable curriculum sequence number as
    # the third tuple item. The book pipeline consumes only URL and title.
    return [(f"chapters/glava-{num:02d}/{entry[0]}", entry[1]) for entry in mod.PAGES]


def chapter_title(num: int) -> str:
    return chapter_metadata.chapter_title(num)


def chapter_canonical_url(num: int) -> str:
    return chapter_metadata.chapter_url(num)


CONFIG = BookLocaleConfig(
    language="ru",
    html_lang="ru",
    site=SITE,
    assets_root=SITE,
    book_title=BOOK_TITLE,
    book_subtitle=BOOK_SUBTITLE,
    book_author=BOOK_AUTHOR,
    book_author_role=BOOK_AUTHOR_ROLE,
    book_description=BOOK_DESCRIPTION,
    site_url_display=SITE_URL_DISPLAY,
    rights_holder=RIGHTS_HOLDER,
    content_license_name=CONTENT_LICENSE_NAME,
    content_license_url=CONTENT_LICENSE_URL,
    rights_notice_plain=RIGHTS_NOTICE_PLAIN,
    rights_notice_paragraphs_html=RIGHTS_NOTICE_PARAGRAPHS_HTML,
    chapter_word="Глава",
    title_page_kicker="PYTHON 3.14 · С НУЛЯ",
    page_abbrev="СТР.",
    toc_title="Оглавление",
    toc_intro_label="Вводные материалы",
    toc_projects_label="Проекты",
    toc_reference_label="Справочник",
    toc_index_label="Предметный указатель",
    copyright_edition_line="Издание Cartesian School, 2026. Python 3.14.",
    copyright_electronic_line=(
        "Электронное издание. Онлайн-версия курса, интерактивная практика в браузере\n"
        f"      и исходный код всех проектов — {SITE_URL_DISPLAY}"
    ),
    projects_intro_html=(
        "<h1>Проекты</h1><p>Двенадцать готовых мини-проектов с открытым "
        "исходным кодом — от «Крестики-нолики» до полноценного космического "
        "шутера. Исходный код и живая версия каждого — на сайте курса.</p>"
    ),
    epub_copyright_title="Правовая информация",
    epub_identifier="cartesian-school-python-s-nulya-2026",
    url_path_prefix="",
    index_relpath="predmetnyj-ukazatel.html",
    pdf_output_path=ROOT / "book" / "pdf" / "python-s-nulya-ru.pdf",
    pagination_output_path=ROOT / "data" / "book-pagination.json",
    cover_pdf_path=ROOT / "design" / "exports" / "cover_concept_v1.pdf",
    epub_output_path=ROOT / "book" / "epub" / "python-s-nulya-ru.epub",
    cover_png_path=ROOT / "design" / "exports" / "cover_concept_v1.png",
    front_matter=FRONT_MATTER,
    project_entries=PROJECT_ENTRIES,
    chapter_pages=chapter_pages,
    chapter_title=chapter_title,
    chapter_canonical_url=chapter_canonical_url,
)
