"""Tests for M03-I02 Step 1: the canonical print-layout-metrics source of
truth (book_shared.PRINT_*) and the approved 165x235mm mirrored-margin
geometry render experiment.

Per the M03-I01 audit finding P-1, ``pagination_diagnostics._geometry_report``
previously hardcoded stale, independently-drifted production assumptions
(10.3pt/1.48) that no longer matched the print CSS's actual shipped values
(9.8pt/1.26). These tests pin the fix: one canonical, language-independent
set of constants in ``book_shared`` that both the renderer
(``build_print_css``) and the diagnostics estimator (``_geometry_report``)
read, plus the new controlled geometry experiment added to the existing
render-experiment harness. Like ``test_pagination_diagnostics.py``, these are
static/schema checks only — no ~10-15 minute/language WeasyPrint render is
paid here; the actual RU/PL render measurement is a separate, manually-run
evidence artifact (see evidence/m03/).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import book_shared as bs
from book_pipeline import pagination_diagnostics as diag

# ---------------------------------------------------------------------------
# 1. The stale 10.3pt/1.48 diagnostics assumption is gone
# ---------------------------------------------------------------------------


def test_geometry_report_no_longer_hardcodes_stale_typography() -> None:
    """The pre-M03-I02 defect: _geometry_report() independently assigned
    ``font_size_pt, line_height_ratio = 10.3, 1.48`` — pre-Phase-2B values
    that had silently drifted from the print CSS's actual shipped 9.8pt/1.26.
    Walk the function's AST (excluding its docstring, which legitimately
    narrates this history for future readers) for numeric constants, rather
    than a brittle substring ban."""
    import ast
    import inspect

    source = inspect.getsource(diag._geometry_report)
    tree = ast.parse(source)
    func = tree.body[0]
    body_without_docstring = func.body[1:] if ast.get_docstring(func) else func.body
    numeric_constants = {
        node.value
        for stmt in body_without_docstring
        for node in ast.walk(stmt)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float))
    }
    assert 10.3 not in numeric_constants, "stale pre-Phase-2B font_size_pt literal still assigned"
    assert 1.48 not in numeric_constants, "stale pre-Phase-2B line_height_ratio literal still assigned"


def test_geometry_report_reads_book_shared_constants_not_local_literals() -> None:
    """_geometry_report() must not re-hardcode its own copy of the page/
    margin/typography numbers — it must read book_shared's PRINT_* module
    constants, the single source of truth build_print_css() also reads."""
    source = (SCRIPTS / "book_pipeline" / "pagination_diagnostics.py").read_text(encoding="utf-8")
    for name in (
        "PRINT_PAGE_WIDTH_MM",
        "PRINT_PAGE_HEIGHT_MM",
        "PRINT_MARGIN_TOP_MM",
        "PRINT_MARGIN_RIGHT_MM",
        "PRINT_MARGIN_BOTTOM_MM",
        "PRINT_MARGIN_LEFT_MM",
        "PRINT_BODY_FONT_SIZE_PT",
        "PRINT_BODY_LINE_HEIGHT_RATIO",
    ):
        assert f"bs.{name}" in source, f"_geometry_report should read book_shared.{name}"


# ---------------------------------------------------------------------------
# 2. Diagnostics geometry now equals what the renderer actually uses
# ---------------------------------------------------------------------------


def test_geometry_report_matches_print_css_current_baseline() -> None:
    """The numbers _geometry_report() reports must be exactly the numbers
    build_print_css() actually emits — not merely "close" or "plausible"."""
    geometry = diag._geometry_report()
    css = bs.build_print_css(book_title="Test", page_abbrev="STR.")

    width = f"{geometry['page_width_mm']:g}"
    height = f"{geometry['page_height_mm']:g}"
    assert f"size: {width}mm {height}mm;" in css

    top = f"{geometry['margin_top_mm']:g}"
    right = f"{geometry['margin_right_mm']:g}"
    bottom = f"{geometry['margin_bottom_mm']:g}"
    left = f"{geometry['margin_left_mm']:g}"
    assert f"margin: {top}mm {right}mm {bottom}mm {left}mm;" in css

    font_size = f"{geometry['font_size_pt']:g}"
    assert f"font-size: {font_size}pt; line-height: {geometry['line_height_ratio']:g};" in css


def test_geometry_report_values_equal_book_shared_constants() -> None:
    geometry = diag._geometry_report()
    assert geometry["page_width_mm"] == bs.PRINT_PAGE_WIDTH_MM
    assert geometry["page_height_mm"] == bs.PRINT_PAGE_HEIGHT_MM
    assert geometry["margin_top_mm"] == bs.PRINT_MARGIN_TOP_MM
    assert geometry["margin_right_mm"] == bs.PRINT_MARGIN_RIGHT_MM
    assert geometry["margin_bottom_mm"] == bs.PRINT_MARGIN_BOTTOM_MM
    assert geometry["margin_left_mm"] == bs.PRINT_MARGIN_LEFT_MM
    assert geometry["font_size_pt"] == bs.PRINT_BODY_FONT_SIZE_PT
    assert geometry["line_height_ratio"] == bs.PRINT_BODY_LINE_HEIGHT_RATIO


def test_current_production_geometry_is_unchanged_this_round() -> None:
    """M03-I02 Step 1 measures the approved 165x235mm geometry as a
    controlled EXPERIMENT only; it must not have been promoted to
    production in this round. Pins the legacy baseline the M03-I01 audit
    recorded (152x229mm, 24/20/26/20mm margins, 9.8pt/1.26 body) as still
    the live production constants."""
    assert bs.PRINT_PAGE_WIDTH_MM == 152.0
    assert bs.PRINT_PAGE_HEIGHT_MM == 229.0
    assert bs.PRINT_MARGIN_TOP_MM == 24.0
    assert bs.PRINT_MARGIN_RIGHT_MM == 20.0
    assert bs.PRINT_MARGIN_BOTTOM_MM == 26.0
    assert bs.PRINT_MARGIN_LEFT_MM == 20.0
    assert bs.PRINT_BODY_FONT_SIZE_PT == 9.8
    assert bs.PRINT_BODY_LINE_HEIGHT_RATIO == 1.26


# ---------------------------------------------------------------------------
# 3 & 4. The canonical geometry experiment is locale-neutral and RU/PL route
# through the exact same implementation (no per-language experiment fork)
# ---------------------------------------------------------------------------


def test_canonical_geometry_experiment_is_declared_once_not_per_locale() -> None:
    """RENDER_EXPERIMENTS is one shared dict, not a per-language mapping —
    there is no 'canonical_165x235_mirrored_geometry_ru' /
    '..._pl' split, and the same run_render_experiments() call is used
    for both languages (see test_pagination_diagnostics.py's existing
    RU/PL parity tests for the pre-existing experiments)."""
    assert "canonical_165x235_mirrored_geometry" in diag.RENDER_EXPERIMENTS
    for name in diag.RENDER_EXPERIMENTS:
        assert not name.endswith(("_ru", "_pl")), f"locale-specific experiment name found: {name}"


def test_canonical_geometry_patch_holds_typography_constant() -> None:
    """The experiment must isolate geometry only: it must not touch the
    body/heading font-size or line-height rules."""
    patches = diag.RENDER_EXPERIMENTS["canonical_165x235_mirrored_geometry"]
    for old, new in patches:
        assert "font-size" not in old and "font-size" not in new
        assert "line-height" not in old and "line-height" not in new


def test_canonical_geometry_patch_targets_real_css_for_both_locales() -> None:
    """The declared patch's old-side text must actually be present in the
    print CSS generated for both RU and PL locale configs (same shared
    stylesheet, per book_shared.build_print_css's own contract)."""
    from book_pipeline.locales import get_locale

    patches = diag.RENDER_EXPERIMENTS["canonical_165x235_mirrored_geometry"]
    for language in ("ru", "pl"):
        config = get_locale(language)
        css = bs.build_print_css(book_title=config.book_title, page_abbrev=config.page_abbrev)
        for old, _new in patches:
            assert old in css, f"[{language}] geometry patch target not found: {old[:80]!r}"


def test_canonical_geometry_experiment_produces_mirrored_margins() -> None:
    """Applying the patch must yield the exact Product-Owner-approved
    165x235mm trim with genuinely MIRRORED recto/verso margins (not a
    uniform margin re-applied to both page sides)."""
    css = bs.build_print_css(book_title="Test", page_abbrev="STR.")
    for old, new in diag.RENDER_EXPERIMENTS["canonical_165x235_mirrored_geometry"]:
        assert old in css
        css = css.replace(old, new, 1)

    assert "size: 165mm 235mm;" in css
    # Verso (left): inner margin (right side, near spine) 20mm, outer (left) 15mm.
    left_margin = re.search(r"@page :left \{ margin: ([^;]+);", css)
    assert left_margin is not None
    assert left_margin.group(1) == "18mm 20mm 20mm 15mm"
    # Recto (right): inner margin (left side, near spine) 20mm, outer (right) 15mm.
    right_margin = re.search(r"@page :right \{ margin: ([^;]+);", css)
    assert right_margin is not None
    assert right_margin.group(1) == "18mm 15mm 20mm 20mm"
    # Genuinely mirrored, not uniform: left/right margin values must differ
    # between the two page sides.
    assert left_margin.group(1) != right_margin.group(1)


# ---------------------------------------------------------------------------
# 5. No language-specific CSS or publisher branch was introduced
# ---------------------------------------------------------------------------


def test_no_language_specific_branch_introduced_in_book_shared_or_diagnostics() -> None:
    forbidden_patterns = ('language == "ru"', 'language == "pl"', "language=='ru'", "language=='pl'")
    for relative_path in ("book_shared.py", "book_pipeline/pagination_diagnostics.py"):
        source = (SCRIPTS / relative_path).read_text(encoding="utf-8")
        for pattern in forbidden_patterns:
            assert pattern not in source, f"{relative_path}: found language-specific branch: {pattern!r}"


def test_build_print_css_still_takes_no_language_parameter() -> None:
    import inspect

    params = set(inspect.signature(bs.build_print_css).parameters)
    assert params == {"book_title", "page_abbrev"}


def test_no_new_publisher_script_created_for_the_experiment() -> None:
    """Guard against the prohibited pattern this task explicitly called
    out: a parallel experimental book builder (build_pdf_165.py,
    build_book_experiment.py, book_ru_165.css, book_pl_165.css, ...). The
    geometry experiment must live only inside the existing diagnostics
    render-experiment framework."""
    forbidden_names = (
        "build_pdf_165.py",
        "build_book_experiment.py",
        "book_ru_165.css",
        "book_pl_165.css",
        "build_pdf_165_pl.py",
    )
    existing = {p.name for p in SCRIPTS.rglob("*") if p.is_file()}
    for forbidden in forbidden_names:
        assert forbidden not in existing, f"prohibited parallel-publisher file found: {forbidden}"


# ---------------------------------------------------------------------------
# Schema sanity for the fast artifact-analysis geometry field
# ---------------------------------------------------------------------------


def test_geometry_report_schema_unchanged() -> None:
    geometry = diag._geometry_report()
    assert set(geometry) == {
        "page_width_mm", "page_height_mm",
        "margin_top_mm", "margin_right_mm", "margin_bottom_mm", "margin_left_mm",
        "text_width_mm", "text_height_mm", "text_area_pct_of_physical_page",
        "font_size_pt", "line_height_ratio", "line_height_pt", "estimated_lines_per_page",
    }


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
