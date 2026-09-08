"""Canonical, language-independent PDF pagination diagnostics (M02-I07 Phase 2A).

Per docs/contracts/BOOK-BUILD-PIPELINE-CONTRACT.md, this module is diagnostic
ONLY: it never writes to a publication artifact, never changes a pagination
rule, and never forks its analysis by language. It answers "why does this
many physical pages exist" with hard numbers, derived from the SAME
canonical model/config every other stage of the pipeline uses.

Two measurement tiers:

1. Artifact analysis (fast, ~1 minute/book): reads the already-built PDF
   (text extraction, outline/bookmarks) and its pagination sidecar
   (data/book-pagination*.json) — the physical page tree and its generated
   metadata are the authority, exactly as the rest of the pipeline treats
   them. No re-rendering.

2. Render experiments (slow, ~10-15 minutes/book; opt-in via
   ``run_render_experiments=True``): re-renders the canonical
   ``pdf_adapter.build_full_html()`` output with ONE targeted CSS rule
   swapped at a time (e.g. ``.chapter-hero`` recto -> plain page break) to
   MEASURE the exact page-count delta that rule is responsible for, instead
   of guessing from static inspection alone. Every experiment is discarded
   in memory; nothing is written back to book_shared.py or any artifact.
"""

from __future__ import annotations

import re
import statistics
from dataclasses import dataclass
from pathlib import Path

import book_shared as bs
from pypdf import PdfReader

from .config import BookLocaleConfig
from .model import CanonicalBookLoader, CanonicalBookModel

ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMA_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Explicit, reported thresholds (contract: "Define explicit thresholds in
# code and report them" — do not let these drift silently between runs).
# ---------------------------------------------------------------------------
BLANK_MAX_WORDS = 0
NEAR_EMPTY_MAX_WORDS = 25
VERY_SPARSE_MAX_WORDS = 50
SPARSE_MAX_WORDS = 100
EXTENDED_SPARSE_MAX_WORDS = 150

THRESHOLDS = {
    "blank_max_words": BLANK_MAX_WORDS,
    "near_empty_max_words": NEAR_EMPTY_MAX_WORDS,
    "very_sparse_max_words": VERY_SPARSE_MAX_WORDS,
    "sparse_max_words": SPARSE_MAX_WORDS,
    "extended_sparse_max_words": EXTENDED_SPARSE_MAX_WORDS,
}

# Break-related selectors in the shared print stylesheet (book_shared.
# build_print_css). Kept as data here, not re-derived by parsing CSS with a
# real parser — the stylesheet is small, hand-authored, and shared by every
# language, so a literal-substring inventory is the strongest deterministic
# evidence available without vendoring a CSS parser for a diagnostic tool.
BREAK_INSIDE_AVOID_SELECTORS = (
    ".code-block",
    ".callout",
    ".exercise",
    ".summary-box",
    ".cvm",
    ".chapter-figure",
    ".idx-entry",
    ".notebook-card",
    ".compare-table tr",
)


def _word_count(text: str) -> int:
    return len(text.split())


def _strip_known_page_chrome(text: str, *, page_number: int, book_title: str) -> str:
    """Best-effort, PARTIAL removal of print running-header/folio chrome from
    a page's raw extracted text, for a stricter "body word count" than
    ``word_count`` alone.

    ``word_count`` is computed from raw ``pypdf`` text extraction, which
    includes the page's running header and folio (per book_shared.
    build_print_css's ``@top-*``/``@bottom-center`` rules) — so
    ``word_count == 0`` would only ever be true for a page with NO
    body content, no running header, AND no folio, which given this
    stylesheet essentially never happens. It does NOT prove the page's body
    is empty.

    This function strips only the TWO chrome elements identifiable with
    certainty from the committed artifacts:

    1. The page's own folio (``@bottom-center { content: counter(page); }``)
       — always exactly this page's own number, as a trailing text line.
    2. The constant book-title running header shown on right-hand pages
       (``@page :right { @top-right { content: "<book_title>"; ...
       text-transform: uppercase; } }``) — an exact, page-independent
       string, matched case-insensitively since the rendered glyphs are
       uppercase.

    It deliberately does NOT strip the DYNAMIC chapter/lesson-title running
    header shown on left-hand pages (``string(chaptitle)``, i.e. whichever
    <h1> was most recently rendered) — that text varies per physical page
    and is not reliably reconstructible from the committed artifacts alone
    without tracking every source page's own heading position, which is out
    of scope here. A page whose only extracted content is that dynamic
    header will therefore still show as "body non-empty" under this
    function — see the module's documented limitation.
    """
    lines = text.split("\n")
    if lines and lines[-1].strip() == str(page_number):
        lines = lines[:-1]
    normalized_title = book_title.strip().casefold()
    return "\n".join(line for line in lines if line.strip().casefold() != normalized_title)


def _percentile(sorted_values: list[float], p: float) -> float:
    if not sorted_values:
        return 0.0
    if len(sorted_values) == 1:
        return float(sorted_values[0])
    k = (len(sorted_values) - 1) * (p / 100)
    f = int(k)
    c = min(f + 1, len(sorted_values) - 1)
    if f == c:
        return float(sorted_values[f])
    return sorted_values[f] + (sorted_values[c] - sorted_values[f]) * (k - f)


def _url_for(config: BookLocaleConfig, rel_path: str) -> str:
    """The exact canonical-URL key convention pdf_adapter.build_full_html()
    uses for data/book-pagination*.json's ``pages`` dict. Reused here (a
    single-expression convention, not build logic) so diagnostics can look
    up a page's rendered physical page number from the committed sidecar."""
    return config.url_path_prefix + "/" + rel_path


def _flatten_outline(items) -> list:
    flat = []
    for item in items or []:
        if isinstance(item, list):
            flat.extend(_flatten_outline(item))
        else:
            flat.append(item)
    return flat


@dataclass(frozen=True, slots=True)
class PageRecord:
    number: int
    category: str
    chapter_number: int | None
    project_slug: str | None
    word_count: int
    char_count: int
    body_word_count: int

    @property
    def is_blank(self) -> bool:
        """Zero words under RAW pypdf extraction. Given this stylesheet
        always renders a running header and/or folio, this proves only
        "no extractable text of any kind, including chrome" — NOT "the
        page's body is visually/textually empty". See ``is_body_effectively_
        empty`` for the (still partial — see _strip_known_page_chrome)
        chrome-stripped signal."""
        return self.word_count <= BLANK_MAX_WORDS

    @property
    def is_near_empty(self) -> bool:
        return self.word_count < NEAR_EMPTY_MAX_WORDS

    @property
    def is_very_sparse(self) -> bool:
        return self.word_count < VERY_SPARSE_MAX_WORDS

    @property
    def is_sparse(self) -> bool:
        return self.word_count < SPARSE_MAX_WORDS

    @property
    def is_body_effectively_empty(self) -> bool:
        """Zero words after stripping the page's own folio and the constant
        book-title running header (see _strip_known_page_chrome). Still a
        PARTIAL signal — it does not strip the dynamic per-page chapter/
        lesson-title running header — so this can undercount, but it can
        never OVERcount relative to a true visual-blank determination the
        way raw ``is_blank`` can."""
        return self.body_word_count <= BLANK_MAX_WORDS

    def to_dict(self) -> dict:
        return {
            "number": self.number,
            "category": self.category,
            "chapter_number": self.chapter_number,
            "project_slug": self.project_slug,
            "word_count": self.word_count,
            "char_count": self.char_count,
            "body_word_count": self.body_word_count,
            "is_blank": self.is_blank,
            "is_near_empty": self.is_near_empty,
            "is_very_sparse": self.is_very_sparse,
            "is_sparse": self.is_sparse,
            "is_body_effectively_empty": self.is_body_effectively_empty,
        }


@dataclass
class DiagnosticsInputs:
    """Everything read from committed artifacts, before classification."""

    config: BookLocaleConfig
    model: CanonicalBookModel
    reader: PdfReader
    pagination_meta: dict
    page_texts: list[str]  # index 0 == physical page 1


def _load_inputs(language: str) -> DiagnosticsInputs:
    import json

    from .locales import get_locale

    config = get_locale(language)
    if not config.pdf_output_path.is_file():
        raise FileNotFoundError(
            f"required artifact is missing: {config.pdf_output_path} "
            f"(run scripts/build_book.py --language {language} --format pdf first)"
        )
    if not config.pagination_output_path.is_file():
        raise FileNotFoundError(
            f"required artifact is missing: {config.pagination_output_path} "
            f"(run scripts/build_book.py --language {language} --format pdf first)"
        )
    pagination_meta = json.loads(config.pagination_output_path.read_text(encoding="utf-8"))
    model = CanonicalBookLoader.load(config)
    reader = PdfReader(str(config.pdf_output_path))
    page_texts = [(page.extract_text() or "") for page in reader.pages]
    return DiagnosticsInputs(
        config=config, model=model, reader=reader, pagination_meta=pagination_meta, page_texts=page_texts
    )


def _classify_pages(inputs: DiagnosticsInputs) -> list[PageRecord]:
    """Deterministic page classification from committed artifacts only.

    Boundaries come from three sources, in order of preference:
    1. data/book-pagination*.json's ``chapters``/``pages`` dicts (the
       physical page tree's own generated metadata — authoritative per the
       contract).
    2. The final PDF's own outline/bookmarks (auto-generated by WeasyPrint
       from every <h1>), used only where the sidecar has no entry (project
       entries, the index) — matched by exact title text against the
       canonical model, not guessed from position alone.
    3. Fixed, documented physical-layout constants for the three pages that
       precede any anchor (cover/title/copyright), per
       book_shared.write_pdf_pagination_metadata's own
       ``front_matter_numbering`` note.
    """
    config, model, meta = inputs.config, inputs.model, inputs.pagination_meta
    total_pages = int(meta["total_pages"])
    url_pages: dict[str, int] = meta["pages"]
    chapters_meta = meta["chapters"]

    records: dict[int, dict] = {}

    def assign(page_no: int, category: str, *, chapter_number: int | None = None, project_slug: str | None = None) -> None:
        if page_no in records:
            raise RuntimeError(f"page {page_no} classified twice: {records[page_no]['category']!r} and {category!r}")
        records[page_no] = {"category": category, "chapter_number": chapter_number, "project_slug": project_slug}

    # Fixed front-matter layout (cover/title/copyright are never anchored —
    # they are always the first three physical pages; see
    # book_shared.write_pdf_pagination_metadata's front_matter_numbering).
    assign(1, "cover")
    assign(2, "title")
    assign(3, "copyright")

    front_matter_starts = [url_pages[_url_for(config, page.rel_path)] for page in model.front_matter]
    first_front_matter_start = min(front_matter_starts)
    for page_no in range(4, first_front_matter_start):
        assign(page_no, "toc")

    boundaries = sorted(front_matter_starts) + [int(chapters_meta["01"]["start_page"])]
    for start, end in zip(boundaries, boundaries[1:]):
        for page_no in range(start, end):
            assign(page_no, "front_matter")

    for number in range(1, 25):
        chapter = model.chapters[number - 1]
        entry = chapters_meta[f"{number:02d}"]
        chapter_start, chapter_end = int(entry["start_page"]), int(entry["end_page"])
        if len(chapter.pages) > 1:
            second_page_url = _url_for(config, chapter.pages[1].rel_path)
            opener_end = url_pages[second_page_url] - 1
        else:
            opener_end = chapter_end
        for page_no in range(chapter_start, opener_end + 1):
            assign(page_no, "chapter_opener", chapter_number=number)
        for page_no in range(opener_end + 1, chapter_end + 1):
            assign(page_no, "chapter_content", chapter_number=number)

    projects_intro_start = int(chapters_meta["24"]["end_page"]) + 1

    outline = _flatten_outline(inputs.reader.outline)

    def first_bookmark_page(title: str, *, at_or_after: int) -> int:
        for item in outline:
            try:
                page_no = inputs.reader.get_destination_page_number(item) + 1
            except Exception:
                continue
            if item.title == title and page_no >= at_or_after:
                return page_no
        raise RuntimeError(f"no PDF bookmark titled {title!r} found at/after page {at_or_after}")

    index_start = first_bookmark_page(config.toc_index_label, at_or_after=projects_intro_start)

    project_starts: list[tuple[str, int]] = []
    for project in model.projects:
        page_no = first_bookmark_page(project.title, at_or_after=projects_intro_start)
        project_starts.append((project.slug, page_no))
    project_starts.sort(key=lambda item: item[1])

    intro_end = (project_starts[0][1] - 1) if project_starts else (index_start - 1)
    for page_no in range(projects_intro_start, intro_end + 1):
        assign(page_no, "project_intro")

    boundaries = [page for _slug, page in project_starts] + [index_start]
    for (slug, start), end in zip(project_starts, boundaries[1:]):
        for page_no in range(start, end):
            assign(page_no, "project_entry", project_slug=slug)

    for page_no in range(index_start, total_pages + 1):
        assign(page_no, "index")

    missing = sorted(set(range(1, total_pages + 1)) - set(records))
    if missing:
        raise RuntimeError(f"page classification left {len(missing)} page(s) uncategorized: {missing[:10]}...")

    book_title = config.book_title
    return [
        PageRecord(
            number=page_no,
            category=records[page_no]["category"],
            chapter_number=records[page_no]["chapter_number"],
            project_slug=records[page_no]["project_slug"],
            word_count=_word_count(inputs.page_texts[page_no - 1]),
            char_count=len(inputs.page_texts[page_no - 1]),
            body_word_count=_word_count(
                _strip_known_page_chrome(inputs.page_texts[page_no - 1], page_number=page_no, book_title=book_title)
            ),
        )
        for page_no in range(1, total_pages + 1)
    ]


def _totals(pages: list[PageRecord]) -> dict:
    """``blank_pages`` counts zero-text pages under RAW pypdf extraction,
    which includes running headers/folios (see PageRecord.is_blank) — it
    proves only "no extractable text of any kind", not "the page's body is
    visually/textually empty". ``body_effectively_empty_pages`` is a
    stricter, still-partial secondary signal (see
    PageRecord.is_body_effectively_empty / _strip_known_page_chrome) that
    strips the two chrome elements identifiable with certainty."""
    words = [p.word_count for p in pages]
    chars = [p.char_count for p in pages]
    sorted_words = sorted(words)
    return {
        "total_pages": len(pages),
        "blank_pages": sum(p.is_blank for p in pages),
        "body_effectively_empty_pages": sum(p.is_body_effectively_empty for p in pages),
        "near_empty_pages": sum(p.is_near_empty for p in pages),
        "pages_under_25_words": sum(1 for w in words if w < 25),
        "pages_under_50_words": sum(1 for w in words if w < 50),
        "pages_under_100_words": sum(1 for w in words if w < 100),
        "pages_under_150_words": sum(1 for w in words if w < 150),
        "mean_words_per_page": round(statistics.fmean(words), 2) if words else 0.0,
        "median_words_per_page": round(statistics.median(words), 2) if words else 0.0,
        "p10_words_per_page": round(_percentile(sorted_words, 10), 2),
        "p25_words_per_page": round(_percentile(sorted_words, 25), 2),
        "p75_words_per_page": round(_percentile(sorted_words, 75), 2),
        "p90_words_per_page": round(_percentile(sorted_words, 90), 2),
        "max_words_per_page": max(words) if words else 0,
        "mean_characters_per_page": round(statistics.fmean(chars), 1) if chars else 0.0,
        "median_characters_per_page": round(statistics.median(chars), 1) if chars else 0.0,
    }


def _category_totals(pages: list[PageRecord]) -> dict:
    totals: dict[str, int] = {}
    for page in pages:
        totals[page.category] = totals.get(page.category, 0) + 1
    return totals


def _category_word_stats(pages: list[PageRecord]) -> dict:
    by_category: dict[str, list[int]] = {}
    for page in pages:
        by_category.setdefault(page.category, []).append(page.word_count)
    return {
        category: {
            "pages": len(words),
            "mean_words": round(statistics.fmean(words), 2),
            "median_words": round(statistics.median(words), 2),
        }
        for category, words in by_category.items()
    }


def _chapter_diagnostics(pages: list[PageRecord], meta: dict) -> list[dict]:
    by_chapter: dict[int, list[PageRecord]] = {}
    for page in pages:
        if page.chapter_number is not None:
            by_chapter.setdefault(page.chapter_number, []).append(page)

    chapters = []
    for number in range(1, 25):
        chapter_pages = sorted(by_chapter.get(number, []), key=lambda p: p.number)
        entry = meta["chapters"][f"{number:02d}"]
        opener_pages = [p for p in chapter_pages if p.category == "chapter_opener"]
        total_words = sum(p.word_count for p in chapter_pages)
        page_count = len(chapter_pages)
        chapters.append(
            {
                "number": number,
                "title": entry["title"],
                "start_page": entry["start_page"],
                "end_page": entry["end_page"],
                "page_count": page_count,
                "opener_pages": len(opener_pages),
                "opener_words": sum(p.word_count for p in opener_pages),
                "total_words": total_words,
                "mean_words_per_page": round(total_words / page_count, 2) if page_count else 0.0,
                "blank_pages": sum(p.is_blank for p in chapter_pages),
                "near_empty_pages": sum(p.is_near_empty for p in chapter_pages),
                "very_sparse_pages": sum(p.is_very_sparse for p in chapter_pages),
            }
        )
    return chapters


def _recto_policy_report(pages: list[PageRecord], chapters: list[dict]) -> dict:
    """Deterministic evidence about the recto (right-hand) chapter-start
    policy, WITHOUT assuming a literal zero-word filler page exists (the RU
    and PL corpora both have zero raw zero-word pages — see totals.
    blank_pages and its documented raw-extraction caveat): flags the page
    immediately preceding each chapter opener as a "recto candidate" whenever it is functionally near-empty
    (< NEAR_EMPTY_MAX_WORDS) and belongs to the PRECEDING chapter's own
    content, i.e. it is not itself front matter/TOC. This is the strongest
    deterministic signal available from text extraction alone; the render
    experiment (``render_experiments`` field, when requested) gives the
    exact, measured page-count cost instead of this proxy.
    """
    by_number = {p.number: p for p in pages}
    flagged = []
    for chapter in chapters:
        start = chapter["start_page"]
        preceding = by_number.get(start - 1)
        if preceding is None:
            continue
        if preceding.category != "chapter_content":
            continue  # book opener (chapter 1) — preceded by front matter, not a prior chapter's tail
        if preceding.is_near_empty:
            flagged.append(
                {
                    "chapter_number": chapter["number"],
                    "preceding_page": preceding.number,
                    "preceding_page_words": preceding.word_count,
                }
            )
    return {
        "method": (
            "proxy: page immediately before each chapter opener, flagged when it belongs to the "
            "preceding chapter's own content and has fewer than near_empty_max_words words. "
            "No true zero-word page was found in this corpus (see totals.blank_pages), so a "
            "literal 'inserted filler page' count is not meaningful here; this proxy measures "
            "pages made functionally sparse by the recto requirement redistributing content. "
            "See render_experiments.no_recto_right_hand for the exact measured page-count cost."
        ),
        "chapter_openers_total": len(chapters),
        "flagged_preceding_pages": len(flagged),
        "flagged": flagged,
    }


def _forced_break_report(full_html: str, pages: list[PageRecord]) -> dict:
    project_entries = sorted({p.project_slug for p in pages if p.project_slug})
    project_trailing_waste = []
    for slug in project_entries:
        slug_pages = sorted((p for p in pages if p.project_slug == slug), key=lambda p: p.number)
        if len(slug_pages) > 1:
            trailing = slug_pages[-1]
            if trailing.is_very_sparse:
                project_trailing_waste.append({"project_slug": slug, "page": trailing.number, "words": trailing.word_count})
    return {
        "method": (
            "html_occurrences: literal count of each forced-break class in the canonical "
            "full_html. project_trailing_sparse_pages: project entries whose LAST physical page "
            "is < very_sparse_max_words words, evidence that .project-entry's break-before:page "
            "starts a new page before the previous project's content filled one — see "
            "render_experiments.no_project_forced_break for the measured page-count cost."
        ),
        "html_occurrences": {
            "chapter-break (div.chapter-break)": full_html.count('class="chapter-break"')
            + full_html.count('"toc-page chapter-break"'),
            "project-entry (div.project-entry)": full_html.count('class="project-entry"'),
        },
        "project_entries_total": len(project_entries),
        "project_trailing_sparse_pages": len(project_trailing_waste),
        "project_trailing_waste": project_trailing_waste,
    }


def _count_compare_table_rows(full_html: str) -> int:
    """``.compare-table tr`` is a descendant selector: the rule applies to
    every <tr> INSIDE a compare-table, not to the table element itself (that
    element carries the class; its rows never do). Counting `class="compare-
    table"` occurrences would silently report the table count instead."""
    row_count = 0
    for table_html in re.findall(r'<table class="compare-table"[^>]*>.*?</table>', full_html, re.DOTALL):
        row_count += len(re.findall(r"<tr[ >]", table_html))
    return row_count


def _break_inside_avoid_report(full_html: str) -> dict:
    report = {}
    for selector in BREAK_INSIDE_AVOID_SELECTORS:
        if selector == ".compare-table tr":
            report[selector] = {"html_occurrences": _count_compare_table_rows(full_html)}
            continue
        class_name = selector.split()[0].lstrip(".")
        pattern = re.compile(rf'class="[^"]*\b{re.escape(class_name)}\b[^"]*"')
        report[selector] = {"html_occurrences": len(pattern.findall(full_html))}
    return report


def _component_report(full_html: str) -> dict:
    def count_class(name: str) -> int:
        return len(re.findall(rf'class="[^"]*\b{re.escape(name)}\b[^"]*"', full_html))

    return {
        "code_block": {"count": count_class("code-block")},
        "callout": {"count": count_class("callout")},
        "exercise": {"count": count_class("exercise")},
        "summary_box": {"count": count_class("summary-box")},
        "cvm_comparison": {"count": count_class("cvm")},
        "notebook_card": {"count": count_class("notebook-card")},
        "chapter_figure": {
            "total": count_class("chapter-figure"),
            "narrow": count_class("chapter-figure--narrow"),
            "medium": count_class("chapter-figure--medium"),
            "wide": count_class("chapter-figure--wide"),
        },
        "compare_table": {"count": count_class("compare-table")},
        "idx_entry": {"count": count_class("idx-entry")},
    }


def _geometry_report() -> dict:
    """Pure arithmetic from the canonical @page rule
    (book_shared.build_print_css) — no rendering needed."""
    page_width_mm, page_height_mm = 152.0, 229.0
    margin_top_mm, margin_right_mm, margin_bottom_mm, margin_left_mm = 24.0, 20.0, 26.0, 20.0
    text_width_mm = page_width_mm - margin_left_mm - margin_right_mm
    text_height_mm = page_height_mm - margin_top_mm - margin_bottom_mm
    font_size_pt, line_height_ratio = 10.3, 1.48
    line_height_pt = font_size_pt * line_height_ratio
    text_height_pt = text_height_mm * 72 / 25.4
    return {
        "page_width_mm": page_width_mm,
        "page_height_mm": page_height_mm,
        "margin_top_mm": margin_top_mm,
        "margin_right_mm": margin_right_mm,
        "margin_bottom_mm": margin_bottom_mm,
        "margin_left_mm": margin_left_mm,
        "text_width_mm": round(text_width_mm, 2),
        "text_height_mm": round(text_height_mm, 2),
        "text_area_pct_of_physical_page": round(
            100 * (text_width_mm * text_height_mm) / (page_width_mm * page_height_mm), 2
        ),
        "font_size_pt": font_size_pt,
        "line_height_ratio": line_height_ratio,
        "line_height_pt": round(line_height_pt, 3),
        "estimated_lines_per_page": round(text_height_pt / line_height_pt, 2),
    }


# ---------------------------------------------------------------------------
# Render experiments (opt-in, slow): measured, not guessed, page-count deltas.
# ---------------------------------------------------------------------------

# M02-I07 Phase 2A measured five levers by diffing them against the PRE-
# Phase-2B baseline: recto->page, project-hero 62mm->45mm, font 10.3->9.8pt,
# and line-height 1.48->1.35 were all proposals to CHANGE the then-current
# CSS. Phase 2B (this pipeline's current baseline) already ships four of
# those five changes (recto relaxation, project-hero 45mm, font 9.8pt,
# line-height 1.40 — a more conservative value than the 1.35 Phase 2A
# measured, per the Phase 2B ticket's explicit instruction). Re-running
# those experiments against the NEW baseline would try to patch CSS text
# that no longer exists (there is no more "break-before: right" or "62mm"
# or "10.3pt" to remove) — they were retired, not "still testing something",
# once their proposal shipped. Only levers Phase 2B deliberately did NOT
# implement remain as live experiments below: the .project-entry forced
# break was explicitly KEPT this pass (see the Phase 2B ticket's PROJECT
# ENTRY POLICY), and the break-inside:avoid family was only PARTIALLY
# addressed (code blocks over the 18-line threshold split; everything else,
# including short code blocks and all callouts, still avoids breaking).
RENDER_EXPERIMENTS: dict[str, list[tuple[str, str]]] = {
    "no_project_forced_break": [
        (".project-entry { break-before: page; }", ".project-entry { break-before: auto; }"),
    ],
    "no_break_inside_avoid": [
        (selector_css.replace("avoid", "auto", 1), selector_css)  # placeholder, filled below
        for selector_css in ()
    ],
    # Isolate the two highest-frequency break-inside:avoid components
    # individually (see the M02-I07 Phase 2A report, section 8): the
    # combined no_break_inside_avoid ceiling above does not by itself say
    # which selector accounts for how much of it. Post-Phase-2B, this now
    # measures the REMAINING ceiling (code blocks at/under the 18-line
    # splittable threshold, plus every callout regardless of size).
    "no_callout_avoid": [
        (
            ".callout { border: 1px solid var(--color-border-default); border-left: 3.5pt solid var(--color-brand-blue); border-radius: var(--radius-md); padding: 4pt 10pt; margin: 5pt 0; background: var(--color-bg-surface); break-inside: avoid; }",
            ".callout { border: 1px solid var(--color-border-default); border-left: 3.5pt solid var(--color-brand-blue); border-radius: var(--radius-md); padding: 4pt 10pt; margin: 5pt 0; background: var(--color-bg-surface); break-inside: auto; }",
        ),
    ],
    "no_code_block_avoid": [
        (
            ".code-block { border: 1px solid var(--color-border-default); border-radius: var(--radius-md); margin: 10pt 0; break-inside: avoid; overflow: hidden; }",
            ".code-block { border: 1px solid var(--color-border-default); border-radius: var(--radius-md); margin: 10pt 0; break-inside: auto; overflow: hidden; }",
        ),
    ],
}

_BREAK_INSIDE_AVOID_CSS_LINES = (
    ".code-block { border: 1px solid var(--color-border-default); border-radius: var(--radius-md); margin: 10pt 0; break-inside: avoid; overflow: hidden; }",
    ".callout { border: 1px solid var(--color-border-default); border-left: 3.5pt solid var(--color-brand-blue); border-radius: var(--radius-md); padding: 4pt 10pt; margin: 5pt 0; background: var(--color-bg-surface); break-inside: avoid; }",
    ".exercise { border: 1px solid var(--color-border-default); border-radius: var(--radius-md); padding: 4pt 10pt; margin: 5pt 0; break-inside: avoid; }",
    ".summary-box { background: var(--color-bg-surface); border-radius: var(--radius-lg); padding: 5pt 12pt; margin: 6pt 0; break-inside: avoid; }",
    ".cvm { border: 1px solid var(--color-border-default); border-radius: var(--radius-md); margin: 8pt 0; break-inside: avoid; overflow: hidden; }",
    ".chapter-figure { margin: 10pt auto; break-inside: avoid; }",
    ".idx-entry { display: flex; justify-content: space-between; gap: 6pt; padding: 3pt 0; font-size: 9pt; border-bottom: 1px dotted var(--color-border-default); break-inside: avoid; }",
    ".notebook-card { border: 1px solid var(--color-border-default); border-left: 3.5pt solid var(--blue-300); border-radius: var(--radius-md); padding: 6pt 10pt; margin: 8pt 0; break-inside: avoid; background: var(--color-bg-surface); }",
    ".compare-table tr { break-inside: avoid; }",
)
RENDER_EXPERIMENTS["no_break_inside_avoid"] = [
    (line, line.replace("break-inside: avoid", "break-inside: auto")) for line in _BREAK_INSIDE_AVOID_CSS_LINES
]


def run_render_experiments(config: BookLocaleConfig, model: CanonicalBookModel) -> dict:
    """Re-render the canonical full_html with one targeted CSS rule swapped
    at a time and measure the resulting WeasyPrint page count. Slow (each
    variant re-renders the entire book); never writes to any artifact or to
    book_shared.py — the patch is applied to an in-memory CSS string only,
    for the lifetime of one variant's render.

    Requires the ``weasyprint`` extra (already a build-time dependency; not
    imported at module load time so the fast artifact-analysis path never
    needs it installed).
    """
    import os

    os.environ.setdefault("FONTCONFIG_FILE", str(bs.FONTCONFIG_POLICY_PATH))
    os.environ.setdefault("SOURCE_DATE_EPOCH", bs.PDF_SOURCE_DATE_EPOCH)
    from weasyprint import HTML

    from . import pdf_adapter

    original_build_print_css = bs.build_print_css

    def render_with(patches: list[tuple[str, str]] | None) -> int:
        if patches is None:
            bs.build_print_css = original_build_print_css
        else:
            def patched(*, book_title, page_abbrev):
                css = original_build_print_css(book_title=book_title, page_abbrev=page_abbrev)
                for old, new in patches:
                    if old not in css:
                        raise RuntimeError(f"render-experiment patch target not found in CSS: {old[:60]!r}")
                    css = css.replace(old, new, 1)
                return css

            bs.build_print_css = patched
        try:
            full_html, *_ = pdf_adapter.build_full_html(model, config)
            return len(HTML(string=full_html, base_url=str(config.site)).render().pages)
        finally:
            bs.build_print_css = original_build_print_css

    results = {"baseline": render_with(None)}
    for name, patches in RENDER_EXPERIMENTS.items():
        results[name] = render_with(patches)
    baseline = results["baseline"]
    deltas = {name: value - baseline for name, value in results.items() if name != "baseline"}
    return {
        "note": (
            "weasyprint_pages excludes the merged cover page (add 1 for the final PDF's physical "
            "page count). page_delta_vs_baseline is negative when the variant produces FEWER pages. "
            "page_delta_pct_vs_baseline is that delta as a percentage of the baseline page count."
        ),
        "weasyprint_pages": results,
        "page_delta_vs_baseline": deltas,
        "page_delta_pct_vs_baseline": {name: round(100 * delta / baseline, 2) for name, delta in deltas.items()},
    }


def analyze(language: str, *, run_render_experiments_flag: bool = False) -> dict:
    """The one canonical diagnostics entry point. Same implementation for
    every language — ``language`` only selects the BookLocaleConfig; there
    is no per-language branch anywhere in this module."""
    inputs = _load_inputs(language)
    pages = _classify_pages(inputs)

    from . import pdf_adapter

    full_html, *_ = pdf_adapter.build_full_html(inputs.model, inputs.config)
    chapters = _chapter_diagnostics(pages, inputs.pagination_meta)

    import hashlib

    report = {
        "schema_version": SCHEMA_VERSION,
        "language": language,
        "pdf_path": str(inputs.config.pdf_output_path.relative_to(ROOT)),
        "pdf_sha256": hashlib.sha256(inputs.config.pdf_output_path.read_bytes()).hexdigest(),
        "pagination_source_path": str(inputs.config.pagination_output_path.relative_to(ROOT)),
        "thresholds": THRESHOLDS,
        "totals": _totals(pages),
        "category_totals": _category_totals(pages),
        "category_word_stats": _category_word_stats(pages),
        "chapters": chapters,
        "recto_policy": _recto_policy_report(pages, chapters),
        "forced_page_breaks": _forced_break_report(full_html, pages),
        "break_inside_avoid": _break_inside_avoid_report(full_html),
        "components": _component_report(full_html),
        "geometry": _geometry_report(),
        "pages": [p.to_dict() for p in pages],
    }
    if run_render_experiments_flag:
        report["render_experiments"] = run_render_experiments(inputs.config, inputs.model)
    return report
