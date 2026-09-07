"""Regression guard for PR #117's final CI determinism blocker.

After the pagination-label fix (``tests/test_generated_pagination_localization.py``),
CI's final ``git diff --exit-code`` still failed on whitespace bytes in
``site/pl/index.html``. Root cause, confirmed directly against stdlib
``html.parser`` (via ``BeautifulSoup(...).find(...).previous_sibling``):
whitespace-only text nodes between two tags do not survive parsing with a
character count that's part of any documented contract. A literal two-space
run in the RU source (between ``</div>`` and ``<button>``) came back out of
the parser as a single space locally; a separate whitespace-only node
elsewhere, once a newline was involved, drifted between zero and one space
across CPython patch releases (3.14.6 local vs 3.14.7 CI). Both symptoms are
the same underlying bug: ``_translate_html_document``'s
``BeautifulSoup(source, "html.parser")`` reparses and reserializes the RU
source's such nodes, and the parser — not this codebase — decides how many
characters survive.

``normalize_generated_html_whitespace()`` collapses every whitespace-only
run between two tags to one fixed representative per category (a bare
newline if the run contained one, otherwise a single space) immediately
after BeautifulSoup serialization — the narrowest point where the drift can
enter; every later pipeline stage is plain regex/string manipulation and
cannot reintroduce it. HTML's own whitespace-collapse rule already renders
any such run as at most one visible space regardless of how many characters
it contains, so this changes zero rendered pixels while making the
serialized bytes independent of the parser's own internal decisions.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load_module(name: str) -> ModuleType:
    """Load a scripts/<name>.py module directly, without making scripts a
    package (same approach as tests/test_license_consistency.py and
    tests/test_build_polish_course_safety.py)."""
    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def build_polish_course() -> ModuleType:
    return _load_module("build_polish_course")


@pytest.fixture(scope="module")
def inject_language_switchers() -> ModuleType:
    return _load_module("inject_language_switchers")


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
    """A no-newline run that is already the canonical single space (e.g.
    a deliberate gap separating two inline elements) must survive
    unchanged."""
    source = '<span lang="ru">RU</span> <span lang="pl">PL</span>'
    assert build_polish_course.normalize_generated_html_whitespace(source) == source


def test_no_newline_multi_space_run_collapses_to_one_space(build_polish_course) -> None:
    """Reproduces the actual PR #117 drift site: a literal two-space run
    between a switcher </div> and the nav-toggle <button> — no newline
    involved — that stdlib html.parser parsed back out as a single space
    locally, and which is not guaranteed stable across CPython patch
    releases. Any such run must canonicalize to exactly one space,
    regardless of how many spaces/tabs it originally contained."""
    two_spaces = '</div>  <button class="nav-toggle">x</button>'
    one_space = '</div> <button class="nav-toggle">x</button>'
    zero_spaces_result = '</div> <button class="nav-toggle">x</button>'

    assert build_polish_course.normalize_generated_html_whitespace(two_spaces) == one_space
    assert build_polish_course.normalize_generated_html_whitespace(one_space) == one_space
    assert (
        build_polish_course.normalize_generated_html_whitespace('</div>\t<button class="nav-toggle">x</button>')
        == zero_spaces_result
    )


def test_unrelated_button_elements_are_untouched(build_polish_course) -> None:
    """The rule is structural (any inter-tag whitespace-only run), not
    specific to the nav-toggle button — but it also must not invent
    whitespace changes where none existed (zero-length gaps stay
    zero-length)."""
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


_HOMEPAGE_SHAPED_HEADER = """\
<html lang="pl">
<head><meta charset="utf-8"/></head>
<body>
<header>
<a class="brand" href="/pl/index.html">Cartesian School</a>
<ul class="top-nav"><li><a href="/pl/index.html">O kursie</a></li></ul>
<div class="language-switcher-desktop"><nav class="language-switcher" aria-label="Język"><span lang="pl" aria-current="true">PL</span></nav></div> <button aria-controls="mobile-nav-panel" class="nav-toggle" type="button">x</button>
</header>
<nav class="mobile-nav-panel" id="mobile-nav-panel">
<div class="mobile-nav-links">x</div>
<nav class="language-switcher" aria-label="Język"><span lang="pl" aria-current="true">PL</span></nav>
</nav>
</body>
</html>
"""


def test_empty_desktop_div_removal_does_not_splice_a_new_drift_prone_run(
    inject_language_switchers, tmp_path
) -> None:
    """Reproduces the actual PR #117 drift: the homepage template places
    the language-switcher-desktop div *before* the nav-toggle button
    (every other page's template places it after). Removing the emptied
    div naively would leave a bare newline (from before the div) directly
    adjacent to a bare space (from after the div) — the exact
    "\\n " that drifted between local and CI CPython patch releases.
    """
    page = tmp_path / "index.html"
    page.write_text(_HOMEPAGE_SHAPED_HEADER, encoding="utf-8")

    inject_language_switchers._inject(page, "<nav class=\"language-switcher\">NEW</nav>")

    result = page.read_text(encoding="utf-8")
    button_index = result.find("<button")
    assert result[button_index - 1] == "\n", (
        "the desktop-div removal must not leave a bare space directly "
        "before <button> — it must canonicalize to a single newline"
    )
    assert "\n " not in result.split("</header>")[0]


def test_inject_is_idempotent_on_its_own_output(inject_language_switchers, tmp_path) -> None:
    page = tmp_path / "index.html"
    page.write_text(_HOMEPAGE_SHAPED_HEADER, encoding="utf-8")
    switcher = '<nav class="language-switcher">NEW</nav>'

    inject_language_switchers._inject(page, switcher)
    once = page.read_text(encoding="utf-8")
    inject_language_switchers._inject(page, switcher)
    twice = page.read_text(encoding="utf-8")

    assert once == twice


def test_inject_does_not_reformat_unrelated_hand_authored_indentation(
    inject_language_switchers, tmp_path
) -> None:
    """The fix must be scoped to the switcher-removal splice point only —
    it must never touch RU's/PL's own hand-authored indentation elsewhere
    on the page (that reformatting was tried and rejected: it produced a
    14,000+ line diff across the RU homepage alone)."""
    source = """\
<html lang="ru">
<head><meta charset="utf-8"/></head>
<body>
  <a class="brand" href="/index.html">
    <img src="/assets/img/logo.png" alt="" />
  </a>
<header>
<div class="language-switcher-desktop"></div>
<button class="nav-toggle" type="button">x</button>
</header>
<nav class="mobile-nav-panel" id="mobile-nav-panel">
<div class="mobile-nav-links">x</div>
</nav>
</body>
</html>
"""
    page = tmp_path / "index.html"
    page.write_text(source, encoding="utf-8")

    inject_language_switchers._inject(page, '<nav class="language-switcher">NEW</nav>')

    result = page.read_text(encoding="utf-8")
    assert '  <a class="brand" href="/index.html">\n    <img src="/assets/img/logo.png" alt="" />\n  </a>' in result
