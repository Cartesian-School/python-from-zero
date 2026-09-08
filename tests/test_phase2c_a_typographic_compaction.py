"""Tests for the M02-I07 Phase 2C-A typographic-compaction candidate.

Locks in the 19 approved print-CSS density changes (body/heading line-height
and margins, paragraph/list spacing, code-block padding, callout/exercise/
summary-box padding, TOC entry spacing, title-page and copyright-page
spacing) that make up the first typography-only compaction layer on top of
Phase 2B. This is not the final page-count target — later structural/
editorial work (Phase 2C-B, tracked separately) reaches the ~900-page goal —
this file only pins the exact CSS literals for this layer.
"""

from __future__ import annotations

import inspect
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import book_shared as bs

# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def print_css() -> str:
    return bs.build_print_css(book_title="Any Title", page_abbrev="p.")


# ---------------------------------------------------------------------------
# 1. Body typography
# ---------------------------------------------------------------------------


def test_css_body_line_height_is_126(print_css: str) -> None:
    assert (
        "body { font-family: 'DejaVu Serif', 'DejaVu Sans', 'Cartesian Noto Color Emoji', serif; "
        "font-size: 9.8pt; line-height: 1.26; color: var(--color-text-primary); }"
    ) in print_css
    assert "line-height: 1.40;" not in print_css


# ---------------------------------------------------------------------------
# 2. Heading compaction (h1/h2/h3)
# ---------------------------------------------------------------------------


def test_css_h1_is_compacted(print_css: str) -> None:
    assert "h1 { font-size: 18pt; line-height: 1.1; margin: 0 0 5.5pt; string-set: chaptitle content(); }" in print_css
    assert "h1 { font-size: 21pt; margin: 0 0 10pt; string-set: chaptitle content(); }" not in print_css


def test_css_h2_is_compacted(print_css: str) -> None:
    assert "h2 { font-size: 13pt; margin: 12pt 0 5pt; padding-top: 4pt; border-top: 1px solid var(--color-border-default); }" in print_css
    assert "h2 { font-size: 14.5pt; margin: 20pt 0 8pt;" not in print_css


def test_css_h3_is_compacted(print_css: str) -> None:
    assert "h3 { font-size: 10.5pt; margin: 8.5pt 0 3.5pt; }" in print_css
    assert "h3 { font-size: 12pt; margin: 14pt 0 6pt; }" not in print_css


# ---------------------------------------------------------------------------
# 3. Paragraph and list spacing
# ---------------------------------------------------------------------------


def test_css_paragraph_margin_is_compacted(print_css: str) -> None:
    assert "p { margin: 0 0 4.5pt; orphans: 3; widows: 3; }" in print_css
    assert "p { margin: 0 0 8pt; orphans: 3; widows: 3; }" not in print_css


def test_css_list_margin_is_compacted(print_css: str) -> None:
    assert "ul, ol { margin: 0 0 4.5pt; padding-left: 18pt; }" in print_css
    assert "ul, ol { margin: 0 0 8pt; padding-left: 18pt; }" not in print_css


# ---------------------------------------------------------------------------
# 4. Code blocks
# ---------------------------------------------------------------------------


def test_css_code_block_pre_is_compacted(print_css: str) -> None:
    assert (
        ".code-block pre { margin: 0; padding: 7pt 8.5pt; font-size: 8.8pt; "
        "line-height: 1.32; white-space: pre-wrap; word-break: break-word; }"
    ) in print_css
    assert "padding: 9pt 11pt; font-size: 8.8pt; line-height: 1.42;" not in print_css


# ---------------------------------------------------------------------------
# 5. Callouts, exercises, summary boxes
# ---------------------------------------------------------------------------


def test_css_callout_padding_is_compacted(print_css: str) -> None:
    assert (
        ".callout { border: 1px solid var(--color-border-default); border-left: 3.5pt solid "
        "var(--color-brand-blue); border-radius: var(--radius-md); padding: 4pt 10pt; margin: 5pt 0; "
        "background: var(--color-bg-surface); break-inside: avoid; }"
    ) in print_css
    assert "padding: 6pt 10pt; margin: 8pt 0; background: var(--color-bg-surface);" not in print_css


def test_css_exercise_padding_is_compacted(print_css: str) -> None:
    assert (
        ".exercise { border: 1px solid var(--color-border-default); border-radius: var(--radius-md); "
        "padding: 4pt 10pt; margin: 5pt 0; break-inside: avoid; }"
    ) in print_css
    assert ".exercise { border: 1px solid var(--color-border-default); border-radius: var(--radius-md); padding: 6pt 10pt; margin: 8pt 0;" not in print_css


def test_css_summary_box_padding_is_compacted(print_css: str) -> None:
    assert (
        ".summary-box { background: var(--color-bg-surface); border-radius: var(--radius-lg); "
        "padding: 5pt 12pt; margin: 6pt 0; break-inside: avoid; }"
    ) in print_css
    assert "padding: 8pt 12pt; margin: 10pt 0; break-inside: avoid; }" not in print_css


# ---------------------------------------------------------------------------
# 6. Table of contents
# ---------------------------------------------------------------------------


def test_css_toc_part_title_margin_is_compacted(print_css: str) -> None:
    assert (
        ".toc-part-title { font-family: 'DejaVu Sans', sans-serif; font-weight: 700; font-size: 9pt; "
        "text-transform: uppercase; letter-spacing: .05em; color: var(--color-brand-blue); "
        "margin: 6.5pt 0 3pt; }"
    ) in print_css
    assert "margin: 12pt 0 5pt; }\n.toc-part-title:first-child" not in print_css


def test_css_toc_entry_padding_and_line_height_are_compacted(print_css: str) -> None:
    assert (
        ".toc-entry {\n"
        "  display: flex; justify-content: space-between; align-items: baseline; gap: 10pt;\n"
        "  text-decoration: none; color: var(--color-text-primary); font-size: 9.5pt; padding: 1.25pt 0;\n"
        "  line-height: 1.18;\n"
        "  border-bottom: 1px dotted var(--color-border-default);\n"
        "}"
    ) in print_css
    assert "padding: 2.5pt 0;\n  border-bottom: 1px dotted var(--color-border-default);\n}" not in print_css


# ---------------------------------------------------------------------------
# 7. Title page and copyright page
# ---------------------------------------------------------------------------


def test_css_title_page_padding_top_is_compacted(print_css: str) -> None:
    assert ".title-page { page: unnumbered; break-after: page; text-align: center; padding-top: 45mm; }" in print_css
    assert "padding-top: 70mm;" not in print_css


def test_css_title_page_h1_margin_is_compacted(print_css: str) -> None:
    """Font-size deliberately unchanged at 27pt — only the margin shrinks."""
    assert ".title-page h1 { font-size: 27pt; margin: 8pt 0 4pt; string-set: none; }" in print_css
    assert "margin: 12pt 0 6pt; string-set: none;" not in print_css


def test_css_title_page_subtitle_margin_is_compacted(print_css: str) -> None:
    assert ".title-page .subtitle { font-size: 12pt; color: var(--color-text-muted); margin-bottom: 20pt; }" in print_css
    assert "margin-bottom: 36pt;" not in print_css


def test_css_title_page_author_margin_is_compacted(print_css: str) -> None:
    assert ".title-page .author { font-size: 11pt; font-weight: 700; margin-top: 30pt; }" in print_css
    assert "margin-top: 50pt;" not in print_css


def test_css_copyright_page_is_compacted(print_css: str) -> None:
    assert (
        ".copyright-page { page: unnumbered; break-before: page; break-after: page; font-size: 9pt; "
        "line-height: 1.3; color: var(--color-text-muted); padding-top: 4mm; }"
    ) in print_css
    assert "line-height: 1.4; color: var(--color-text-muted); padding-top: 8mm;" not in print_css


def test_css_copyright_page_paragraph_margin_is_compacted(print_css: str) -> None:
    assert ".copyright-page p { margin: 0 0 4pt; font-size: 9pt; }" in print_css
    assert ".copyright-page p { margin: 0 0 7pt; font-size: 9pt; }" not in print_css


def test_css_copyright_page_cp_title_margin_is_compacted(print_css: str) -> None:
    assert (
        ".copyright-page .cp-title { font-family: 'DejaVu Sans', sans-serif; font-weight: 700; "
        "color: var(--color-text-primary); font-size: 11pt; margin-bottom: 3pt; }"
    ) in print_css
    assert "margin-bottom: 4pt; }\n\n/* ---------- Table of contents" not in print_css


# ---------------------------------------------------------------------------
# 8. Unrelated Phase 2B rules stay put (spot-checks; the full contract lives
#    in tests/test_phase2b_pagination_remediation.py)
# ---------------------------------------------------------------------------


def test_css_project_hero_and_page_geometry_are_untouched(print_css: str) -> None:
    assert ".project-entry .project-hero { width: 100%; height: 45mm;" in print_css
    assert "size: 152mm 229mm;" in print_css
    assert "margin: 24mm 20mm 26mm 20mm;" in print_css


def test_css_chapter_hero_is_untouched(print_css: str) -> None:
    assert ".chapter-hero { page: opener; break-before: page; padding-top: 26pt; }" in print_css


# ---------------------------------------------------------------------------
# 9. No per-language branching; signature unchanged
# ---------------------------------------------------------------------------


def test_build_print_css_has_no_language_parameter() -> None:
    """The canonical print stylesheet builder still takes only the two
    locale LABEL parameters (book_title, page_abbrev) — no language or
    locale-conditional argument was introduced by this compaction pass."""
    params = set(inspect.signature(bs.build_print_css).parameters)
    assert params == {"book_title", "page_abbrev"}


def test_no_language_specific_pagination_branch_in_book_shared() -> None:
    source = (SCRIPTS / "book_shared.py").read_text(encoding="utf-8")
    forbidden = ('language == "ru"', 'language == "pl"', "if language ==", 'locale == "ru"', 'locale == "pl"')
    for pattern in forbidden:
        assert pattern not in source, f"found language-specific branch in book_shared.py: {pattern!r}"


def test_print_css_is_structurally_identical_for_ru_and_pl_locales() -> None:
    """Building the stylesheet with each locale's own title/abbrev must
    differ ONLY in the two injected label placeholders — every compaction
    rule (line-height, margin, padding, font-size) is byte-identical
    between the two calls, exactly as before this pass."""
    from book_pipeline.locales import get_locale

    ru_config = get_locale("ru")
    pl_config = get_locale("pl")
    ru_css = bs.build_print_css(book_title=ru_config.book_title, page_abbrev=ru_config.page_abbrev)
    pl_css = bs.build_print_css(book_title=pl_config.book_title, page_abbrev=pl_config.page_abbrev)

    ru_lines = ru_css.split("\n")
    pl_lines = pl_css.split("\n")
    assert len(ru_lines) == len(pl_lines)
    differing_lines = [(a, b) for a, b in zip(ru_lines, pl_lines) if a != b]
    for ru_line, pl_line in differing_lines:
        assert ru_config.book_title in ru_line or ru_config.page_abbrev in ru_line
        assert pl_config.book_title in pl_line or pl_config.page_abbrev in pl_line
