# M03-I02 Step 2A — Production Geometry Promotion

Milestone: **M03-I02 — Structural Page-Cost Elimination**
Step: **Step 2A — promote the approved canonical geometry to production**
Branch: `feat/m03-i02-structural-page-cost`
Main SHA: `4cbe39fd583f31393d6a4a5c96681eb23028b096`
Step 1 commit: `bc472b85c8b3570bbae18a9b5f01b91af4aa408d`
Canonical pipeline entry point: `scripts/build_book.py` → `book_pipeline.build_book(language, output_format)`

## 1. Geometry decision

| | Old production | New production (this step) |
|---|---|---|
| Page size | 152 × 229 mm | **165 × 235 mm** |
| Margins | 24 / 20 / 26 / 20 mm (uniform) | top 18mm, bottom 20mm, **inner 20mm, outer 15mm** (genuinely mirrored) |
| Text measure | ~112 mm | **130 mm** (matches Book Design System v1 exactly) |
| Body typography | 9.8pt / 1.26 | Unchanged — 9.8pt / 1.26 |

Source of approval: **Book Design System v1** and the **binding Product Owner decisions recorded in the M03-I01 audit (Issue #123)** — not `BBPC-001`, which defines canonical pipeline *architecture*, never physical trim dimensions. This mis-attribution in Step 1's diagnostics comment has been corrected.

**Semantic source-of-truth refactor**: `scripts/book_shared.py`'s `PRINT_MARGIN_LEFT_MM`/`PRINT_MARGIN_RIGHT_MM` constants (the wrong abstraction for a mirrored, physically-bound book) were replaced with `PRINT_MARGIN_INNER_MM` (20mm) / `PRINT_MARGIN_OUTER_MM` (15mm). The renderer derives the actual per-side CSS margin from page position:

- **Verso (left-hand) page** — spine on the right: `margin: 18mm 20mm 20mm 15mm` (top / inner-right / bottom / outer-left)
- **Recto (right-hand) page** — spine on the left: `margin: 18mm 15mm 20mm 20mm` (top / outer-right / bottom / inner-left)

No locale-specific geometry was introduced; both constants are read by `build_print_css()` for both RU and PL, verified identical (`test_ru_and_pl_produce_the_same_production_geometry`).

## 2. Diagnostics model updated

- `pagination_diagnostics._geometry_report()` now reports `margin_inner_mm`/`margin_outer_mm` (not `margin_left_mm`/`margin_right_mm`), reading `book_shared.PRINT_*` directly — same single-source-of-truth pattern Step 1 established, extended to the new semantics.
- The Step 1 `canonical_165x235_mirrored_geometry` render experiment was **removed** — once production geometry *is* the approved value, patching production's own `@page` rule to itself is a no-op comparison. `RENDER_EXPERIMENTS` now contains exactly the four real, still-unpromoted structural levers: `no_project_forced_break`, `no_break_inside_avoid`, `no_callout_avoid`, `no_code_block_avoid` — untouched, measurement tools only, not implemented this round.

## 3. Build commands (canonical entry point only)

```
python scripts/build_book.py --all                                    # pass 1
python -c "...build_book(language='ru', output_format='epub')"        # retry, transient failure
python scripts/build_book.py --language pl --format all               # pass 1 continuation
python -c "...build_book(language='pl', output_format='epub')"        # retry, transient failure

# pagination-dependency closure (see §5)
python scripts/build_chapter_01.py .. build_chapter_24.py
python scripts/build_site_index.py
python scripts/build_polish_course.py
python scripts/inject_language_switchers.py
python scripts/build_seo_meta.py
python scripts/build_front_matter_pl.py
python scripts/build_license_page_pl.py
python scripts/build_llms_pl.py

python scripts/build_book.py --all                                    # pass 2, FINAL
python -c "...build_book(language='ru'/'pl', output_format='epub')"   # retries, transient failure
```

## 4. Transient build failure (recorded, not hidden)

Both languages' EPUB builds failed on **every** first attempt in **both** passes with `'H' format requires 0 <= number <= 65535`, then succeeded cleanly on an immediate retry through the same canonical entry point — 4/4 retries succeeded on the first try. This is **not deterministic**: `epub_adapter.py` was not modified, and the failure is consistent with this project's documented history of transient PDF/EPUB-toolchain flakiness under load. No code defect was found; no fix was applied to `epub_adapter.py` (which the task explicitly protects).

## 5. Pagination dependency closure

Promoting geometry changes physical PDF pagination, which several generated outputs embed as literal numbers. Traced and closed the full chain:

- **RU chapter opener/mini-TOC `si-page` labels** (`site/chapters/glava-NN/index.html`) — sourced from `scripts/book_pagination.py` reading `data/book-pagination.json` at generation time. Regenerated via all 24 `build_chapter_NN.py` scripts.
- **RU homepage page-count badge** (`site/index.html`, "Страниц в книге") — regenerated via `build_site_index.py`.
- **PL mirror of both** — PL pages carry the *same* numeric labels as RU by established design (PL's own `book_pagination` support doesn't exist; numbers are treated as verbatim/untranslated content copied from the freshly-regenerated RU source), regenerated via `build_polish_course.py`.
- **`manifest/i18n/routes.json`** — the "home" page's canonical-source binding declares `data/book-pagination.json` as a dependency; its content-fingerprint (`source.sha256`) went stale and was recomputed with the repository's own `source_hash()` algorithm (no translation/content fields touched).
- **`manifest/i18n/ru_baseline.json`** — the frozen M02 delivery baseline recorded the *old* PDF/EPUB sha256 and page count; updated to the new, intentionally-changed canonical values. `bookmarks`/`outline_top_level_entries` independently verified unchanged (heading/section structure didn't change, only geometry).
- Two idempotent post-processors (`inject_language_switchers.py`, `build_seo_meta.py`) were re-run to restore the language-switcher nav and SEO meta block that full-content regeneration strips, per the established, CI-documented ordering.
- `build_front_matter_pl.py` / `build_license_page_pl.py` / `build_llms_pl.py` were re-run to restore PL's curated front-matter/license content and llms outputs that `build_polish_course.py`'s generic translation/site-wipe pass overwrote or deleted — this is the same established CI sequence, not an ad hoc addition.

No educational prose, no translation wording, and no locale-specific layout logic were touched anywhere in this chain — verified by a systematic diff scan (see §8).

### A self-inflicted issue, found and recovered

Patching `routes.json`'s "home" `source.sha256` without also updating the PL variant's `source_sha256` field created a transient inconsistency: `localization.py`'s `effective_status()` classified PL's home variant as "stale," so `site_header()`'s language switcher rendered a disabled "translation unavailable" span on the RU homepage instead of a real link. `build_polish_course.py` then crashed translating that never-before-seen string, after already having deleted `site/pl/` (its own destructive-by-design first step) and only partially rewritten it. **Recovery**: restored `site/pl/` from git, updated *both* hash fields together, regenerated the homepage correctly (verified: real PL link, correct badge), then re-ran `build_polish_course.py` successfully end-to-end (1160/1160 pages, 493 notebooks). No corrupted state was ever committed.

## 6. Results — actual rebuilt production artifacts

| | RU | PL |
|---|---:|---:|
| Step 1 predicted final pages | 1767 | 1727 |
| **Actual final production pages** | **1767** | **1727** |
| Prediction vs. actual | **0 delta** | **0 delta** |
| Delta vs. legacy (2097 / 2035) | −330 (−15.74%) | −308 (−15.14%) |
| Expected band (±3 pages) | 1764–1770 ✅ | 1724–1730 ✅ |
| Mean words/page | 128.87 | 130.78 |
| Median words/page | 128 | 128 |
| Near-empty pages | 41 | 38 |
| Very sparse (<50 words) pages | 108 | 98 |
| Blank pages | 0 | 0 |
| Chapter-opener physical pages (24 chapters) | 33 | 32 |
| Chapter-content physical pages | 1709 | 1670 |

Both languages landed **exactly** on the Step 1 predicted values — no material difference, no root-cause investigation required. Chapter-opener overhead dropped from 38→33 (RU) / 38→32 (PL), a side effect of the larger page absorbing more opener-intro prose onto a single page.

## 7. Validation

- `python scripts/validate_book.py` — **PASS**: RU PDF 1767 pages/1221 bookmarks, RU EPUB epubcheck 0 errors, PL PDF 1727 pages/1221 bookmarks, PL EPUB epubcheck 0 errors; both language checks passed.
- `python scripts/validate_pagination.py` — **PASS**: 24 chapters, 1767 physical pages, PDF/TOC/site consistent.
- `pytest tests/` — first run: **399 passed, 1 failed** (`test_localization.py::test_frozen_baseline` — expected: the frozen PDF/EPUB sha256 baseline predates this intentional rebuild). Fixed by updating `manifest/i18n/ru_baseline.json`'s `pdf.pages`/`pdf.sha256`/`epub.sha256` fields. Final run: **400 passed, 0 failed** (255.89s).

## 8. Content-integrity verification

Every one of the 1225 changed files was scanned programmatically: each diff line was normalized against known-safe patterns (`si-page">N<` numeric spans, `СТР./STRONA N` chapter-num labels, the homepage page-count badge, and the link-position/attribute-order noise produced by re-running the existing idempotent switcher/SEO injectors) and paired against its counterpart. **Zero unpaired prose or translation-content lines were found** across the full `site/` and `manifest/` diff — every remaining change is a numeric page-reference update or a benign structural re-serialization already established as correct by a prior commit (`0aadfd6d`, which fixed this exact injection-order question).

## 9. Exact files changed

- `scripts/book_shared.py`, `scripts/book_pipeline/pagination_diagnostics.py` (geometry implementation)
- `tests/test_m03_i02_step1_canonical_geometry.py`, `tests/test_pagination_diagnostics.py`, `tests/test_phase2b_pagination_remediation.py`, `tests/test_phase2c_a_typographic_compaction.py`
- `manifest/i18n/routes.json`, `manifest/i18n/ru_baseline.json`
- `data/book-pagination.json`, `data/book-pagination-pl.json`
- `book/pdf/python-s-nulya-ru.pdf`, `book/pdf/python-od-zera-pl.pdf`, `book/epub/python-s-nulya-ru.epub`, `book/epub/python-od-zera-pl.epub`
- `site/index.html`, `site/chapters/**/*.html` (561 files), `site/pl/**/*.html` (649 files) — pagination-label synchronization only
- `evidence/m03/m03-i02-step2a-production-geometry-promotion.md`, `.json`

## 10. Explicit statements

- **No educational content was changed.** No prose, no examples, no exercises, no diagrams.
- **No translation wording was changed.** PL content changes are exclusively numeric page-reference labels mirroring the updated RU source, per the pre-existing, established mechanism.
- **Step 2B was not started.** No fragmentation/break-inside tuning, no chapter-opener structural optimization, no table/figure/code-block tuning, no widow/orphan changes. The four real structural render-experiments remain declared but unexecuted measurement tools only.
