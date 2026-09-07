# M02-I07 Phase 2A — PDF Pagination Diagnostics and Root-Cause Evidence

**Branch:** `feat/m02-i07-book-pagination-remediation`
**Contract:** `docs/contracts/BOOK-BUILD-PIPELINE-CONTRACT.md`
**Status:** Diagnostic only. No publishing behavior, pagination rule, typography value, or educational content was changed. `book/pdf/*.pdf`, `book/epub/*.epub`, and `data/book-pagination*.json` are byte-identical to the M02-I06 baseline.

Machine-readable evidence: `evidence/m02-i07-pagination-diagnostics-ru.json`, `evidence/m02-i07-pagination-diagnostics-pl.json` (full per-page and per-chapter records; the numbers below are pulled directly from those files).

## Methodology, in one paragraph

Two measurement tiers were used, both implemented in `scripts/book_pipeline/pagination_diagnostics.py` (one canonical implementation, `language` is a parameter — no RU/PL fork). **Tier 1 (artifact analysis, fast, ~70s/book):** reads the already-built, already-committed PDF (per-page text extraction + its outline/bookmarks) and its pagination sidecar (`data/book-pagination*.json`), which the pipeline itself already treats as the authoritative physical page tree. Every physical page is classified into exactly one category; word/character counts come from `pypdf` text extraction. **Tier 2 (render experiments, slow, ~90-140s/variant, opt-in via `--render-experiments`):** re-renders the canonical `pdf_adapter.build_full_html()` output with exactly one CSS rule swapped at a time (e.g. `.chapter-hero`'s `break-before: right` → `break-before: page`), entirely in memory, and measures the resulting WeasyPrint page count. This turns "how much does this rule cost" from a guess into a measurement. Nothing in either tier writes to a committed artifact or to `book_shared.py`.

## 1. Executive summary

- RU is 2519 physical pages, PL is 2429. **Zero pages in either book have zero extracted words under raw PDF text extraction.** Raw extraction includes running headers and folios (see the Methodology and section 4), so this proves only "no page is entirely without extractable text of any kind" — it does **not** by itself prove no page is visually or body-empty. A stricter, chrome-stripped secondary check (below) found the same result — but with a documented partial limitation, not a definitive visual-blank determination. Either way, the popular "the book is full of blank pages" framing does not match the evidence found here.
- A secondary metric strips the two chrome elements identifiable with certainty (the page's own folio, and the constant book-title running header) before recounting words: **zero pages are "body-effectively-empty" under this stricter check either**, in both RU and PL. This check is still partial — it cannot strip the *dynamic* per-page chapter/lesson-title running header — so it can undercount but never overcount relative to a true visual-blank page; see section 4 for the full caveat.
- Instead, the corpus has a large population of **functionally sparse pages**: 111 RU / 105 PL pages under 25 words, 308 RU / 286 PL under 50 words, and roughly **57% of all pages (1431/2519 RU, 1324/2429 PL) are under 100 words** — driven overwhelmingly by pagination *rules*, not by empty space with nothing on it.
- The single largest **measured, isolatable** lever found is **`.code-block { break-inside: avoid }`**: removing it alone saves **70 pages in RU (-2.8%)** and **66 in PL (-2.7%)** — roughly half of the entire break-inside-avoid family's combined ceiling.
- The recto (`break-before: right`) chapter-opener policy and the `.project-entry` forced page break are real but **small**: 11 and 8 pages in RU (13 and 7 in PL) respectively — well under 1% of the book each. A separate, isolated experiment on the `.project-hero` graphic's fixed height (62mm → 45mm, keeping the forced break) measured **-9 pages in RU** (see section 7 for the PL figure, and for why this is a distinct mechanism from the forced-break removal, not the same 8/7 pages counted twice).
- **600-800 pages is not achievable through pagination-rule or typography tuning alone**, at any combination measured here. The book's actual body-text volume (≈232,000 words per language) would require roughly **330 words per physical page** to land in that range — a ~3.6× density increase over the current ~93 words/page median. See section 17.
- Every finding below was cross-checked between RU and PL and found **consistent within a few percentage points**, confirming the CSS architecture (not content, not language) drives the pagination behavior — exactly what the M02-I06 language-independence contract predicts.

## 2. Current page-count baseline

| | RU | PL |
|---|---:|---:|
| Total physical pages | 2519 | 2429 |
| PDF SHA-256 | `60e512cf6f...4720a` | `bc7e51a3b7...8b11cb` |
| Total extracted words (all pages, includes running-header/folio bleed — see Limitations) | 232,201 | 230,053 |
| Mean words/page | 92.18 | 94.71 |
| Median words/page | 93 | 95 |
| Chapters | 24 | 24 |
| Projects | 13 | 13 |

## 3. Page-density distribution

| Metric | RU | PL |
|---|---:|---:|
| p10 words/page | 46.0 | 46.0 |
| p25 words/page | 68.0 | 70.0 |
| median | 93 | 95 |
| p75 words/page | 118.0 | 120.0 |
| p90 words/page | 140.0 | 145.0 |
| max words/page | 211 | 218 |
| mean chars/page | 665.6 | 690.8 |
| pages < 25 words | 111 (4.4%) | 105 (4.3%) |
| pages < 50 words | 308 (12.2%) | 286 (11.8%) |
| pages < 100 words | 1431 (56.8%) | 1324 (54.5%) |
| pages < 150 words | 2364 (93.8%) | 2245 (92.4%) |

The distribution is unimodal and fairly narrow (p25-p75 spans only 50 words in both books) — there is no single dominant spike of near-zero pages; the mass under 100 words is spread broadly, consistent with a *structural* (rule-driven) cause rather than a handful of isolated defects.

## 4. Blank and near-empty pages

Thresholds (defined in code, `book_pipeline.pagination_diagnostics.THRESHOLDS`, reported verbatim):

```
blank_max_words:          0   (<= 0 words)
near_empty_max_words:    25   (< 25 words)
very_sparse_max_words:   50   (< 50 words)
sparse_max_words:       100   (< 100 words)
extended_sparse_max_words: 150 (< 150 words)
```

**`blank_pages` (raw pypdf extraction): 0 in both RU and PL.** This metric counts pages with zero words under raw text extraction, which includes the page's running header (chapter-title string-set, uppercase) and/or footer folio. **Zero zero-text pages were observed under raw PDF extraction; because running headers/folios contribute text, this metric cannot by itself exclude body-empty or visually blank pages** — a page whose entire "content" is a running header and a folio number would still show a non-zero raw word count and would not be flagged by `blank_pages` alone.

**Secondary check — `body_effectively_empty_pages`: also 0 in both RU and PL.** To close part of that gap, a second metric (`PageRecord.is_body_effectively_empty` / `_strip_known_page_chrome`) strips the two chrome elements identifiable with certainty from the canonical print CSS before recounting words: (1) the page's own folio (an exact match against that page's own number), and (2) the constant book-title running header shown on right-hand pages (an exact, page-independent string). It deliberately does **not** attempt to strip the *dynamic* chapter/lesson-title running header shown on left-hand pages (`string(chaptitle)`, i.e. whichever `<h1>` most recently rendered) — that text varies per physical page and is not reliably reconstructible from the committed artifacts without tracking every source page's own heading position, which is out of scope for this phase. Because this strip is partial, `body_effectively_empty_pages` can only ever be greater than or equal to the true count of visually-empty pages — it can undercount, never overcount. Finding it at 0 as well is meaningful corroborating evidence, but **visual-blank determination remains formally unresolved** by this audit; a definitive answer would require a pixel-coverage or WeasyPrint box-geometry pass, which is out of scope here.

Known limitation (documented per the task's explicit requirement): text extraction cannot see icon-only or checkbox-only list content, and the partial chrome-strip above cannot see the dynamic per-page running header either. One concrete instance was found and manually verified (RU page 43, chapter 1's "Как получить максимум от этой книги" sub-lesson): the page's raw extracted text is only its heading (the dynamic running-header case the strip does not cover) + folio, while the preceding page ends with two bullet markers (`•`) whose label text did not extract at all — the page is plausibly not visually blank, just under-counted by both metrics. This is a real, acknowledged blind spot; it does not change any of the CSS-rule-driven findings below, which are corroborated by the independent render-experiment measurements.

## 5. Chapter-level density

Chapters with the lowest words-per-page (both books independently agree on the pattern: Turtle-graphics-heavy and file/Tkinter-heavy chapters are the least dense, correlating with `.chapter-figure` usage — see section 11):

**RU**, lowest mean words/page:

| Ch. | Title | Pages | Words/page | Total words |
|---:|---|---:|---:|---:|
| 7 | Глубокое погружение в Turtle | 130 | 67.78 | 8,811 |
| 12 | Множество увлекательных мини-проектов! | 92 | 77.35 | 7,116 |
| 6 | Рисуем классные вещи с помощью Turtle | 88 | 77.64 | 6,832 |
| 16 | Создаём классные приложения с Tkinter | 152 | 81.17 | 12,338 |
| 15 | Python и файлы | 128 | 81.21 | 10,395 |

**PL**, lowest mean words/page:

| Ch. | Title | Pages | Words/page | Total words |
|---:|---|---:|---:|---:|
| 16 | Twórz fajne aplikacje za pomocą Tkinter | 148 | 82.89 | 12,268 |
| 15 | Python i akta | 124 | 83.85 | 10,398 |
| 4 | Python lubi liczby | 78 | 85.26 | 6,650 |
| 11 | Dużo informacji! | 102 | 87.13 | 8,887 |

Chapter 7 (Turtle deep-dive, RU) is the single lowest-density chapter found and also has the worst pages-per-1000-words ratio (14.75, vs. a book median around 11-12) — it is the chapter with the heaviest concentration of full-width diagrams (`.chapter-figure`), each of which is `break-inside: avoid` and (per section 9) frequently pushed to start its own mostly-empty page.

Median chapter density across all 24 chapters is ~90.5 words/page (RU) — close to the book-wide median, meaning most chapters are unremarkable and the "lowest density" tail is a small, identifiable, figure-heavy minority, not the norm.

## 6. Recto-policy cost (measured)

Rule: `.chapter-hero { page: opener; break-before: right; }`

| | RU | PL |
|---|---:|---:|
| Chapter openers | 24 | 24 |
| **Measured page-count cost** (render experiment: `right` → `page`) | **-11 pages (-0.44%)** | **-13 pages (-0.54%)** |
| Proxy: chapter-opener-preceding pages flagged functionally sparse (< 25 words, belonging to the prior chapter) | 12 of 24 | 13 of 24 |

The measured cost (11-13 pages) is the reliable number; the proxy (which pages precede a chapter start) over- and under-counts individual chapters because content redistributes across several pages when a page is inserted, but its *count* of affected chapter boundaries (12-13 of 24, roughly half) corroborates the render measurement's order of magnitude. **This is a real but small cost: well under 1% of the book.**

Important finding while investigating this: **no page adjacent to a chapter start shows zero words under raw extraction** (consistent with section 4's `blank_pages == 0` finding). The recto requirement does not insert an obviously-empty page; the observable effect is that it forces the immediately preceding page's content to end early, so the *previous* page becomes sparser rather than a distinguishably "new" page appearing. Given section 4's caveat, this should be read as "the mechanism is real and the pages it produces are sparse, not that a definitively blank page was ruled out" — the render-experiment page-count cost above is the reliable, extraction-independent number.

## 7. Forced page-break cost (measured)

The project-entry section involves **two distinct, separately measured mechanisms** — they are not the same experiment and their page-count costs must not be added together or conflated:

**Mechanism A — `.project-entry { break-before: page; }` itself** (the forced break; 13 occurrences, RU and PL both):

| | RU | PL |
|---|---:|---:|
| **Measured page-count cost** (`break-before: page` → `auto`, hero height unchanged) | **-8 pages (-0.32%)** | **-7 pages (-0.29%)** |
| Project entries whose *last* physical page is < 50 words (direct evidence of the mechanism) | 9 of 13 | 7 of 13 |

**Mechanism B — the `.project-hero` graphic's fixed height** (62mm; a *separate* isolated experiment, forced break left in place, hero height reduced to a specific proposed value of 45mm):

| | RU | PL |
|---|---:|---:|
| **Measured page-count cost** (`.project-hero` height 62mm → 45mm, `break-before: page` unchanged) | **-9 pages (-0.36%)** | **-7 pages (-0.29%)** |

Direct textual confirmation of the underlying mechanism (RU, physical pages 2495-2496): page 2495 carries the project's title, description, and topic tags (46 words); page 2496 carries only `"Запустите локально: python paint_app.py"` plus the running header and folio (8 words total). This pattern repeats for the large majority of the 13 projects — the `.project-hero` graphic (fixed 62mm height) plus text consumes most of page 1, leaving the `.notebook-card` (itself `break-inside: avoid`) too tall to fit in the remainder, so it starts a near-empty page 2. **This is the cleanest, most visually confirmable finding in this whole audit.**

Both experiments target the *same underlying pattern* from different angles (removing the break entirely vs. leaving the break but freeing enough space that a second page is rarely needed) and, unsurprisingly, land on similar-sized but genuinely independent measurements (-8 vs -9 RU; -7 vs -7 PL). **Neither number should be read as validating the other, and a combined "do both" change has not been measured** — per section 16, effects like these should be re-measured together, not summed, before being accepted as a combined estimate.

**`.chapter-break`, `.toc-page`, `.copyright-page`, `.title-page`** (all `break-before`/`break-after: page`) are *structural*, not wasteful — they exist to give front matter, the TOC, and the projects/index sections their own starting page, exactly once each (6 `.chapter-break` divs, 1 title page, 1 copyright page). These were **not** included in the render-experiment removal set because removing them would run unrelated sections together on one page — a correctness change, not a waste-reduction one.

## 8. `break-inside: avoid` impact (measured, the single largest category)

| Selector | HTML occurrences (RU=PL, shared content structure) | Isolated measured cost (RU / PL) |
|---|---:|---:|
| `.code-block` | 1,445 | **-70 / -66 pages** |
| `.callout` | 2,832 | **-32 / -26 pages** |
| `.exercise` | 408 | not isolated — see combined below |
| `.summary-box` | 77 | not isolated |
| `.cvm` (classic-vs-modern comparison) | 200 | not isolated |
| `.chapter-figure` | 31 (23 wide, 2 narrow, 0 medium) | not isolated |
| `.idx-entry` | 70 | not isolated |
| `.notebook-card` | 506 | not isolated |
| `.compare-table tr` (rows, not tables — see note) | 1,216 rows across 257 tables | not isolated |
| **All nine selectors combined** (`break-inside: avoid` → `auto` everywhere) | — | **-141 / -129 pages (-5.6% / -5.3%)** |

`.code-block` alone accounts for **~50% of the entire combined ceiling** (70 of 141 pages, RU), despite having roughly half the occurrence count of `.callout` (1,445 vs 2,832) — code blocks are simply *taller* on average, so each one that doesn't fit the remaining page wastes more space than a typical 2-4 line callout. `.callout` accounts for a further ~23% (32 of 141). Together, code blocks and callouts explain **~72% of the entire break-inside-avoid page cost** — the remaining seven selectors combined account for only ~39 pages (~28%, or under 1.6% of the book).

**Caveat on the combined -141/-129 figure:** this is a *ceiling*, not a recommendation — it was measured by removing `break-inside: avoid` from every listed selector simultaneously and unconditionally, which would let even a 2-line code block split mid-statement across a page boundary. It quantifies the maximum theoretically recoverable space from this category; section 15's remediation plan proposes a much narrower, size-conditional relaxation instead.

## 9. Code-block impact

- 1,445 code blocks across the RU corpus (identical count in PL — code listings are not translated).
- Isolated `break-inside: avoid` removal cost: **-70 pages (RU), -66 (PL)** — the single largest individually-measured lever in this audit.
- `.code-block pre` already uses `white-space: pre-wrap; word-break: break-word;` — long lines wrap rather than overflowing, so the *width* dimension is already handled; the *height*/pagination dimension (a whole block moving to the next page rather than splitting) is the open cost.
- Not measured directly (would require a size-conditional CSS rule the current architecture doesn't have a hook for): what fraction of the 1,445 blocks are "large" (author's working definition for Phase 2B: more than ~15-18 lines, i.e. taller than roughly half the current 33-line text column) and therefore the ones actually paying this cost. Recommended as the first concrete measurement of Phase 2B.

## 10. Table impact

- 257 `.compare-table` tables (classic-vs-modern / option-A-vs-option-B comparisons), containing 1,216 `<tr>` rows total, each individually `break-inside: avoid`.
- This selector was **not** isolated in a render experiment (grouped into the combined -141/-129 figure); given its low per-row height relative to a code block, its individual contribution is expected to be materially smaller than either `.code-block` or `.callout` — a reasonable estimate, given the group total minus the two isolated leaders (39 remaining pages across 7 selectors), is a low single digit to low double digit page count, not a top-3 contributor. Recommended for isolated measurement in Phase 2B before any change is proposed.
- Plain (non-`.compare-table`) `<table>` elements have no explicit break-inside rule in the print stylesheet at all — they were not investigated further here as no forcing mechanism applies to them.

## 11. Figure/diagram impact

- 31 `.chapter-figure` instances: 23 wide, 2 narrow, 0 medium. Not isolated individually, but strongly correlated with the single lowest-density chapter found (Chapter 7, Turtle deep-dive — section 5) purely through cross-referencing occurrence density against chapter word-count tables in the underlying evidence JSON.
- `.chapter-figure` is `break-inside: avoid`, and a full-width diagram plus its caption can plausibly occupy 40-60% of the 179mm text column height on its own — one such figure landing near a page boundary is enough to push the remainder of that page's content forward, leaving a partial page behind it. This matches the "figure-heavy chapters have the lowest density" pattern found independently in section 5.
- Limitation acknowledged per section 4: a page dominated by one `.chapter-figure` plus a short caption will show a low *word* count in this text-extraction-based method while being visually full (a large image, not whitespace) — the "low words/page" signal for figure-heavy chapters should NOT be read as "these pages are wasted," but as "these pages are graphics-heavy, and this text-only method cannot distinguish that from true waste without a visual/box-geometry pass." Recommended follow-up for Phase 2B if figure sizing is on the table: a pixel-coverage or WeasyPrint-box-geometry measurement, out of scope here.

## 12. Page-geometry analysis

From the canonical `@page` rule (`book_shared.build_print_css`), computed arithmetically (no rendering needed):

| | Value |
|---|---:|
| Page size | 152mm × 229mm (6in × 9in — a standard technical-book trim) |
| Margins (top/right/bottom/left) | 24 / 20 / 26 / 20 mm |
| Text area | 112mm × 179mm |
| Text area as % of physical page | **57.6%** |
| Body font size / line-height | 10.3pt / 1.48 |
| Line height | 15.244pt |
| Estimated lines per page | **~33.3** |

For context: many 6"×9" technical books (the same trim size used here) run 42-50 lines per page at 9-9.5pt/1.15-1.25 line-height with tighter margins — this book's current typography sits well on the spacious end of that range. Margin/line-height choices are a legitimate, measurable lever (see sections 13 and 17), but the trim size itself is not "small" for the density achieved.

## 13. Typography sensitivity analysis (measured, not estimated)

| Change | RU pages | RU delta | PL pages | PL delta |
|---|---:|---:|---:|---:|
| Baseline | 2518 | — | 2428 | — |
| Font 10.3pt → 9.8pt (line-height unchanged) | 2476 | **-42 (-1.67%)** | 2387 | **-41 (-1.69%)** |
| Line-height 1.48 → 1.35 (font unchanged) | 2387 | **-131 (-5.20%)** | 2307 | **-121 (-4.98%)** |

(All four render-experiment numbers above are WeasyPrint's own internal page count, i.e. one less than the final merged-PDF page count — see the `render_experiments` block of the evidence JSON.)

Line-height is a **far larger lever than font size** per unit of visual change (a 0.13 line-height reduction costs about 5.2%, vs. a 0.5pt font reduction costs 1.7%) — but it is also the *riskier* change: 1.35 is a fairly tight setting for a serif body face read at length, more likely to be perceived as "cramped" than a half-point font reduction. Both numbers are real render measurements, not linear extrapolations from CSS inspection.

## 14. Top ranked root causes by measured/estimated page inflation (RU; PL tracks within a few pages throughout)

10 quantified causes plus one qualitative pattern (#11, not a page-cost figure). Rows 8 and 9 are two DIFFERENT, independently-measured mechanisms for the same project-entry symptom (see section 7) — they are listed separately and must not be added together as if they were one combined -17-page finding; row 6's "-19/-20" is a third, separately-measured combination (recto + row-9's forced-break removal, NOT row 8's hero resize).

| # | Cause | Evidence | Page cost | % of book | Confidence |
|---|---|---|---:|---:|---|
| 1 | `break-inside: avoid` (all 9 selectors combined) | Measured (render experiment) | -141 | -5.6% | **Measured ceiling** |
| 2 | Line-height 1.48 → 1.35 | Measured (render experiment) | -131 | -5.2% | **Measured** |
| 3 | `.code-block { break-inside: avoid }` alone | Measured (isolated render experiment) | -70 | -2.8% | **Measured** |
| 4 | Font-size 10.3pt → 9.8pt | Measured (render experiment) | -42 | -1.7% | **Measured** |
| 5 | `.callout { break-inside: avoid }` alone | Measured (isolated render experiment) | -32 | -1.3% | **Measured** |
| 6 | Recto (`break-before: right`) + `.project-entry` forced-break REMOVAL, combined (evidence-JSON key `combined_p0_p1`) | Measured (render experiment) | -19 | -0.75% | **Measured** |
| 7 | `.chapter-hero` recto policy alone | Measured (render experiment) | -11 | -0.44% | **Measured** |
| 8 | `.project-hero` height 62mm → 45mm alone (forced break UNCHANGED — a separate mechanism from row 9) | Measured (isolated render experiment) | -9 | -0.36% | **Measured** |
| 9 | `.project-entry` forced page break REMOVAL alone (hero height UNCHANGED — a separate mechanism from row 8) | Measured (isolated render experiment) | -8 | -0.32% | **Measured** |
| 10 | Remaining 7 break-inside selectors combined (`.exercise`, `.summary-box`, `.cvm`, `.chapter-figure`, `.idx-entry`, `.notebook-card`, `.compare-table tr`) | Derived: (1) − (3) − (5) | ≈ -39 | ≈ -1.5% | Derived from measured totals |
| 11 | Figure-dense chapter content (Turtle/Tkinter chapters) | Chapter-density correlation (section 5, 11) | not separable from content volume | — | Qualitative, content-correlated |

## 15. Recommended remediation order (ranked P0-P5)

| Priority | Location / rule | Current | Proposed direction | Expected reduction | Visual risk | Semantic risk | Test needed |
|---|---|---|---|---:|---|---|---|
| **P0** | `.project-entry .project-hero` height (`book_shared.build_print_css`) — mechanism B, section 7 | Fixed 62mm | Reduce hero height to 45mm (the specific value measured) so title+description+`.notebook-card` fit on ONE page per project, WITHOUT touching the forced break | **-9 RU / -7 PL (measured: `render_experiments.project_hero_45mm`)** | Low (smaller decorative graphic, all text preserved) | None | Visual check: all 13 project entries fit on 1 page each; hero still legible |
| **P0-alt** | `.project-entry { break-before: page; }` — mechanism A, section 7 (an ALTERNATIVE to P0 for the same symptom, not additive with it — see section 7's non-conflation note) | Forces every project onto its own fresh page regardless of remaining space | Relax to `break-before: auto`, letting a short project flow onto the same page as the previous one's tail | **-8 RU / -7 PL (measured: `render_experiments.no_project_forced_break`)** | Low-medium (projects would no longer each start a visually clean new page) | None | Verify project boundaries remain visually distinguishable without the page break (e.g. via spacing/rule) |
| **P1** | `.chapter-hero { break-before: right; }` | Forces recto (right-hand) start | Relax to `break-before: page` (still a clean fresh-page start, drops the right-hand requirement) | **-11 RU / -13 PL (measured: `render_experiments.no_recto_right_hand`)** | Low-medium (loses the classic "chapters start on a right page" print convention — a genuine editorial/design judgment call) | None | Regenerate `data/book-pagination.json`; confirm chapter start/end contiguity holds; confirm outline/bookmarks still resolve |
| **P2a** | `.code-block { break-inside: avoid }` | Unconditional avoid | Conditional: keep `avoid` for blocks under ~15-18 lines; allow `auto` (controlled split) for longer ones | Est. 30-45 of the 70-page ceiling | Medium (a split code block needs a "continued" visual cue to stay legible) | Low | Verify no split occurs mid-statement in a way that changes meaning; verify syntax-highlighting spans don't break across the split |
| **P2b** | `.callout { break-inside: avoid }` | Unconditional avoid | Same conditional approach, size threshold tuned to callout's typical shorter height | Est. 10-20 of the 32-page ceiling | Medium | Low | Verify callout icon/border still reads correctly if split; most callouts are short enough this may rarely trigger |
| **P2c** | Remaining break-inside selectors (`.exercise`, `.summary-box`, `.cvm`, `.chapter-figure`, `.idx-entry`, `.notebook-card`, `.compare-table tr`) | Unconditional avoid | Leave as-is; combined ceiling (~39 pages, ~1.5%) does not justify the added fragmentation-handling complexity here — revisit only if Phase 2B needs every remaining page | ~0 (deferred) | — | — | — |
| **P3** | `@page` margins (24/20/26/20mm) | Spacious relative to comparable 6"×9" technical books | Modest trim (e.g. -2 to -3mm per side) once P0-P2 are in and re-measured | Not render-measured; geometry estimate only, likely low single-digit % | Medium (less white space/margin for reader annotation, tighter gutter) | None | Re-run the full render-experiment harness after any margin change — do not estimate this one from CSS alone |
| **P4a** | Body font-size 10.3pt | — | Trim to ~9.8-10.0pt | -42 pages at 9.8pt (measured) | Low-medium | None | Print-simulate a sample chapter at actual trim size for legibility sign-off |
| **P4b** | Body line-height 1.48 | — | Trim to ~1.40 first (not 1.35 — see section 13's risk note), re-measure before going further | Unmeasured at 1.40 (bracketed between 0 and -131 at 1.35) | Medium-high | None | Same legibility sign-off as P4a, at actual trim size, ideally on a printed proof |
| **P5** | Aggressive compaction: stack P0-P2 (narrow) + P3 + P4a + a conservative P4b (1.40) together | — | Only after each piece above is independently validated and re-measured together (effects are not purely additive — see section 17) | Estimated 250-450 pages combined, i.e. roughly 2050-2250 total pages | High (multiple simultaneous changes compound readability risk) | Low if content untouched | Full render-experiment re-run of the *combined* stack, not a sum of independent deltas; a full print-proof review |

## 16. Risks and trade-offs

- **Every render-experiment number in this report isolates exactly one change**, except one: section 7's "combined_p0_p1" experiment (recto relaxation + project-entry forced-break removal — NOT the project-hero resize, see section 7's non-conflation note) showed near-perfect additivity (-11 + -8 = -19 measured as -19 exactly in RU; -13 + -7 = -20 measured as -20 exactly in PL). This should **not** be assumed to generalize to combinations involving line-height or break-inside changes, where the mechanisms interact (a looser line-height changes how many lines a "long" code block needs, which changes how often the P2 threshold triggers). **Any P5 combined estimate must be re-measured with the actual combined CSS**, not summed from independent deltas.
- **Line-height and code-block/callout fragmentation are the two highest-value levers, and also the two with the most reader-facing risk.** The recto and project-entry fixes (P0/P1) are comparatively low-risk but also low-yield (under 1% each).
- **The figure/diagram findings (section 11) are qualitative, not a proposed cut.** Reducing diagram count or size would touch educational content and diagrams, which is explicitly out of scope for this phase and protected under the contract's "Protected Educational Structure" clause.
- **Text-extraction-based density metrics systematically undercount graphics-heavy pages** (section 4, 11) — a future phase should not treat "low words/page" as automatically "wasted" without also checking whether the page is carrying a full-width diagram.
- **The extracted word counts include running-header and folio text** on every page (a few words of bleed per page, documented in section 2's total). This is a small, uniform bias that does not affect relative comparisons (all pages carry it equally) but means "total words" is not a pure body-text count.

## 17. Proposed Phase 2B acceptance targets

**Is 600-800 pages realistic without harming readability? No — not through pagination-rule or typography tuning within the current page format.**

The corpus contains ≈232,000 words of body text per language (a real, protected content volume — see the contract's Protected Educational Structure clause; this phase does not propose cutting it). To land at 700 pages (the middle of the requested range) at that word count requires roughly:

```
232,201 words / 700 pages ≈ 332 words/page
```

against a current median of 93 words/page — a **~3.6× density increase**. The single largest measured lever in this entire audit (removing all `break-inside: avoid`, the least realistic one to actually ship) is worth 5.6%. Stacking literally every lever measured here (break-inside ceiling + line-height-to-1.35 + font-to-9.8pt + recto + project-break, ignoring the interaction risk flagged in section 16) is arithmetically:

```
2519 − 141 − 131 − 42 − 19 ≈ 2186 pages (RU)
```

— a 13% reduction, landing around **2100-2250 pages**, not 700. **600-800 pages is not reachable by any combination of pagination-rule and typography changes measured in this audit, at the current 152mm×229mm trim and current content volume.**

**What range is realistic**, based on what was actually measured:

| Scenario | Changes | Estimated RU pages | Basis |
|---|---|---:|---|
| **Low-risk only** (P0-alt+P1) | Project-entry forced-break removal + recto relaxation — NOTE: this is the `combined_p0_p1` evidence-JSON key, a name preserved from the initial measurement round; it does NOT include the P0 project-hero resize (a separate, not-yet-combined measurement — see section 7) | ~2500 (−0.8%) | Measured (`render_experiments.combined_p0_p1`) |
| **Moderate redesign** (P0-P2 narrow, P4a, conservative P4b) | + size-conditional code-block/callout fragmentation + font 9.8pt + line-height ~1.40 | **≈2000-2300** (−9% to −20%) | Partial measurement + informed interpolation; must be re-measured as a combined stack before acceptance |
| **Aggressive compaction** (P0-P4 stacked at measured maximum settings, no content change) | + line-height 1.35 (not 1.40) + full break-inside removal | **≈2150-2250** (still, because the biggest levers don't stack cleanly — see section 16) | Sum of measured deltas, upper-bound, not re-measured as a stack |
| **600-800 pages** | Not achievable without either (a) a different page format (larger trim size and/or multi-column layout) or (b) reducing the ~232K-word content volume | — | Out of scope for a layout-only remediation; requires an explicit Product Owner content/format decision |

**Recommendation for Phase 2B:** target the **moderate redesign** band (roughly 2000-2300 pages, a 10-20% reduction) using the P0-P2/P4a levers in this report, each re-measured individually and then as a combined stack via the same render-experiment harness before being accepted — and treat any page-format change (trim size, columns) as a separate, explicit decision requiring its own Product Owner sign-off, since the numbers above show it is the only way to approach 600-800 pages.

---

## Appendix: reproduction

```bash
python scripts/analyze_book_pagination.py --language ru
python scripts/analyze_book_pagination.py --language pl
python scripts/analyze_book_pagination.py --all
python scripts/analyze_book_pagination.py --language ru --render-experiments   # ~15-20 min, 10 variants
python scripts/analyze_book_pagination.py --language pl --render-experiments   # ~15-20 min, 10 variants
```

Both committed evidence JSONs (`evidence/m02-i07-pagination-diagnostics-{ru,pl}.json`) were regenerated through these exact two `--render-experiments` commands (the canonical CLI, no manual/follow-up mutation of the output) as part of this report's review-amendment pass, and every `render_experiments` value reproduced identically to the prior committed values, with three fields newly present because they are now computed by the canonical implementation itself: `no_callout_avoid`, `no_code_block_avoid`, `project_hero_45mm`, and `page_delta_pct_vs_baseline` for every variant.

Tests: `pytest tests/test_pagination_diagnostics.py -q` (37 tests). All but three run the fast artifact-analysis tier; three additional tests (`test_declared_render_experiments_are_well_formed`, `test_declared_render_experiment_patches_target_real_css`, `test_run_render_experiments_produces_expected_schema`) assert the render-experiment names/schema/arithmetic are correct WITHOUT paying the ~15-20 minute/language cost of real WeasyPrint rendering (the last of the three fakes only the `weasyprint.HTML.render()` call itself, exercising every other line of `run_render_experiments` for real).
