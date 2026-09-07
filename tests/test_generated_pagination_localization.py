"""Regression guard for PR #117's CI blocker: ``build_polish_course.py``'s
normal production rebuild raised ``KeyError: "Missing Polish translation
resource for 'ГЛАВА 1 · СТР. 11'"``.

Root cause: the chapter-opener label ``ГЛАВА {n} · СТР. {page}`` (see
``scripts/site_lib.py``) is structured, pipeline-generated metadata, not
human-authored prose — but the PL generator ran every Cyrillic string
through ``TranslationMemory``, which requires an exact committed entry per
distinct string. A pagination change (M02-I07 Phase 2B) shifted every
chapter's start page, producing 24 new label strings with no cached
translation, and the fail-closed ``TranslationMemory.translate()`` correctly
refused to invent one.

The fix — ``translate_generated_text()`` — recognizes this one structural
pattern and derives the PL label deterministically from the RU string's own
numbers, before the string ever reaches ``TranslationMemory``. These tests
pin that behavior directly (no HTML rendering, no real translation-memory
file) so it can never again require one-off translation-memory entries per
chapter/page-number combination.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load_build_polish_course() -> ModuleType:
    """Load scripts/build_polish_course.py directly, without making scripts
    a package (same approach as tests/test_license_consistency.py and
    tests/test_build_polish_course_safety.py)."""
    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location(
        "build_polish_course", ROOT / "scripts" / "build_polish_course.py"
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    # Must be registered before exec_module(): the module defines a
    # @dataclass, and dataclasses.py resolves annotations via
    # sys.modules[cls.__module__] — it would otherwise raise AttributeError
    # on a None lookup.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def build_polish_course() -> ModuleType:
    return _load_build_polish_course()


def test_chapter_opener_label_localizes_structurally(build_polish_course) -> None:
    result = build_polish_course.translate_generated_text("ГЛАВА 1 · СТР. 11", "pl")
    assert result == "ROZDZIAŁ 1 · STRONA 11"


@pytest.mark.parametrize(
    ("chapter", "page"),
    [(1, 11), (7, 446), (24, 4438), (13, 1072), (9, 1)],
)
def test_chapter_opener_label_preserves_arbitrary_digits_exactly(
    build_polish_course, chapter: int, page: int
) -> None:
    source = f"ГЛАВА {chapter} · СТР. {page}"
    result = build_polish_course.translate_generated_text(source, "pl")
    assert result == f"ROZDZIAŁ {chapter} · STRONA {page}"


def test_unrecognized_locale_returns_none(build_polish_course) -> None:
    assert build_polish_course.translate_generated_text("ГЛАВА 1 · СТР. 11", "de") is None


def test_ordinary_prose_is_not_matched(build_polish_course) -> None:
    assert build_polish_course.translate_generated_text("Привет, мир!", "pl") is None
    assert build_polish_course.translate_generated_text("ГЛАВА 1: Введение", "pl") is None


def test_translation_memory_resolves_chapter_opener_without_an_entry(build_polish_course) -> None:
    """The structural rule must be consulted *before* the TranslationMemory
    lookup, and must never register the string as missing/pending — a
    pagination change must not require new committed TM entries."""
    tm = build_polish_course.TranslationMemory(collect=False)
    assert "ГЛАВА 1 · СТР. 11" not in tm.entries.values()
    sources_before = dict(tm.sources)

    result = tm.translate("ГЛАВА 1 · СТР. 11")

    assert result == "ROZDZIAŁ 1 · STRONA 11"
    assert tm.missing == set()
    assert tm.sources == sources_before, "must not record a TM entry for a structurally-derived label"


def test_ordinary_unknown_prose_still_raises_in_normal_mode(build_polish_course) -> None:
    tm = build_polish_course.TranslationMemory(collect=False)
    with pytest.raises(KeyError, match="Missing Polish translation resource"):
        tm.translate("Это совершенно новая, никогда не переводившаяся строка")


def test_collect_mode_semantics_unchanged_for_ordinary_prose(build_polish_course) -> None:
    tm = build_polish_course.TranslationMemory(collect=True)
    source = "Это совершенно новая, никогда не переводившаяся строка"

    result = tm.translate(source)

    assert result == source
    assert source in tm.missing


def test_collect_mode_does_not_register_chapter_opener_as_missing(build_polish_course) -> None:
    tm = build_polish_course.TranslationMemory(collect=True)

    result = tm.translate("ГЛАВА 3 · СТР. 236")

    assert result == "ROZDZIAŁ 3 · STRONA 236"
    assert tm.missing == set()
