"""Tests for the M02-I07 Phase 2B pagination remediation.

Covers the ticket's explicit test requirements: the canonical print CSS
carries the four approved P0/P1/P4 changes, no RU/PL-specific pagination
rule exists, code-block splittable classification is deterministic (long
blocks tagged, short blocks not, threshold boundary exact), identical
source structure classifies identically regardless of language, no content
text is altered by classification, and EPUB's own stylesheet/behavior is
untouched by it.
"""

from __future__ import annotations

import inspect
import sys
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import book_shared as bs

# ---------------------------------------------------------------------------
# 1. Canonical shared CSS contains the four approved changes
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def print_css() -> str:
    return bs.build_print_css(book_title="Any Title", page_abbrev="p.")


def test_css_contains_project_hero_45mm(print_css: str) -> None:
    assert ".project-entry .project-hero { width: 100%; height: 45mm;" in print_css
    assert "height: 62mm" not in print_css


def test_css_contains_chapter_hero_break_before_page(print_css: str) -> None:
    assert ".chapter-hero { page: opener; break-before: page;" in print_css
    assert "break-before: right" not in print_css


def test_css_contains_body_font_98pt(print_css: str) -> None:
    assert "font-size: 9.8pt; line-height: 1.40;" in print_css
    assert "font-size: 10.3pt" not in print_css


def test_css_body_line_height_is_140_not_135(print_css: str) -> None:
    """The ticket explicitly forbids 1.35 in this pass — check the BODY
    rule specifically, since 1.35 legitimately appears elsewhere in the
    stylesheet for an unrelated component (.compare-table's own
    line-height), so a blanket string search would false-positive."""
    assert "font-size: 9.8pt; line-height: 1.40;" in print_css
    assert "font-size: 10.3pt; line-height: 1.48;" not in print_css
    assert "font-size: 10.3pt; line-height: 1.35;" not in print_css


def test_css_project_entry_forced_break_is_unchanged(print_css: str) -> None:
    """Explicit ticket policy: keep .project-entry's own break-before:page in
    this pass — only the hero height changed, not the forced break itself."""
    assert ".project-entry { break-before: page; }" in print_css


def test_css_code_block_default_still_avoids_breaking(print_css: str) -> None:
    """Only .code-block--splittable may fragment; the base .code-block rule
    keeps break-inside: avoid untouched (short/medium blocks stay intact)."""
    assert ".code-block { border: 1px solid var(--color-border-default); border-radius: var(--radius-md); margin: 10pt 0; break-inside: avoid; overflow: hidden; }" in print_css
    assert ".code-block--splittable { break-inside: auto" in print_css


def test_css_callouts_are_unchanged_in_this_pass(print_css: str) -> None:
    """Per the ticket's explicit fallback: callout-size classification was
    judged not reliably deterministic without added complexity, so callouts
    are left with their existing break-inside: avoid, undisturbed."""
    assert ".callout { border: 1px solid var(--color-border-default); border-left: 3.5pt solid var(--color-brand-blue); border-radius: var(--radius-md); padding: 6pt 10pt; margin: 8pt 0; background: var(--color-bg-surface); break-inside: avoid; }" in print_css


def test_css_page_size_and_margins_unchanged(print_css: str) -> None:
    """P3 explicitly out of scope for this pass."""
    assert "size: 152mm 229mm;" in print_css
    assert "margin: 24mm 20mm 26mm 20mm;" in print_css


# ---------------------------------------------------------------------------
# 2. No RU/PL-specific pagination rule exists
# ---------------------------------------------------------------------------


def test_build_print_css_has_no_language_parameter() -> None:
    """The canonical print stylesheet builder never took (and still does
    not take) a language argument — the only two parameters are locale
    LABELS (book_title, page_abbrev), not language-conditional logic."""
    params = set(inspect.signature(bs.build_print_css).parameters)
    assert params == {"book_title", "page_abbrev"}


def test_print_css_is_structurally_identical_for_ru_and_pl_locales() -> None:
    """Building the stylesheet with each locale's own title/abbrev must
    differ ONLY in the two injected label placeholders — every pagination
    rule (break-before, break-inside, font-size, line-height, margins) is
    byte-identical between the two calls."""
    sys.path.insert(0, str(SCRIPTS))
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


def test_no_language_specific_pagination_branch_in_book_shared() -> None:
    source = (SCRIPTS / "book_shared.py").read_text(encoding="utf-8")
    forbidden = ('language == "ru"', 'language == "pl"', "if language ==", 'locale == "ru"', 'locale == "pl"')
    for pattern in forbidden:
        assert pattern not in source, f"found language-specific branch in book_shared.py: {pattern!r}"


# ---------------------------------------------------------------------------
# 3-5. Code-block splittable classification: deterministic, threshold-exact
# ---------------------------------------------------------------------------


def _code_block_html(n_lines: int) -> str:
    code = "\n".join(f"x{i} = {i}" for i in range(n_lines))
    return f'<html><body><div class="code-block"><pre><code>{code}</code></pre></div></body></html>'


def test_short_code_block_is_not_classified_splittable() -> None:
    html = _code_block_html(5)
    result = bs.classify_splittable_code_blocks(html)
    assert result == html  # untouched, not even re-serialized
    assert "code-block--splittable" not in result


def test_long_code_block_is_classified_splittable() -> None:
    html = _code_block_html(40)
    result = bs.classify_splittable_code_blocks(html)
    assert "code-block--splittable" in result


@pytest.mark.parametrize(
    "line_count,expect_splittable",
    [
        (1, False),
        (bs.CODE_BLOCK_SPLITTABLE_LINE_THRESHOLD - 1, False),
        (bs.CODE_BLOCK_SPLITTABLE_LINE_THRESHOLD, False),  # exactly at threshold: NOT splittable (strictly >)
        (bs.CODE_BLOCK_SPLITTABLE_LINE_THRESHOLD + 1, True),  # one line over: splittable
        (100, True),
    ],
)
def test_threshold_boundary_is_exact(line_count: int, expect_splittable: bool) -> None:
    result = bs.classify_splittable_code_blocks(_code_block_html(line_count))
    assert ("code-block--splittable" in result) is expect_splittable


def test_threshold_is_18_lines_as_specified_by_the_ticket() -> None:
    """Pinned so a future change to this constant is a visible, deliberate
    diff, not an accidental drift — see book_shared.py's own comment for the
    corpus measurement that justified this exact value."""
    assert bs.CODE_BLOCK_SPLITTABLE_LINE_THRESHOLD == 18


def test_classification_is_deterministic_across_repeated_calls() -> None:
    html = _code_block_html(30)
    first = bs.classify_splittable_code_blocks(html)
    second = bs.classify_splittable_code_blocks(html)
    assert first == second


def test_multiple_code_blocks_are_classified_independently() -> None:
    short_block = '<div class="code-block"><pre><code>' + "\n".join(f"a{i}" for i in range(3)) + "</code></pre></div>"
    long_block = '<div class="code-block"><pre><code>' + "\n".join(f"b{i}" for i in range(30)) + "</code></pre></div>"
    html = f"<html><body>{short_block}{long_block}</body></html>"
    result = bs.classify_splittable_code_blocks(html)
    soup = BeautifulSoup(result, "lxml")
    blocks = soup.find_all("div", class_="code-block")
    assert len(blocks) == 2
    assert "code-block--splittable" not in blocks[0].get("class", [])
    assert "code-block--splittable" in blocks[1].get("class", [])


# ---------------------------------------------------------------------------
# 6. Same source structure in RU and PL receives equivalent classification
# ---------------------------------------------------------------------------


def test_identical_line_count_classifies_identically_regardless_of_language_text() -> None:
    """The classifier only ever inspects line count, never language/script —
    Cyrillic and Latin content of the same structural size must classify
    the same way."""
    ru_code = "\n".join(f"перемен_{i} = {i}  # комментарий" for i in range(30))
    pl_code = "\n".join(f"zmienna_{i} = {i}  # komentarz" for i in range(30))
    ru_html = f'<html><body><div class="code-block"><pre><code>{ru_code}</code></pre></div></body></html>'
    pl_html = f'<html><body><div class="code-block"><pre><code>{pl_code}</code></pre></div></body></html>'

    ru_result = bs.classify_splittable_code_blocks(ru_html)
    pl_result = bs.classify_splittable_code_blocks(pl_html)
    assert "code-block--splittable" in ru_result
    assert "code-block--splittable" in pl_result


def test_classify_function_takes_no_language_parameter() -> None:
    params = set(inspect.signature(bs.classify_splittable_code_blocks).parameters)
    assert "language" not in params
    assert "locale" not in params


# ---------------------------------------------------------------------------
# 8. No content text is altered by code-block classification
# ---------------------------------------------------------------------------


def test_classification_does_not_alter_visible_text() -> None:
    original = _code_block_html(30)
    classified = bs.classify_splittable_code_blocks(original)
    original_text = BeautifulSoup(original, "lxml").get_text()
    classified_text = BeautifulSoup(classified, "lxml").get_text()
    assert original_text == classified_text


def test_classification_preserves_line_order_and_count() -> None:
    lines = [f"step_{i} = {i}" for i in range(25)]
    html = f'<html><body><div class="code-block"><pre><code>{chr(10).join(lines)}</code></pre></div></body></html>'
    classified = bs.classify_splittable_code_blocks(html)
    soup = BeautifulSoup(classified, "lxml")
    code_text = soup.find("code").get_text()
    assert code_text.split("\n") == lines  # no missing, duplicated, or reordered lines


def test_classification_is_a_noop_when_no_code_block_present() -> None:
    html = "<html><body><p>Just a paragraph, no code here.</p></body></html>"
    assert bs.classify_splittable_code_blocks(html) == html


def test_classification_is_a_noop_when_code_block_has_no_code_element() -> None:
    html = '<html><body><div class="code-block"><pre>no code tag here</pre></div></body></html>'
    assert bs.classify_splittable_code_blocks(html) == html


# ---------------------------------------------------------------------------
# 9. EPUB behavior/CSS is not changed by PDF-only pagination classification
# ---------------------------------------------------------------------------


def test_epub_stylesheet_defines_no_splittable_rule() -> None:
    """The classification only matters to the PDF print stylesheet
    (book_shared.build_print_css) — EPUB packages the WEBSITE's own
    theory.css verbatim (via epub_adapter.py), which this change must not
    touch, so the added class attribute is inert there."""
    theory_css = (ROOT / "site" / "assets" / "css" / "theory.css").read_text(encoding="utf-8")
    assert "code-block--splittable" not in theory_css


def test_epub_adapter_does_not_reference_splittable_class() -> None:
    epub_adapter_source = (SCRIPTS / "book_pipeline" / "epub_adapter.py").read_text(encoding="utf-8")
    assert "code-block--splittable" not in epub_adapter_source
    assert "classify_splittable_code_blocks" not in epub_adapter_source


def test_normalization_happens_once_in_the_shared_loader_not_per_adapter() -> None:
    """The classification call must live in the one shared canonical loader
    (book_pipeline/model.py) — never duplicated into pdf_adapter.py or
    epub_adapter.py, which would violate the single-canonical-pipeline
    contract this ticket explicitly re-affirms."""
    model_source = (SCRIPTS / "book_pipeline" / "model.py").read_text(encoding="utf-8")
    pdf_adapter_source = (SCRIPTS / "book_pipeline" / "pdf_adapter.py").read_text(encoding="utf-8")
    epub_adapter_source = (SCRIPTS / "book_pipeline" / "epub_adapter.py").read_text(encoding="utf-8")
    assert "classify_splittable_code_blocks" in model_source
    assert "classify_splittable_code_blocks" not in pdf_adapter_source
    assert "classify_splittable_code_blocks" not in epub_adapter_source
