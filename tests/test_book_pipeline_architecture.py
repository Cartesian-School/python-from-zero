"""Architecture conformance tests for the canonical book-build pipeline.

Guards docs/contracts/BOOK-BUILD-PIPELINE-CONTRACT.md's binding invariant:
"There MUST be exactly one canonical book-build pipeline for all language
editions and all supported publication formats. The selected language is
only an input parameter. The selected publication format is only an output
parameter." These tests exercise the architecture itself (parameter
plumbing, adapter wiring, content-model sharing, compatibility-wrapper
thinness) rather than rendered PDF/EPUB byte content, which
tests/test_license_consistency.py and scripts/validate_book.py already
cover.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import chapter_metadata
from book_pipeline import (
    SUPPORTED_FORMATS,
    SUPPORTED_LANGUAGES,
    build_book,
    epub_adapter,
    get_locale,
    pdf_adapter,
)
from book_pipeline import pipeline as book_pipeline_module
from book_pipeline.model import CanonicalBookLoader

WRAPPER_SCRIPTS = {
    ("ru", "pdf"): SCRIPTS / "build_pdf.py",
    ("ru", "epub"): SCRIPTS / "build_epub.py",
    ("pl", "pdf"): SCRIPTS / "build_pdf_pl.py",
    ("pl", "epub"): SCRIPTS / "build_epub_pl.py",
}

# Markers that would indicate a compatibility wrapper has grown independent
# publishing logic instead of delegating to the canonical pipeline (contract
# section 2: "Thin wrappers MAY exist only when they delegate to the same
# canonical pipeline without introducing independent publishing behavior").
_FORBIDDEN_LOGIC_MARKERS = (
    "def build_full_html",
    "def build_item",
    "def build_project_item",
    "def chapter_pages",
    "def extract_article",
    "def extract_opener",
    "def extract_project",
    "class EpubBook",
    "EpubBook()",
    "HTML(string=",
    "WeasyPrint",
    "write_epub(",
    "merge_cover(",
    "PAGES",
)


# ---------------------------------------------------------------------------
# 1 & 4: one canonical pipeline; RU and PL use the same pipeline implementation
# ---------------------------------------------------------------------------


def test_single_canonical_pipeline_implementation() -> None:
    """The adapter used for a given format is the same function object no
    matter which language is requested — there is exactly one PDF
    implementation and exactly one EPUB implementation, not one per locale."""
    assert book_pipeline_module._ADAPTERS["pdf"] is pdf_adapter.build
    assert book_pipeline_module._ADAPTERS["epub"] is epub_adapter.build
    # Only one canonical build_book callable exists at all.
    from book_pipeline.pipeline import build_book as pipeline_build_book

    assert pipeline_build_book is build_book


def test_ru_and_pl_route_through_the_identical_adapter_functions(monkeypatch) -> None:
    calls = []

    def fake_load(config):
        calls.append(("load", config.language))
        return object()

    def fake_pdf_build(model, config):
        calls.append(("pdf", config.language))

    def fake_epub_build(model, config):
        calls.append(("epub", config.language))

    monkeypatch.setattr(CanonicalBookLoader, "load", staticmethod(fake_load))
    monkeypatch.setitem(book_pipeline_module._ADAPTERS, "pdf", fake_pdf_build)
    monkeypatch.setitem(book_pipeline_module._ADAPTERS, "epub", fake_epub_build)

    for language in ("ru", "pl"):
        for output_format in ("pdf", "epub"):
            build_book(language=language, output_format=output_format)

    assert calls == [
        ("load", "ru"), ("pdf", "ru"),
        ("load", "ru"), ("epub", "ru"),
        ("load", "pl"), ("pdf", "pl"),
        ("load", "pl"), ("epub", "pl"),
    ]


# ---------------------------------------------------------------------------
# 2 & 3: language and format are input/output parameters
# ---------------------------------------------------------------------------


def test_language_is_an_input_parameter(monkeypatch) -> None:
    seen_configs = []
    monkeypatch.setattr(CanonicalBookLoader, "load", staticmethod(lambda config: seen_configs.append(config) or object()))
    monkeypatch.setitem(book_pipeline_module._ADAPTERS, "pdf", lambda model, config: None)

    build_book(language="ru", output_format="pdf")
    build_book(language="pl", output_format="pdf")

    assert [config.language for config in seen_configs] == ["ru", "pl"]
    assert seen_configs[0] is get_locale("ru")
    assert seen_configs[1] is get_locale("pl")


def test_format_is_an_output_parameter(monkeypatch) -> None:
    monkeypatch.setattr(CanonicalBookLoader, "load", staticmethod(lambda config: object()))
    invoked = []

    def _make_adapter(fmt):
        return lambda model, config: invoked.append(fmt)

    for output_format in SUPPORTED_FORMATS:
        monkeypatch.setitem(book_pipeline_module._ADAPTERS, output_format, _make_adapter(output_format))

    for output_format in SUPPORTED_FORMATS:
        build_book(language="ru", output_format=output_format)

    assert invoked == list(SUPPORTED_FORMATS)


# ---------------------------------------------------------------------------
# 5: PDF and EPUB adapters receive the same canonical content model
# ---------------------------------------------------------------------------


def test_pdf_and_epub_adapters_receive_the_same_canonical_model(monkeypatch) -> None:
    sentinel_model = object()
    monkeypatch.setattr(CanonicalBookLoader, "load", staticmethod(lambda config: sentinel_model))
    captured: dict[str, object] = {}
    monkeypatch.setitem(book_pipeline_module._ADAPTERS, "pdf", lambda model, config: captured.__setitem__("pdf", model))
    monkeypatch.setitem(book_pipeline_module._ADAPTERS, "epub", lambda model, config: captured.__setitem__("epub", model))

    build_book(language="ru", output_format="pdf")
    build_book(language="ru", output_format="epub")

    assert captured["pdf"] is sentinel_model
    assert captured["epub"] is sentinel_model


# ---------------------------------------------------------------------------
# 6: language-specific builder forks contain no independent logic
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("language,output_format", sorted(WRAPPER_SCRIPTS))
def test_compatibility_wrapper_is_thin(language: str, output_format: str) -> None:
    path = WRAPPER_SCRIPTS[(language, output_format)]
    source = path.read_text(encoding="utf-8")

    assert f'build_book(language="{language}", output_format="{output_format}")' in source

    for marker in _FORBIDDEN_LOGIC_MARKERS:
        assert marker not in source, f"{path.name} contains independent publishing logic: {marker!r}"

    # A generous ceiling on a "thin" wrapper — the real builders these
    # replaced were 200-335 lines of independent logic each.
    assert len(source.splitlines()) < 40, f"{path.name} looks too large to be a thin wrapper"


# ---------------------------------------------------------------------------
# 7 & 8: unsupported language/format fail explicitly
# ---------------------------------------------------------------------------


def test_unsupported_language_fails_explicitly() -> None:
    # "en" is deliberately not used here: it is an explicitly planned future
    # locale (contract section 9), not a permanently invalid one. Use a
    # sentinel that can never become a real locale code instead.
    with pytest.raises(ValueError, match="unsupported language"):
        get_locale("xx-invalid")
    with pytest.raises(ValueError, match="unsupported language"):
        build_book(language="xx-invalid", output_format="pdf")


def test_unsupported_format_fails_explicitly() -> None:
    with pytest.raises(ValueError, match="unsupported output format"):
        build_book(language="ru", output_format="docx")


# ---------------------------------------------------------------------------
# 9: output filenames are locale-config driven
# ---------------------------------------------------------------------------


def test_output_filenames_are_locale_config_driven() -> None:
    ru_config = get_locale("ru")
    pl_config = get_locale("pl")

    assert ru_config.pdf_output_path.name == "python-s-nulya-ru.pdf"
    assert ru_config.epub_output_path.name == "python-s-nulya-ru.epub"
    assert pl_config.pdf_output_path.name == "python-od-zera-pl.pdf"
    assert pl_config.epub_output_path.name == "python-od-zera-pl.epub"
    assert ru_config.pdf_output_path != pl_config.pdf_output_path
    assert ru_config.epub_output_path != pl_config.epub_output_path

    # Neither adapter may hardcode a locale's output filename — both must
    # take it from the config object they are handed.
    for adapter_source_path in (
        SCRIPTS / "book_pipeline" / "pdf_adapter.py",
        SCRIPTS / "book_pipeline" / "epub_adapter.py",
    ):
        source = adapter_source_path.read_text(encoding="utf-8")
        assert "python-s-nulya-ru" not in source
        assert "python-od-zera-pl" not in source


# ---------------------------------------------------------------------------
# 10: chapter order remains identical to canonical source ordering
# ---------------------------------------------------------------------------


def test_ru_chapter_title_order_matches_canonical_source() -> None:
    ru_config = get_locale("ru")
    canonical = chapter_metadata.chapters()
    assert [chapter.number for chapter in canonical] == list(range(1, 25))
    for chapter in canonical:
        assert ru_config.chapter_title(chapter.number) == chapter.title
        assert ru_config.chapter_canonical_url(chapter.number) == chapter.url


def test_canonical_model_preserves_sequential_chapter_order() -> None:
    """End-to-end: the loaded model's chapters are numbered 1..24 in order,
    for both languages — the pipeline never reorders or renumbers chapters
    per format or per language."""
    for language in SUPPORTED_LANGUAGES:
        model = CanonicalBookLoader.load(get_locale(language))
        assert [chapter.number for chapter in model.chapters] == list(range(1, 25))
        for chapter in model.chapters:
            assert len(chapter.pages) >= 1
