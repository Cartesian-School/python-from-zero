#!/usr/bin/env python3
"""Собирает канонический печатный PDF и его фактическую пагинацию.

Переиспользует извлечение содержимого страниц из build_epub.py (тот же <article> /
.chapter-hero+.section-list разбор), но склеивает всё в один HTML-документ с печатной
типографикой: обложка (уже готовый дизайн-концепт, склеен как первая физическая
страница через pypdf), титульный лист, страница авторских прав, оглавление с реальными
номерами страниц (CSS target-counter, без ручного пересчёта),
разрыв страницы перед каждой главой, колонтитулы, приложение с проектами, предметный
указатель.

Нумерация страниц сквозная: обложка и титульный лист не показывают folio, остальные
страницы используют арабские числа физического PDF. Каждая глава начинается на recto
через ``break-before: right``; возникающая blank page учитывается физическим page tree.

Физическое дерево итогового PDF является единственной authority для start pages.
Builder пишет ``data/book-pagination.json`` из реально отрендеренных anchors; старые
минимальные страницы или ручные offsets в расчёте не участвуют.
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import book_shared as bs

# Pango initializes Fontconfig while WeasyPrint constructs the document font
# configuration.  Set the canonical policy before importing WeasyPrint so a
# mutable system emoji face can never enter layout or PDF serialization.
os.environ["FONTCONFIG_FILE"] = str(bs.FONTCONFIG_POLICY_PATH)

import build_epub as be
from chapter_metadata import chapters
from weasyprint import HTML
from weasyprint import __version__ as WEASYPRINT_VERSION

SITE = ROOT / "site"
OUT = ROOT / "book" / "pdf" / "python-s-nulya-ru.pdf"
COVER_PDF = ROOT / "design" / "exports" / "cover_concept_v1.pdf"
PAGINATION_OUT = ROOT / "data" / "book-pagination.json"
LAYOUT_VERSION_TAG = "cartesian-school-book-layout-v1"

BOOK_TITLE = "Python с нуля"
BOOK_SUBTITLE = "программирование, графика, приложения и игры"
BOOK_AUTHOR = "Siergej Sobolewski"
BOOK_AUTHOR_ROLE = "Software & AI Engineer, основатель Cartesian School"
BOOK_DESCRIPTION = "Книга для начинающих: Python 3.14, графика на Turtle, приложения на Tkinter, игры на Pygame и веб-разработка на Flask."
SITE_URL_DISPLAY = "cartesianschool.org"


PRINT_CSS = bs.build_print_css(book_title=BOOK_TITLE, page_abbrev="СТР.")


def build_title_page() -> str:
    return f"""
    <div class="title-page">
      <div class="kicker">PYTHON 3.14 · С НУЛЯ</div>
      <h1>{BOOK_TITLE}</h1>
      <div class="subtitle">{BOOK_SUBTITLE}</div>
      <div class="author">{BOOK_AUTHOR}</div>
      <div class="author-role">{BOOK_AUTHOR_ROLE}</div>
    </div>
    """


def build_copyright_page() -> str:
    """The book's own copyright/rights notice.

    Draws on be.RIGHTS_NOTICE_PARAGRAPHS_HTML (defined once in build_epub.py,
    which this module already imports as `be`) rather than a second, locally
    authored copy — so the PDF and EPUB can never independently drift on the
    licensing model. Prose/explanations/diagrams/assignments are CC BY-NC-SA
    4.0. ALL code is MIT (see LICENSE-CODE.md at the repository root) unless
    a file/directory states otherwise — including inline code snippets
    printed inside this very book's text, not just the standalone projects
    appendix. The full MIT text is intentionally NOT reproduced here — a
    short, scoped reference is the accurate statement for a book copyright
    page; the complete license text lives in the repository's own
    LICENSE-CODE.md."""
    return f"""
    <div class="copyright-page">
      <p class="cp-title">{BOOK_TITLE}: {BOOK_SUBTITLE}</p>
      <p>{BOOK_AUTHOR} — {BOOK_AUTHOR_ROLE}</p>
      <p>Издание Cartesian School, 2026. Python 3.14.</p>
      <p>Электронное издание. Онлайн-версия курса, интерактивная практика в браузере
      и исходный код всех проектов — {SITE_URL_DISPLAY}</p>
      {be.RIGHTS_NOTICE_PARAGRAPHS_HTML}
    </div>
    """


def build_toc_entries() -> str:
    parts = ['<div class="toc-part-title">Вводные материалы</div>']
    for anchor_id, title in be.FRONT_MATTER:
        marker = "fm-" + anchor_id.rsplit("/", 1)[-1].replace(".html", "")
        parts.append(f'<a class="toc-entry" href="#{marker}"><span class="toc-label">{title}</span></a>')

    for num in range(1, 25):
        title = be.chapter_title(num)
        parts.append(f'<a class="toc-entry toc-chapter" href="#marker-ch-{num}"><span class="toc-label">Глава {num}. {title}</span></a>')

    parts.append('<div class="toc-part-title">Проекты</div>')
    for entry in be.PROJECTS:
        parts.append(f'<a class="toc-entry" href="#proj-{entry["slug"]}"><span class="toc-label">{entry["title"]}</span></a>')

    parts.append('<div class="toc-part-title">Справочник</div>')
    parts.append('<a class="toc-entry" href="#marker-index"><span class="toc-label">Предметный указатель</span></a>')

    return f"""
    <div class="toc-page chapter-break">
      <h1>Оглавление</h1>
      {"".join(parts)}
    </div>
    """


strip_wrapper = bs.strip_wrapper
printify_notebook_cards = bs.printify_notebook_cards


def printify_opener(inner_html: str, num: int, marker_id: str) -> str:
    return bs.printify_opener(inner_html, num, marker_id, chapter_label=f"ГЛАВА {num}")


def build_projects_appendix() -> str:
    parts = ['<div class="chapter-break"><h1>Проекты</h1><p>Двенадцать готовых мини-проектов с открытым исходным кодом — от «Крестики-нолики» до полноценного космического шутера. Исходный код и живая версия каждого — на сайте курса.</p></div>']
    for entry in be.PROJECTS:
        html_text = (SITE / "projects" / entry["slug"] / "index.html").read_text(encoding="utf-8")
        inner = strip_wrapper(be.extract_project(html_text))
        parts.append(f'<div id="proj-{entry["slug"]}" class="project-entry">{inner}</div>')
    return "".join(parts)


def build_full_html() -> tuple[
    str,
    list[tuple[str, int]],
    list[tuple[str, str]],
    str,
]:
    parts = [build_title_page(), build_copyright_page(), build_toc_entries()]
    chapter_markers: list[tuple[str, int]] = []  # (marker_id, chapter_num)
    page_markers: list[tuple[str, str]] = []  # (marker_id, canonical URL)

    for rel_path, _title in be.FRONT_MATTER:
        marker = "fm-" + rel_path.rsplit("/", 1)[-1].replace(".html", "")
        html_text = (SITE / rel_path).read_text(encoding="utf-8")
        inner = printify_notebook_cards(strip_wrapper(be.extract_article(html_text)))
        parts.append(f'<div id="{marker}" class="chapter-break">{inner}</div>')
        page_markers.append((marker, f"/{rel_path}"))

    for num in range(1, 25):
        pages = be.chapter_pages(num)
        for i, (rel_path, _title) in enumerate(pages):
            html_text = (SITE / rel_path).read_text(encoding="utf-8")
            if i == 0:
                marker_id = f"marker-ch-{num}"
                inner = printify_opener(
                    strip_wrapper(be.extract_opener(html_text)), num, marker_id
                )
                parts.append(inner)
                chapter_markers.append((marker_id, num))
            else:
                marker_id = f"marker-page-{num:02d}-{i:03d}"
                inner = printify_notebook_cards(strip_wrapper(be.extract_article(html_text)))
                parts.append(f'<div id="{marker_id}">{inner}</div>')
            page_markers.append((marker_id, f"/{rel_path}"))

    project_marker = "marker-projects"
    projects_html = build_projects_appendix().replace(
        '<div class="chapter-break">',
        f'<div id="{project_marker}" class="chapter-break">',
        1,
    )
    parts.append(projects_html)

    idx_html = (SITE / "predmetnyj-ukazatel.html").read_text(encoding="utf-8")
    idx_inner = strip_wrapper(be.extract_article(idx_html))
    parts.append(f'<div id="marker-index" class="chapter-break">{idx_inner}</div>')

    full_html = (
        "<html lang='ru'><head><meta charset='utf-8'>"
        f"<title>{BOOK_TITLE}: {BOOK_SUBTITLE}</title>"
        f"<meta name='author' content='{BOOK_AUTHOR}'>"
        f"<meta name='description' content='{BOOK_DESCRIPTION}'>"
        f"<style>{PRINT_CSS}</style></head><body>{''.join(parts)}</body></html>"
    )
    return full_html, chapter_markers, page_markers, project_marker


resolve_anchor_pages = bs.resolve_anchor_pages


def main() -> None:
    # FontTools reads SOURCE_DATE_EPOCH when serializing embedded subsets.
    # Override any caller-specific value so this canonical build has one
    # explicit, portable timestamp contract.
    os.environ["SOURCE_DATE_EPOCH"] = bs.PDF_SOURCE_DATE_EPOCH
    if not COVER_PDF.is_file():
        raise RuntimeError(f"cover PDF is missing: {COVER_PDF}")
    bs.validate_fontconfig_policy()
    font_records = bs.validate_font_files()
    full_html, chapter_markers, page_markers, project_marker = build_full_html()

    doc = HTML(string=full_html, base_url=str(SITE)).render()
    total_pages = len(doc.pages)
    marker_ids = {
        marker_id for marker_id, _num in chapter_markers
    } | {
        marker_id for marker_id, _url in page_markers
    } | {project_marker, "marker-index"}
    anchor_pages = resolve_anchor_pages(doc, marker_ids)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp_content_pdf = OUT.parent / "_content_tmp.pdf"
    doc.write_pdf(str(tmp_content_pdf))
    bs.merge_cover(tmp_content_pdf, COVER_PDF, OUT)
    tmp_content_pdf.unlink()

    # +1 physical page for the merged, WeasyPrint-external cover.
    final_total_pages = total_pages + 1
    final_anchor_pages = {marker_id: page + 1 for marker_id, page in anchor_pages.items()}

    canonical_chapters = {item.number: item for item in chapters()}
    chapter_title_url = {
        num: (canonical_chapters[num].title, canonical_chapters[num].url)
        for num in range(1, 25)
    }

    bs.write_pdf_pagination_metadata(
        out_pdf=OUT,
        pagination_out=PAGINATION_OUT,
        cover_pdf_path=COVER_PDF,
        full_html=full_html,
        font_records=font_records,
        final_total_pages=final_total_pages,
        final_anchor_pages=final_anchor_pages,
        chapter_markers=chapter_markers,
        page_markers=page_markers,
        project_marker=project_marker,
        chapter_title_url=chapter_title_url,
        layout_version_tag=LAYOUT_VERSION_TAG,
        weasyprint_version=WEASYPRINT_VERSION,
    )

    print(f"Записано: {OUT.relative_to(ROOT)} ({final_total_pages} страниц)")
    for marker_id, num in chapter_markers:
        print(f"  Глава {num:>2}: физическая стр. {final_anchor_pages[marker_id]}")
    print(f"  Предметный указатель: физическая стр. {final_anchor_pages['marker-index']}")
    print(f"  Всего физических страниц: {final_total_pages}")
    print(f"Записано: {PAGINATION_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
