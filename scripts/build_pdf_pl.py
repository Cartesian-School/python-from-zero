#!/usr/bin/env python3
"""Собирает канонический печатный PDF польского издания и его фактическую
пагинацию (book/pdf/python-od-zera-pl.pdf).

PL counterpart of build_pdf.py — reuses the exact same print stylesheet
(scripts/book_shared.py's build_print_css(), so a layout change applies to
both books at once), pagination/anchor bookkeeping, font validation, and
cover-merge machinery. Content comes from build_epub_pl.py's already-
resolved PL page list (site/pl/, PL front matter/titles read back from the
translated HTML itself — see that module's docstring for why there is no
separate PL "PAGES" source of truth to import).
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import book_shared as bs

os.environ["FONTCONFIG_FILE"] = str(bs.FONTCONFIG_POLICY_PATH)

import build_epub_pl as be
from weasyprint import HTML
from weasyprint import __version__ as WEASYPRINT_VERSION

SITE = ROOT / "site" / "pl"
OUT = ROOT / "book" / "pdf" / "python-od-zera-pl.pdf"
COVER_PDF = ROOT / "design" / "exports" / "cover_concept_v1_pl.pdf"
PAGINATION_OUT = ROOT / "data" / "book-pagination-pl.json"
LAYOUT_VERSION_TAG = "cartesian-school-book-layout-v1"

BOOK_TITLE = be.BOOK_TITLE
BOOK_SUBTITLE = be.BOOK_SUBTITLE
BOOK_AUTHOR = be.BOOK_AUTHOR
BOOK_AUTHOR_ROLE = "Software & AI Engineer, założyciel Cartesian School"
BOOK_DESCRIPTION = (
    "Książka dla początkujących: Python 3.14, grafika w Turtle, aplikacje w "
    "Tkinter, gry w Pygame i tworzenie stron internetowych we Flasku."
)
SITE_URL_DISPLAY = "cartesianschool.org"

PRINT_CSS = bs.build_print_css(book_title=BOOK_TITLE, page_abbrev="STR.")


def build_title_page() -> str:
    return f"""
    <div class="title-page">
      <div class="kicker">PYTHON 3.14 · OD ZERA</div>
      <h1>{BOOK_TITLE}</h1>
      <div class="subtitle">{BOOK_SUBTITLE}</div>
      <div class="author">{BOOK_AUTHOR}</div>
      <div class="author-role">{BOOK_AUTHOR_ROLE}</div>
    </div>
    """


def build_copyright_page() -> str:
    """The book's own copyright/rights notice — draws on
    be.RIGHTS_NOTICE_PARAGRAPHS_HTML (build_epub_pl.py) so the PDF and EPUB
    can never independently drift on the licensing model. See build_pdf.py's
    RU counterpart for the full licensing-scope rationale this mirrors."""
    return f"""
    <div class="copyright-page">
      <p class="cp-title">{BOOK_TITLE}: {BOOK_SUBTITLE}</p>
      <p>{BOOK_AUTHOR} — {BOOK_AUTHOR_ROLE}</p>
      <p>Wydanie Cartesian School, 2026. Python 3.14.</p>
      <p>Wydanie elektroniczne. Wersja online kursu, interaktywna praktyka w
      przeglądarce i kod źródłowy wszystkich projektów — {SITE_URL_DISPLAY}</p>
      {be.RIGHTS_NOTICE_PARAGRAPHS_HTML}
    </div>
    """


def build_toc_entries() -> str:
    parts = ['<div class="toc-part-title">Materiały wprowadzające</div>']
    for anchor_id, title in be.FRONT_MATTER:
        marker = "fm-" + anchor_id.rsplit("/", 1)[-1].replace(".html", "")
        parts.append(f'<a class="toc-entry" href="#{marker}"><span class="toc-label">{title}</span></a>')

    for num in range(1, 25):
        title = be.chapter_title(num)
        parts.append(f'<a class="toc-entry toc-chapter" href="#marker-ch-{num}"><span class="toc-label">Rozdział {num}. {title}</span></a>')

    parts.append('<div class="toc-part-title">Projekty</div>')
    for entry in be.PROJECTS:
        parts.append(f'<a class="toc-entry" href="#proj-{entry["slug"]}"><span class="toc-label">{entry["title"]}</span></a>')

    parts.append('<div class="toc-part-title">Kompendium</div>')
    parts.append('<a class="toc-entry" href="#marker-index"><span class="toc-label">Indeks rzeczowy</span></a>')

    return f"""
    <div class="toc-page chapter-break">
      <h1>Spis treści</h1>
      {"".join(parts)}
    </div>
    """


strip_wrapper = bs.strip_wrapper
printify_notebook_cards = bs.printify_notebook_cards


def printify_opener(inner_html: str, num: int, marker_id: str) -> str:
    return bs.printify_opener(inner_html, num, marker_id, chapter_label=f"ROZDZIAŁ {num}")


def build_projects_appendix() -> str:
    parts = [
        '<div class="chapter-break"><h1>Projekty</h1>'
        "<p>Dwanaście gotowych mini-projektów z otwartym kodem źródłowym — od "
        "„Kółko i krzyżyk” po pełnoprawną kosmiczną strzelankę. Kod źródłowy i "
        "działająca wersja każdego z nich — na stronie kursu.</p></div>"
    ]
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
        page_markers.append((marker, f"/pl/{rel_path}"))

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
            page_markers.append((marker_id, f"/pl/{rel_path}"))

    project_marker = "marker-projects"
    projects_html = build_projects_appendix().replace(
        '<div class="chapter-break">',
        f'<div id="{project_marker}" class="chapter-break">',
        1,
    )
    parts.append(projects_html)

    idx_html = (SITE / "indeks-rzeczowy.html").read_text(encoding="utf-8")
    idx_inner = strip_wrapper(be.extract_article(idx_html))
    parts.append(f'<div id="marker-index" class="chapter-break">{idx_inner}</div>')

    full_html = (
        "<html lang='pl'><head><meta charset='utf-8'>"
        f"<title>{BOOK_TITLE}: {BOOK_SUBTITLE}</title>"
        f"<meta name='author' content='{BOOK_AUTHOR}'>"
        f"<meta name='description' content='{BOOK_DESCRIPTION}'>"
        f"<style>{PRINT_CSS}</style></head><body>{''.join(parts)}</body></html>"
    )
    return full_html, chapter_markers, page_markers, project_marker


resolve_anchor_pages = bs.resolve_anchor_pages


def main() -> None:
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
    tmp_content_pdf = OUT.parent / "_content_tmp_pl.pdf"
    doc.write_pdf(str(tmp_content_pdf))
    bs.merge_cover(tmp_content_pdf, COVER_PDF, OUT)
    tmp_content_pdf.unlink()

    # +1 physical page for the merged, WeasyPrint-external cover.
    final_total_pages = total_pages + 1
    final_anchor_pages = {marker_id: page + 1 for marker_id, page in anchor_pages.items()}

    chapter_title_url = {
        num: (be.chapter_title(num), f"/pl/chapters/rozdzial-{num:02d}/index.html")
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

    print(f"Zapisano: {OUT.relative_to(ROOT)} ({final_total_pages} stron)")
    for marker_id, num in chapter_markers:
        print(f"  Rozdział {num:>2}: strona fizyczna {final_anchor_pages[marker_id]}")
    print(f"  Indeks rzeczowy: strona fizyczna {final_anchor_pages['marker-index']}")
    print(f"  Łączna liczba stron fizycznych: {final_total_pages}")
    print(f"Zapisano: {PAGINATION_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
