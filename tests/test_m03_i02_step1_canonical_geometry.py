"""Tests for M03-I02 Steps 1 and 2A: the canonical print-layout-metrics
source of truth (book_shared.PRINT_*) and the production promotion of the
approved 165x235mm mirrored-margin geometry.

Per the M03-I01 audit finding P-1, ``pagination_diagnostics._geometry_report``
previously hardcoded stale, independently-drifted production assumptions
(10.3pt/1.48) that no longer matched the print CSS's actual shipped values
(9.8pt/1.26). Step 1 fixed that by introducing one canonical,
language-independent set of constants in ``book_shared`` that both the
renderer (``build_print_css``) and the diagnostics estimator
(``_geometry_report``) read, and measured the approved geometry as a
one-off render experiment against the then-current legacy baseline. Step 2A
promoted that measured geometry directly into ``book_shared.PRINT_*`` —
production now IS 165x235mm with genuinely mirrored recto/verso margins
expressed as INNER/OUTER (not LEFT/RIGHT) — and removed the now-redundant
experiment (patching production's own rule to itself would be a no-op).

These are static/schema checks only — no ~10-15 minute/language WeasyPrint
render is paid here; the actual RU/PL production render measurement is a
separate, manually-run evidence artifact (see evidence/m03/).
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
        "PRINT_MARGIN_BOTTOM_MM",
        "PRINT_MARGIN_INNER_MM",
        "PRINT_MARGIN_OUTER_MM",
        "PRINT_BODY_FONT_SIZE_PT",
        "PRINT_BODY_LINE_HEIGHT_RATIO",
    ):
        assert f"bs.{name}" in source, f"_geometry_report should read book_shared.{name}"


# ---------------------------------------------------------------------------
# 2. Diagnostics geometry equals what the renderer actually uses
# ---------------------------------------------------------------------------


def test_geometry_report_matches_print_css_production_values() -> None:
    """The numbers _geometry_report() reports must be exactly the numbers
    build_print_css() actually emits — not merely "close" or "plausible"."""
    geometry = diag._geometry_report()
    css = bs.build_print_css(book_title="Test", page_abbrev="STR.")

    width = f"{geometry['page_width_mm']:g}"
    height = f"{geometry['page_height_mm']:g}"
    assert f"size: {width}mm {height}mm;" in css

    top = f"{geometry['margin_top_mm']:g}"
    bottom = f"{geometry['margin_bottom_mm']:g}"
    inner = f"{geometry['margin_inner_mm']:g}"
    outer = f"{geometry['margin_outer_mm']:g}"
    # Recto (:right): top / outer / bottom / inner.
    assert f"@page :right {{ margin: {top}mm {outer}mm {bottom}mm {inner}mm;" in css
    # Verso (:left): top / inner / bottom / outer.
    assert f"@page :left {{ margin: {top}mm {inner}mm {bottom}mm {outer}mm;" in css

    font_size = f"{geometry['font_size_pt']:g}"
    assert f"font-size: {font_size}pt; line-height: {geometry['line_height_ratio']:g};" in css


def test_geometry_report_values_equal_book_shared_constants() -> None:
    geometry = diag._geometry_report()
    assert geometry["page_width_mm"] == bs.PRINT_PAGE_WIDTH_MM
    assert geometry["page_height_mm"] == bs.PRINT_PAGE_HEIGHT_MM
    assert geometry["margin_top_mm"] == bs.PRINT_MARGIN_TOP_MM
    assert geometry["margin_bottom_mm"] == bs.PRINT_MARGIN_BOTTOM_MM
    assert geometry["margin_inner_mm"] == bs.PRINT_MARGIN_INNER_MM
    assert geometry["margin_outer_mm"] == bs.PRINT_MARGIN_OUTER_MM
    assert geometry["font_size_pt"] == bs.PRINT_BODY_FONT_SIZE_PT
    assert geometry["line_height_ratio"] == bs.PRINT_BODY_LINE_HEIGHT_RATIO


# ---------------------------------------------------------------------------
# 3. Step 2A: canonical geometry is now PRODUCTION, not an experiment
# ---------------------------------------------------------------------------


def test_production_geometry_is_the_approved_canonical_165x235_mirrored() -> None:
    """Step 2A promoted the Product-Owner-approved geometry directly into
    production. book_shared.PRINT_* must equal the approved values — the
    legacy 152x229mm/uniform-margin baseline must be gone, not merely
    reachable via an opt-in experiment."""
    assert bs.PRINT_PAGE_WIDTH_MM == 165.0
    assert bs.PRINT_PAGE_HEIGHT_MM == 235.0
    assert bs.PRINT_MARGIN_TOP_MM == 18.0
    assert bs.PRINT_MARGIN_BOTTOM_MM == 20.0
    assert bs.PRINT_MARGIN_INNER_MM == 20.0
    assert bs.PRINT_MARGIN_OUTER_MM == 15.0
    # Body typography is explicitly NOT part of this promotion.
    assert bs.PRINT_BODY_FONT_SIZE_PT == 9.8
    assert bs.PRINT_BODY_LINE_HEIGHT_RATIO == 1.26


def test_no_stale_fixed_left_right_margin_abstraction_remains() -> None:
    """The pre-Step-2A PRINT_MARGIN_LEFT_MM/PRINT_MARGIN_RIGHT_MM constants
    encoded the wrong abstraction for a mirrored, physically-bound book (a
    uniform left/right pair cannot express "the margin near the spine").
    They must no longer exist at all — not merely be unused."""
    assert not hasattr(bs, "PRINT_MARGIN_LEFT_MM")
    assert not hasattr(bs, "PRINT_MARGIN_RIGHT_MM")


def test_obsolete_geometry_experiment_was_removed() -> None:
    """Once production geometry IS the approved 165x235mm mirrored layout,
    an experiment that patches production's own @page rule to itself would
    be a no-op comparison — it must be gone, not left behind as dead
    weight or (worse) silently comparing production against production."""
    assert "canonical_165x235_mirrored_geometry" not in diag.RENDER_EXPERIMENTS


def test_left_and_right_pages_are_genuinely_mirrored_in_production_css() -> None:
    """Applying no patch at all — this IS production now — must yield the
    exact Product-Owner-approved 165x235mm trim with genuinely MIRRORED
    recto/verso margins (not a uniform margin re-applied to both sides)."""
    css = bs.build_print_css(book_title="Test", page_abbrev="STR.")

    assert "size: 165mm 235mm;" in css

    left_margin = re.search(r"@page :left \{ margin: ([^;]+);", css)
    assert left_margin is not None
    assert left_margin.group(1) == "18mm 20mm 20mm 15mm"

    right_margin = re.search(r"@page :right \{ margin: ([^;]+);", css)
    assert right_margin is not None
    assert right_margin.group(1) == "18mm 15mm 20mm 20mm"

    # Genuinely mirrored, not uniform: left/right margin values must differ
    # between the two page sides.
    assert left_margin.group(1) != right_margin.group(1)


# ---------------------------------------------------------------------------
# 4. Real structural render experiments survive the promotion untouched
# ---------------------------------------------------------------------------


_EXPECTED_STRUCTURAL_EXPERIMENTS = {
    "no_project_forced_break",
    "no_break_inside_avoid",
    "no_callout_avoid",
    "no_code_block_avoid",
}


def test_real_structural_experiments_are_preserved_as_measurement_tools() -> None:
    """Step 2A must not implement (or remove) any Step 2B structural lever —
    these four remain declared, real, opt-in measurement tools only."""
    assert set(diag.RENDER_EXPERIMENTS) == _EXPECTED_STRUCTURAL_EXPERIMENTS


# ---------------------------------------------------------------------------
# 5. No language-specific CSS, geometry, or publisher branch was introduced
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


def test_ru_and_pl_produce_the_same_production_geometry() -> None:
    """RU and PL must use the exact same production @page rule — geometry
    is a format-adapter concern, never a locale concern."""
    from book_pipeline.locales import get_locale

    ru_config = get_locale("ru")
    pl_config = get_locale("pl")
    ru_css = bs.build_print_css(book_title=ru_config.book_title, page_abbrev=ru_config.page_abbrev)
    pl_css = bs.build_print_css(book_title=pl_config.book_title, page_abbrev=pl_config.page_abbrev)

    ru_page_rule = re.search(r"@page \{.*?\n\}", ru_css, re.DOTALL).group(0)
    pl_page_rule = re.search(r"@page \{.*?\n\}", pl_css, re.DOTALL).group(0)
    assert ru_page_rule == pl_page_rule

    for language, css in (("ru", ru_css), ("pl", pl_css)):
        assert "size: 165mm 235mm;" in css, f"[{language}] production trim missing"


def test_no_new_publisher_script_created_for_the_promotion() -> None:
    """Guard against the prohibited pattern this task explicitly called
    out: a parallel PDF builder or per-locale CSS file introduced while
    promoting geometry to production."""
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


def test_geometry_report_schema_uses_inner_outer_not_left_right() -> None:
    geometry = diag._geometry_report()
    assert set(geometry) == {
        "page_width_mm", "page_height_mm",
        "margin_top_mm", "margin_bottom_mm", "margin_inner_mm", "margin_outer_mm",
        "text_width_mm", "text_height_mm", "text_area_pct_of_physical_page",
        "font_size_pt", "line_height_ratio", "line_height_pt", "estimated_lines_per_page",
    }


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
