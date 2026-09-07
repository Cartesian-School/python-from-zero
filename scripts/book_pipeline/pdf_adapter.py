"""The PDF publication adapter.

Owns exactly what docs/contracts/BOOK-BUILD-PIPELINE-CONTRACT.md section 11
assigns to a PDF adapter: physical page geometry, print CSS, running
headers/footers, pagination bookkeeping, font embedding validation, and
cover-PDF merging. It receives the same ``CanonicalBookModel`` the EPUB
adapter receives (see book_pipeline.model) and must not maintain independent
chapter content, translated strings, or chapter ordering of its own.

Page numbering is continuous: the cover and title page show no folio, every
later page uses Arabic physical-PDF numbers. Each chapter starts on a recto
page via ``break-before: right``; any resulting blank page is accounted for
by the physical page tree. The physical page tree of the rendered PDF is the
single authority for chapter start pages — this module writes the pagination
sidecar (``<language>``'s ``pagination_output_path``) from the actually
rendered anchors, never from manual offsets.
"""

from __future__ import annotations

import os
from pathlib import Path

import book_shared as bs

# Pango initializes Fontconfig while WeasyPrint constructs the document font
# configuration. Set the canonical policy before importing WeasyPrint so a
# mutable system emoji face can never enter layout or PDF serialization.
os.environ["FONTCONFIG_FILE"] = str(bs.FONTCONFIG_POLICY_PATH)

from weasyprint import HTML
from weasyprint import __version__ as WEASYPRINT_VERSION

from .config import BookLocaleConfig
from .model import CanonicalBookModel

ROOT = Path(__file__).resolve().parent.parent.parent
LAYOUT_VERSION_TAG = "cartesian-school-book-layout-v1"


def _front_matter_marker(rel_path: str) -> str:
    return "fm-" + rel_path.rsplit("/", 1)[-1].replace(".html", "")


def build_title_page(config: BookLocaleConfig) -> str:
    return f"""
    <div class="title-page">
      <div class="kicker">{config.title_page_kicker}</div>
      <h1>{config.book_title}</h1>
      <div class="subtitle">{config.book_subtitle}</div>
      <div class="author">{config.book_author}</div>
      <div class="author-role">{config.book_author_role}</div>
    </div>
    """


def build_copyright_page(config: BookLocaleConfig) -> str:
    """The book's own copyright/rights notice. Draws on
    config.rights_notice_paragraphs_html — the exact same fragment the EPUB
    adapter's copyright item uses — so the two publication formats can never
    independently drift on the licensing model. The full MIT text is
    intentionally NOT reproduced here — a short, scoped reference is the
    accurate statement for a book copyright page; the complete license text
    lives in the repository's own LICENSE-CODE.md."""
    return f"""
    <div class="copyright-page">
      <p class="cp-title">{config.book_title}: {config.book_subtitle}</p>
      <p>{config.book_author} — {config.book_author_role}</p>
      <p>{config.copyright_edition_line}</p>
      <p>{config.copyright_electronic_line}</p>
      {config.rights_notice_paragraphs_html}
    </div>
    """


def build_toc_entries(model: CanonicalBookModel, config: BookLocaleConfig) -> str:
    parts = [f'<div class="toc-part-title">{config.toc_intro_label}</div>']
    for page in model.front_matter:
        marker = _front_matter_marker(page.rel_path)
        parts.append(f'<a class="toc-entry" href="#{marker}"><span class="toc-label">{page.title}</span></a>')

    for chapter in model.chapters:
        label = f"{config.chapter_word} {chapter.number}. {chapter.title}"
        parts.append(
            f'<a class="toc-entry toc-chapter" href="#marker-ch-{chapter.number}">'
            f'<span class="toc-label">{label}</span></a>'
        )

    parts.append(f'<div class="toc-part-title">{config.toc_projects_label}</div>')
    for project in model.projects:
        parts.append(f'<a class="toc-entry" href="#proj-{project.slug}"><span class="toc-label">{project.title}</span></a>')

    parts.append(f'<div class="toc-part-title">{config.toc_reference_label}</div>')
    parts.append(f'<a class="toc-entry" href="#marker-index"><span class="toc-label">{config.toc_index_label}</span></a>')

    return f"""
    <div class="toc-page chapter-break">
      <h1>{config.toc_title}</h1>
      {"".join(parts)}
    </div>
    """


def build_full_html(
    model: CanonicalBookModel, config: BookLocaleConfig
) -> tuple[str, list[tuple[str, int]], list[tuple[str, str]], str]:
    print_css = bs.build_print_css(book_title=config.book_title, page_abbrev=config.page_abbrev)
    parts = [build_title_page(config), build_copyright_page(config), build_toc_entries(model, config)]
    chapter_markers: list[tuple[str, int]] = []  # (marker_id, chapter_num)
    page_markers: list[tuple[str, str]] = []  # (marker_id, canonical URL)

    for page in model.front_matter:
        marker = _front_matter_marker(page.rel_path)
        inner = bs.printify_notebook_cards(bs.strip_wrapper(page.content))
        parts.append(f'<div id="{marker}" class="chapter-break">{inner}</div>')
        page_markers.append((marker, config.url_path_prefix + "/" + page.rel_path))

    for chapter in model.chapters:
        for index, page in enumerate(chapter.pages):
            if index == 0:
                marker_id = f"marker-ch-{chapter.number}"
                chapter_label = f"{config.chapter_word.upper()} {chapter.number}"
                inner = bs.printify_opener(
                    bs.strip_wrapper(page.content), chapter.number, marker_id, chapter_label=chapter_label
                )
                parts.append(inner)
                chapter_markers.append((marker_id, chapter.number))
            else:
                marker_id = f"marker-page-{chapter.number:02d}-{index:03d}"
                inner = bs.printify_notebook_cards(bs.strip_wrapper(page.content))
                parts.append(f'<div id="{marker_id}">{inner}</div>')
            page_markers.append((marker_id, config.url_path_prefix + "/" + page.rel_path))

    project_marker = "marker-projects"
    parts.append(f'<div id="{project_marker}" class="chapter-break">{config.projects_intro_html}</div>')
    for project in model.projects:
        parts.append(f'<div id="proj-{project.slug}" class="project-entry">{bs.strip_wrapper(project.content)}</div>')

    parts.append(f'<div id="marker-index" class="chapter-break">{bs.strip_wrapper(model.index_page.content)}</div>')

    full_html = (
        f"<html lang='{config.html_lang}'><head><meta charset='utf-8'>"
        f"<title>{config.book_title}: {config.book_subtitle}</title>"
        f"<meta name='author' content='{config.book_author}'>"
        f"<meta name='description' content='{config.book_description}'>"
        f"<style>{print_css}</style></head><body>{''.join(parts)}</body></html>"
    )
    return full_html, chapter_markers, page_markers, project_marker


def build(model: CanonicalBookModel, config: BookLocaleConfig) -> None:
    # FontTools reads SOURCE_DATE_EPOCH when serializing embedded subsets.
    # Override any caller-specific value so this canonical build has one
    # explicit, portable timestamp contract.
    os.environ["SOURCE_DATE_EPOCH"] = bs.PDF_SOURCE_DATE_EPOCH
    if not config.cover_pdf_path.is_file():
        raise RuntimeError(f"cover PDF is missing: {config.cover_pdf_path}")
    bs.validate_fontconfig_policy()
    font_records = bs.validate_font_files()
    full_html, chapter_markers, page_markers, project_marker = build_full_html(model, config)

    doc = HTML(string=full_html, base_url=str(config.site)).render()
    total_pages = len(doc.pages)
    marker_ids = (
        {marker_id for marker_id, _num in chapter_markers}
        | {marker_id for marker_id, _url in page_markers}
        | {project_marker, "marker-index"}
    )
    anchor_pages = bs.resolve_anchor_pages(doc, marker_ids)

    out = config.pdf_output_path
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp_content_pdf = out.parent / f"_content_tmp_{config.language}.pdf"
    doc.write_pdf(str(tmp_content_pdf))
    bs.merge_cover(tmp_content_pdf, config.cover_pdf_path, out)
    tmp_content_pdf.unlink()

    # +1 physical page for the merged, WeasyPrint-external cover.
    final_total_pages = total_pages + 1
    final_anchor_pages = {marker_id: page + 1 for marker_id, page in anchor_pages.items()}

    chapter_title_url = {chapter.number: (chapter.title, chapter.canonical_url) for chapter in model.chapters}

    bs.write_pdf_pagination_metadata(
        out_pdf=out,
        pagination_out=config.pagination_output_path,
        cover_pdf_path=config.cover_pdf_path,
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

    print(f"Wrote: {out.relative_to(ROOT)} ({final_total_pages} pages)")
    for marker_id, number in chapter_markers:
        print(f"  Chapter {number:>2}: physical page {final_anchor_pages[marker_id]}")
    print(f"  Index: physical page {final_anchor_pages['marker-index']}")
    print(f"  Total physical pages: {final_total_pages}")
    print(f"Wrote: {config.pagination_output_path.relative_to(ROOT)}")
