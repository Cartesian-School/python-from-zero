# M03-I02 Step 1 — Canonical Geometry Controlled Baseline

Milestone: **M03-I02 — Structural Page-Cost Elimination**
Step: **Step 1 — measurement only**
Source main SHA: `4cbe39fd583f31393d6a4a5c96681eb23028b096`
Feature branch: `feat/m03-i02-structural-page-cost` (created from the same SHA, no drift)
Canonical pipeline entry point: `scripts/build_book.py` → `book_pipeline.build_book(language, output_format)` (`scripts/book_pipeline/pipeline.py`)

This is a measurement step. **No claim of success toward the 850–1000 page
target is made.** No educational content, translation, or locale-specific
layout logic was touched.

## 1. Root-cause fix: one source of truth for print-layout metrics

M03-I01 audit finding P-1: `pagination_diagnostics._geometry_report()`
independently hardcoded stale production assumptions
(`font_size_pt=10.3, line_height_ratio=1.48`) that had drifted from the print
CSS's actual shipped values (`9.8pt/1.26`).

Fix: `scripts/book_shared.py` now declares one canonical, language-independent
set of print-layout constants —

```
PRINT_PAGE_WIDTH_MM = 152.0
PRINT_PAGE_HEIGHT_MM = 229.0
PRINT_MARGIN_TOP_MM = 24.0
PRINT_MARGIN_RIGHT_MM = 20.0
PRINT_MARGIN_BOTTOM_MM = 26.0
PRINT_MARGIN_LEFT_MM = 20.0
PRINT_BODY_FONT_SIZE_PT = 9.8
PRINT_BODY_LINE_HEIGHT_RATIO = 1.26
```

`build_print_css()` now interpolates these constants into its `@page`/`body`
CSS template (previously hardcoded literals); `pagination_diagnostics.
_geometry_report()` now reads the same constants via `bs.PRINT_*` instead of
its own local, independently-drifting literals. The two can now never
silently diverge again — there is exactly one place these numbers live.

Verified: the generated print CSS is **byte-identical** before and after this
refactor (diffed the full `build_print_css()` output against the pre-change
source).

## 2. Baseline geometry (current production, legacy)

| | Value |
|---|---|
| Page size | 152 × 229 mm |
| Margins (top/right/bottom/left) | 24 / 20 / 26 / 20 mm |
| Margin scheme | Uniform — not mirrored by recto/verso |
| Body typography (held constant in this experiment) | 9.8pt / 1.26 line-height |

## 3. Experimental geometry (Product-Owner-approved canonical M03 target)

| | Value |
|---|---|
| Page size | 165 × 235 mm |
| Recto (right) margin (top/outer/bottom/inner) | 18 / 15 / 20 / 20 mm |
| Verso (left) margin (top/inner/bottom/outer) | 18 / 20 / 20 / 15 mm |
| Margin scheme | Genuinely mirrored recto/verso |
| Nominal text measure | ~130 mm |
| Body typography | Unchanged — 9.8pt / 1.26 |

Implemented as one new entry (`canonical_165x235_mirrored_geometry`) in the
existing `book_pipeline.pagination_diagnostics.RENDER_EXPERIMENTS` harness —
**not** a new publisher, script, or per-locale CSS file. The patch touches
only the `@page` size rule and the `@page :left`/`@page :right` margin
declarations; it does not touch any heading, code, callout, or component
rule.

## 4. Measured results — actual WeasyPrint renders, both languages

Measured via `book_pipeline.pagination_diagnostics.run_render_experiments()`,
which re-renders the exact canonical `pdf_adapter.build_full_html()` output
through real WeasyPrint, once per variant. No extrapolation.

### RU

| | Pages (WeasyPrint, pre-cover) | Pages (final PDF, +1 cover) |
|---|---:|---:|
| Baseline (152×229mm) | 2096 | **2097** (matches committed artifact) |
| Canonical geometry (165×235mm mirrored) | 1766 | **1767** |
| **Delta** | **−330** | **−330 (−15.74%)** |

### PL

| | Pages (WeasyPrint, pre-cover) | Pages (final PDF, +1 cover) |
|---|---:|---:|
| Baseline (152×229mm) | 2034 | **2035** (matches committed artifact) |
| Canonical geometry (165×235mm mirrored) | 1726 | **1727** |
| **Delta** | **−308** | **−308 (−15.14%)** |

Both baseline renders reproduce the currently-committed PDF page counts
exactly (RU 2097, PL 2035) — confirming this measurement run is representative
of current production, not a stale or drifted baseline.

### Supplementary diagnostics (fast artifact-analysis path, current committed PDFs)

| | RU | PL |
|---|---:|---:|
| Chapter-opener physical pages (24 chapters) | 38 | 38 |
| Chapter-content physical pages | 2033 | 1971 |
| Mean words/page | 109.45 | 111.83 |
| Median words/page | 109 | 111 |
| Near-empty pages | 55 | 49 |

### Other render-experiment levers measured in the same run (for context only — not promoted, not new this round)

| Experiment | RU pages | PL pages |
|---|---:|---:|
| `no_project_forced_break` | 2095 | 2032 |
| `no_break_inside_avoid` | 2014 | 1956 |
| `no_callout_avoid` | 2076 | 2015 |
| `no_code_block_avoid` | 2061 | 1996 |

## 5. Target status

Product Owner target: **850–1000 pages per language, nominal ≈900**
(inherited from the M03-I01 audit correction; BBPC-001 §17's 600–800 figure
remains a separate, unamended governance item).

**Not yet reached.** Geometry alone moves RU from 2097 → 1767 and
PL from 2035 → 1727 — a real, substantial, measured ~15% reduction, but both
remain well above the 850–1000 target. This confirms the M03-I01 audit's own
prior finding: geometry change is necessary but not sufficient; further
structural page-cost work (Step 2+) is required.

## 6. Test results

- `tests/test_m03_i02_step1_canonical_geometry.py` (new, 13 tests): all passed.
- `tests/test_pagination_diagnostics.py` (updated: `_EXPECTED_RENDER_EXPERIMENT_NAMES` now includes `canonical_165x235_mirrored_geometry`): all passed.
- Full suite `pytest tests/`: **399 passed**, 0 failed, in 309.95s.

## 7. Explicit confirmations

- No educational content changed.
- No translation changed.
- No language-specific layout fork created (`RENDER_EXPERIMENTS` is one shared dict; the experiment name carries no `_ru`/`_pl` suffix; `build_print_css()` still takes no language parameter).
- No new publisher script or per-locale CSS file created (`build_pdf_165.py`, `book_ru_165.css`, etc. — none exist).
- Canonical publication artifacts untouched: `book/pdf/*.pdf`, `book/epub/*.epub`, `data/book-pagination*.json` were not written to by this measurement (verified via `git status --short`).
- Production canonical geometry is **unchanged** this round — `book_shared.PRINT_*` constants still equal the legacy 152×229mm/24-20-26-20mm/9.8pt/1.26 baseline; the 165×235mm mirrored geometry exists only as an opt-in diagnostics experiment.
- `docs/contracts/BOOK-BUILD-PIPELINE-CONTRACT.md` not modified.
- Figma not touched. Cover and End Page not touched.

## 8. Exact files changed this step

- `scripts/book_shared.py`
- `scripts/book_pipeline/pagination_diagnostics.py`
- `tests/test_pagination_diagnostics.py`
- `tests/test_m03_i02_step1_canonical_geometry.py`
- `evidence/m03/m03-i02-step1-canonical-geometry-baseline.md`
- `evidence/m03/m03-i02-step1-canonical-geometry-baseline.json`
