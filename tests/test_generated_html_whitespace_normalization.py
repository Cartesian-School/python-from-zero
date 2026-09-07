"""Regression guard for PR #117's final CI determinism blocker.

After the pagination-label fix (``tests/test_generated_pagination_localization.py``),
CI's final ``git diff --exit-code`` still failed on a single whitespace byte in
``site/pl/index.html``: the committed tree had one leading space before the
generated mobile-nav ``<button ... class="nav-toggle" ...>``, while a fresh
GitHub Actions rebuild produced zero. Both environments ran the identical
pinned beautifulsoup4/lxml versions; only the CPython patch release differed
(3.14.6 locally vs 3.14.7 in CI). The exact run of spaces/tabs stdlib
``html.parser`` keeps around a newline in a whitespace-only text node is not
part of any documented contract, so it is not guaranteed stable across
patch releases — and ``_translate_html_document``'s ``BeautifulSoup(source,
"html.parser")`` reparses and reserializes the RU source's such nodes
verbatim.

``normalize_generated_html_whitespace()`` collapses every whitespace-only,
newline-containing run between two tags to one canonical form immediately
after BeautifulSoup serialization (the narrowest point where the drift can
enter — every later pipeline stage is plain regex/string manipulation and
cannot reintroduce it). HTML's own whitespace-collapse rule already renders
any such run as a single space regardless of how many spaces/tabs it
contains, so this changes zero rendered pixels.
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
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def build_polish_course() -> ModuleType:
    return _load_build_polish_course()


_CANONICAL_NAV_TOGGLE = (
    '</ul>\n<button aria-controls="mobile-nav-panel" class="nav-toggle">x</button>'
)


@pytest.mark.parametrize(
    "leading_whitespace",
    ["", " ", "   ", "\t", " \t "],
    ids=["zero-spaces", "one-space", "three-spaces", "tab", "mixed"],
)
def test_nav_toggle_whitespace_variants_normalize_identically(
    build_polish_course, leading_whitespace: str
) -> None:
    source = (
        '</ul>\n' + leading_whitespace
        + '<button aria-controls="mobile-nav-panel" class="nav-toggle">x</button>'
    )
    result = build_polish_course.normalize_generated_html_whitespace(source)
    assert result == _CANONICAL_NAV_TOGGLE


def test_visible_prose_whitespace_is_untouched(build_polish_course) -> None:
    source = "<p>Python od zera — kurs interaktywny</p>"
    assert build_polish_course.normalize_generated_html_whitespace(source) == source


def test_deliberate_inline_single_space_is_untouched(build_polish_course) -> None:
    """A whitespace run with no newline (e.g. the space separating two
    inline switcher labels) is meaningful inline spacing, not layout
    indentation, and must survive unchanged."""
    source = '<span lang="ru">RU</span> <span lang="pl">PL</span>'
    assert build_polish_course.normalize_generated_html_whitespace(source) == source


def test_unrelated_button_elements_are_untouched(build_polish_course) -> None:
    """The rule is structural (any inter-tag newline-containing whitespace
    run), not specific to the nav-toggle button — but it also must not
    invent whitespace changes where none existed."""
    source = '<button type="submit">OK</button>'
    assert build_polish_course.normalize_generated_html_whitespace(source) == source

    tight = "<div><button>A</button><button>B</button></div>"
    assert build_polish_course.normalize_generated_html_whitespace(tight) == tight


def test_protected_elements_preserve_significant_whitespace(build_polish_course) -> None:
    for tag in ("pre", "code", "textarea", "script", "style"):
        source = f"<{tag}>\n   indented\n     more\n</{tag}>"
        assert build_polish_course.normalize_generated_html_whitespace(source) == source


def test_normalization_is_idempotent(build_polish_course) -> None:
    source = (
        '<header>\n  <a href="/">Home</a>\n\t\t<button class="nav-toggle">x</button>  \n'
        "</header>"
    )
    once = build_polish_course.normalize_generated_html_whitespace(source)
    twice = build_polish_course.normalize_generated_html_whitespace(once)
    assert once == twice


def test_structural_pagination_labels_still_localize(build_polish_course) -> None:
    """Guards against a fix at this boundary breaking the earlier PR #117
    structural pagination-label fix (translate_generated_text)."""
    result = build_polish_course.translate_generated_text("ГЛАВА 1 · СТР. 11", "pl")
    assert result == "ROZDZIAŁ 1 · STRONA 11"


def test_unknown_prose_still_fails_closed(build_polish_course) -> None:
    tm = build_polish_course.TranslationMemory(collect=False)
    with pytest.raises(KeyError, match="Missing Polish translation resource"):
        tm.translate("Абсолютно новая непереведённая строка для этого теста")
