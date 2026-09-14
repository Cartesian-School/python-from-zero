"""Tests for the canonical PDF pagination diagnostics (M02-I07 Phase 2A).

These exercise the FAST artifact-analysis path only (reads the already-built
PDF + pagination sidecar; no re-rendering) — the slow, opt-in
``render_experiments`` path is a manual/CI-evidence tool, not something a
routine test run should pay ~10-15 minutes per language for. Assertions are
all objective (page counts, schema keys, threshold arithmetic) — none depend
on subjective visual judgment, per the task's own requirement.
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
from book_pipeline import SUPPORTED_LANGUAGES
from book_pipeline import pagination_diagnostics as diag
from book_pipeline.locales import get_locale

_REQUIRED_PDFS = {
    language: get_locale(language).pdf_output_path for language in SUPPORTED_LANGUAGES
}
_missing = {lang: path for lang, path in _REQUIRED_PDFS.items() if not path.is_file()}
pytestmark = pytest.mark.skipif(
    bool(_missing), reason=f"required PDF artifact(s) missing: {_missing}"
)


@pytest.fixture(scope="module")
def report_ru() -> dict:
    return diag.analyze("ru")


@pytest.fixture(scope="module")
def report_pl() -> dict:
    return diag.analyze("pl")


@pytest.fixture(scope="module", params=["ru", "pl"])
def report(request, report_ru, report_pl) -> dict:
    return report_ru if request.param == "ru" else report_pl


# ---------------------------------------------------------------------------
# RU and PL use the same diagnostics implementation; no locale-specific fork
# ---------------------------------------------------------------------------


def test_ru_and_pl_use_the_same_analyze_function() -> None:
    """There is exactly one ``analyze`` callable; language is a plain
    argument to it, not a dispatch key to a per-locale implementation."""
    import book_pipeline.pagination_diagnostics as mod1
    import book_pipeline.pagination_diagnostics as mod2

    assert mod1.analyze is mod2.analyze
    assert inspect.signature(diag.analyze).parameters.keys() >= {"language"}


def test_no_locale_specific_analysis_fork_exists() -> None:
    """Guard against a future PR silently reintroducing an ``if language ==
    "ru"``-shaped fork into the diagnostics module (the same architectural
    violation M02-I06 removed from the build pipeline itself)."""
    source = (SCRIPTS / "book_pipeline" / "pagination_diagnostics.py").read_text(encoding="utf-8")
    forbidden_patterns = ('language == "ru"', 'language == "pl"', "language=='ru'", "language=='pl'")
    for pattern in forbidden_patterns:
        assert pattern not in source, f"found language-specific branch: {pattern!r}"


def test_ru_and_pl_reports_share_identical_schema(report_ru, report_pl) -> None:
    assert set(report_ru) == set(report_pl)
    assert set(report_ru["totals"]) == set(report_pl["totals"])
    assert set(report_ru["thresholds"]) == set(report_pl["thresholds"])
    assert report_ru["thresholds"] == report_pl["thresholds"] == diag.THRESHOLDS


# ---------------------------------------------------------------------------
# Blank / near-empty classification is deterministic
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "word_count,expected_blank,expected_near_empty,expected_very_sparse,expected_sparse",
    [
        (0, True, True, True, True),
        (1, False, True, True, True),
        (24, False, True, True, True),
        (25, False, False, True, True),
        (49, False, False, True, True),
        (50, False, False, False, True),
        (99, False, False, False, True),
        (100, False, False, False, False),
        (500, False, False, False, False),
    ],
)
def test_blank_and_near_empty_thresholds_are_deterministic(
    word_count, expected_blank, expected_near_empty, expected_very_sparse, expected_sparse
) -> None:
    page = diag.PageRecord(
        number=1, category="chapter_content", chapter_number=1, project_slug=None,
        word_count=word_count, char_count=word_count * 5, body_word_count=word_count,
    )
    assert page.is_blank is expected_blank
    assert page.is_near_empty is expected_near_empty
    assert page.is_very_sparse is expected_very_sparse
    assert page.is_sparse is expected_sparse


@pytest.mark.parametrize("body_word_count,expected", [(0, True), (1, False)])
def test_body_effectively_empty_threshold_is_deterministic(body_word_count, expected) -> None:
    """is_body_effectively_empty is keyed on body_word_count (post chrome-
    strip), independent of raw word_count — a page with plenty of raw
    (chrome-inclusive) words can still be body-effectively-empty, and vice
    versa is impossible by construction (stripping only ever removes text)."""
    page = diag.PageRecord(
        number=1, category="chapter_content", chapter_number=1, project_slug=None,
        word_count=50, char_count=250, body_word_count=body_word_count,
    )
    assert page.is_body_effectively_empty is expected


@pytest.mark.parametrize(
    "text,page_number,book_title,expected",
    [
        ("КАК ПОЛУЧИТЬ МАКСИМУМ ОТ ЭТОЙ КНИГИ\n43", 43, "Python с нуля", "КАК ПОЛУЧИТЬ МАКСИМУМ ОТ ЭТОЙ КНИГИ"),
        ("Запустите локально: python paint_app.py\nPYTHON С НУЛЯ\n2496", 2496, "Python с нуля", "Запустите локально: python paint_app.py"),
        ("body only, no chrome", 7, "Python с нуля", "body only, no chrome"),
    ],
)
def test_strip_known_page_chrome_is_deterministic(text, page_number, book_title, expected) -> None:
    assert diag._strip_known_page_chrome(text, page_number=page_number, book_title=book_title) == expected


def test_classification_is_deterministic_across_repeated_runs(report_ru) -> None:
    second_run = diag.analyze("ru")
    assert second_run["category_totals"] == report_ru["category_totals"]
    assert second_run["totals"] == report_ru["totals"]
    assert [p["category"] for p in second_run["pages"]] == [p["category"] for p in report_ru["pages"]]


# ---------------------------------------------------------------------------
# Chapter mapping correctness
# ---------------------------------------------------------------------------


def test_every_physical_page_is_classified_exactly_once(report) -> None:
    numbers = [p["number"] for p in report["pages"]]
    assert numbers == list(range(1, report["totals"]["total_pages"] + 1))


def test_chapter_mapping_matches_pagination_sidecar(report) -> None:
    assert len(report["chapters"]) == 24
    assert [c["number"] for c in report["chapters"]] == list(range(1, 25))
    pages_by_number = {p["number"]: p for p in report["pages"]}
    for chapter in report["chapters"]:
        expected_page_count = chapter["end_page"] - chapter["start_page"] + 1
        assert chapter["page_count"] == expected_page_count
        chapter_pages = [
            pages_by_number[n] for n in range(chapter["start_page"], chapter["end_page"] + 1)
        ]
        assert all(p["chapter_number"] == chapter["number"] for p in chapter_pages)
        assert all(p["category"] in ("chapter_opener", "chapter_content") for p in chapter_pages)
        # exactly the first page(s) of the range are the opener, per pdf_adapter's
        # own opener/content split — never a content page ahead of an opener page.
        categories = [p["category"] for p in chapter_pages]
        first_content_index = next(
            (i for i, c in enumerate(categories) if c == "chapter_content"), len(categories)
        )
        assert all(c == "chapter_opener" for c in categories[:first_content_index])
        assert all(c == "chapter_content" for c in categories[first_content_index:])


def test_category_totals_sum_to_total_pages(report) -> None:
    assert sum(report["category_totals"].values()) == report["totals"]["total_pages"]


def test_no_raw_zero_word_pages_found_but_thresholds_still_meaningful(report) -> None:
    """Documented, evidence-backed corpus fact (see the M02-I07 report):
    zero pages have zero words under RAW pypdf extraction in either book —
    this does NOT by itself prove no page is visually/body empty, since raw
    extraction includes running headers/folios (see PageRecord.is_blank's
    docstring and body_effectively_empty_pages for the partial, stricter
    secondary signal). The near-empty/very-sparse thresholds still classify
    a substantial minority of pages; this test pins both findings so a
    future content/layout change that reintroduces (or removes) them is
    visible in the diff."""
    assert report["totals"]["blank_pages"] == 0
    assert report["totals"]["near_empty_pages"] > 0
    assert report["totals"]["body_effectively_empty_pages"] >= 0


# ---------------------------------------------------------------------------
# Unsupported language fails explicitly
# ---------------------------------------------------------------------------


def test_unsupported_language_fails_explicitly() -> None:
    with pytest.raises(ValueError, match="unsupported language"):
        diag.analyze("xx-invalid")


def test_missing_artifact_fails_explicitly(tmp_path, monkeypatch) -> None:
    import dataclasses

    from book_pipeline import locales as locales_module

    ru_config = get_locale("ru")
    fake_config = dataclasses.replace(ru_config, pdf_output_path=tmp_path / "missing.pdf")
    monkeypatch.setitem(locales_module._REGISTRY, "ru", fake_config)
    with pytest.raises(FileNotFoundError, match="missing.pdf"):
        diag.analyze("ru")


# ---------------------------------------------------------------------------
# Metrics schema stability
# ---------------------------------------------------------------------------


_EXPECTED_TOP_LEVEL_KEYS = {
    "schema_version", "language", "pdf_path", "pdf_sha256", "pagination_source_path",
    "thresholds", "totals", "category_totals", "category_word_stats", "chapters",
    "recto_policy", "forced_page_breaks", "break_inside_avoid", "components", "geometry", "pages",
}
_EXPECTED_TOTALS_KEYS = {
    "total_pages", "blank_pages", "body_effectively_empty_pages", "near_empty_pages",
    "pages_under_25_words", "pages_under_50_words", "pages_under_100_words", "pages_under_150_words",
    "mean_words_per_page", "median_words_per_page", "p10_words_per_page",
    "p25_words_per_page", "p75_words_per_page", "p90_words_per_page",
    "max_words_per_page", "mean_characters_per_page", "median_characters_per_page",
}


def test_metrics_schema_is_stable(report) -> None:
    assert set(report) == _EXPECTED_TOP_LEVEL_KEYS
    assert set(report["totals"]) == _EXPECTED_TOTALS_KEYS
    assert report["schema_version"] == diag.SCHEMA_VERSION


def test_page_record_schema_is_stable(report) -> None:
    expected_page_keys = {
        "number", "category", "chapter_number", "project_slug",
        "word_count", "char_count", "body_word_count",
        "is_blank", "is_near_empty", "is_very_sparse", "is_sparse", "is_body_effectively_empty",
    }
    assert set(report["pages"][0]) == expected_page_keys


def test_chapter_record_schema_is_stable(report) -> None:
    expected_chapter_keys = {
        "number", "title", "start_page", "end_page", "page_count", "opener_pages",
        "opener_words", "total_words", "mean_words_per_page", "blank_pages",
        "near_empty_pages", "very_sparse_pages",
    }
    assert set(report["chapters"][0]) == expected_chapter_keys


# ---------------------------------------------------------------------------
# Render-experiment schema (declared names + computed fields), WITHOUT
# paying the ~10-15 minute/language cost of real WeasyPrint rendering.
# ---------------------------------------------------------------------------


_EXPECTED_RENDER_EXPERIMENT_NAMES = {
    "no_project_forced_break",
    "no_break_inside_avoid",
    "no_callout_avoid",
    "no_code_block_avoid",
}


def test_declared_render_experiments_are_well_formed() -> None:
    """Static check (no rendering): every declared experiment has at least
    one (old, new) CSS patch pair, each a distinct, non-empty string pair —
    catches an experiment declared but left empty/no-op."""
    assert set(diag.RENDER_EXPERIMENTS) == _EXPECTED_RENDER_EXPERIMENT_NAMES
    for name, patches in diag.RENDER_EXPERIMENTS.items():
        assert isinstance(patches, list) and patches, f"{name} declares no patches"
        for old, new in patches:
            assert isinstance(old, str) and old
            assert isinstance(new, str) and new
            assert old != new, f"{name}: patch is a no-op ({old!r})"


def test_declared_render_experiment_patches_target_real_css(report_ru) -> None:
    """Every declared patch's ``old`` substring must actually be present in
    the canonical print stylesheet — a stale/renamed CSS rule would
    otherwise fail silently until someone runs the slow --render-experiments
    path by hand (see run_render_experiments' own RuntimeError guard, which
    this test exercises the precondition for without paying its cost)."""
    css = bs.build_print_css(book_title=get_locale("ru").book_title, page_abbrev=get_locale("ru").page_abbrev)
    for name, patches in diag.RENDER_EXPERIMENTS.items():
        for old, _new in patches:
            assert old in css, f"{name}: patch target not found in current CSS: {old[:60]!r}"


def test_run_render_experiments_produces_expected_schema(monkeypatch) -> None:
    """Exercises run_render_experiments' REAL control flow (patch
    application, build_full_html for every variant, delta/pct computation)
    with only the expensive WeasyPrint render step faked out — so this
    verifies the exact fields the task requires (weasyprint_pages,
    page_delta_vs_baseline, page_delta_pct_vs_baseline, and that every
    declared experiment name appears in each) without a ~10-15 minute cost.
    """
    import sys as _sys
    import types

    from book_pipeline.locales import get_locale as _get_locale
    from book_pipeline.model import CanonicalBookLoader

    class _FakeDoc:
        def __init__(self, page_count: int) -> None:
            self.pages = list(range(page_count))

    class _FakeHTML:
        def __init__(self, *, string: str, base_url: str) -> None:
            # Deterministic pseudo page-count that varies with the patched
            # CSS's length, so different variants produce different (fake)
            # page counts and the delta/pct arithmetic is exercised for real.
            self._page_count = 1000 + (len(string) % 97)

        def render(self):
            return _FakeDoc(self._page_count)

    monkeypatch.setitem(_sys.modules, "weasyprint", types.SimpleNamespace(HTML=_FakeHTML))

    config = _get_locale("ru")
    model = CanonicalBookLoader.load(config)
    result = diag.run_render_experiments(config, model)

    assert set(result) == {"note", "weasyprint_pages", "page_delta_vs_baseline", "page_delta_pct_vs_baseline"}
    assert set(result["weasyprint_pages"]) == {"baseline", *_EXPECTED_RENDER_EXPERIMENT_NAMES}
    assert set(result["page_delta_vs_baseline"]) == _EXPECTED_RENDER_EXPERIMENT_NAMES
    assert set(result["page_delta_pct_vs_baseline"]) == _EXPECTED_RENDER_EXPERIMENT_NAMES

    baseline = result["weasyprint_pages"]["baseline"]
    for name in _EXPECTED_RENDER_EXPERIMENT_NAMES:
        expected_delta = result["weasyprint_pages"][name] - baseline
        assert result["page_delta_vs_baseline"][name] == expected_delta
        assert result["page_delta_pct_vs_baseline"][name] == pytest.approx(100 * expected_delta / baseline, abs=0.01)
