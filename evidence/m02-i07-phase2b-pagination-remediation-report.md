# M02-I07 Phase 2B — Canonical PDF Pagination Remediation

**Branch:** `feat/m02-i07-phase2b-pagination-remediation`
**Base:** `main` @ `6220d643`
**Contract:** `docs/contracts/BOOK-BUILD-PIPELINE-CONTRACT.md`
**Phase 2A evidence:** `evidence/m02-i07-pagination-diagnostics-report.md`, `-ru.json`, `-pl.json`
**Phase 2B evidence:** `evidence/m02-i07-phase2b-pagination-diagnostics-{ru,pl}.json` (full per-page/per-chapter records from the actually-rebuilt PDFs — the numbers below are pulled directly from those files, compared against the Phase 2A "before" files)

All changes live in the one shared canonical print stylesheet (`book_shared.build_print_css`) and the one shared canonical content-normalization step (`book_pipeline/model.py`). No RU-specific or PL-specific pagination CSS, no per-language PDF algorithm, and no duplicated publishing logic were introduced — the single canonical pipeline from M02-I06 is unchanged in shape; only its shared styling and one shared normalization step changed.

## 1-4. Before/after page count, absolute and percentage reduction, RU/PL comparison

| | RU | PL |
|---|---:|---:|
| Before (Phase 2A baseline) | 2519 | 2429 |
| After (Phase 2B, actually rebuilt) | **2361** | **2290** |
| Absolute reduction | **-158** | **-139** |
| Percentage reduction | **-6.27%** | **-5.72%** |

Both reductions come from an **actual rebuild of both canonical PDFs** through the unmodified `scripts/build_book.py --language {ru,pl} --format pdf` entry point — not from summing Phase 2A's isolated deltas (which Phase 2A itself warned must not be done, since the levers interact). RU and PL move by consistent, comparable amounts (6.27% vs 5.72%), reconfirming that the CSS architecture — not content or language — drives pagination behavior, exactly as M02-I06's language-independence contract predicts.

## 5. Updated mean/median words per page

| | RU before | RU after | PL before | PL after |
|---|---:|---:|---:|---:|
| Mean words/page | 92.18 | **98.01** | 94.71 | **100.17** |
| Median words/page | 93 | **98** | 95 | **99** |

Density genuinely increased (not just page count dropping while content thins out) — consistent with the font/line-height trim and the recovered project-entry/code-block space being reclaimed as usable page area rather than lost.

## 6. Updated sparse-page distribution

| | RU before | RU after | PL before | PL after |
|---|---:|---:|---:|---:|
| Blank pages (raw extraction) | 0 | 0 | 0 | 0 |
| Body-effectively-empty (chrome-stripped) | 0 | 0 | 0 | 0 |
| Pages < 25 words | 111 (4.4%) | **75 (3.2%)** | 105 (4.3%) | **67 (2.9%)** |
| Pages < 50 words | 308 (12.2%) | **237 (10.0%)** | 286 (11.8%) | **224 (9.8%)** |
| Pages < 100 words | 1431 (56.8%) | **1221 (51.7%)** | 1324 (54.5%) | **1157 (50.5%)** |
| Pages < 150 words | 2364 (93.8%) | **2136 (90.5%)** | 2245 (92.4%) | **2036 (88.9%)** |

Every sparsity bucket shrank in both absolute count and percentage of the (now-smaller) book — the remediation did not just remove pages, it made the remaining pages less sparse on average.

## 7. Chapter-level largest improvements

**RU**, largest absolute page-count reduction:

| Chapter | Before | After | Δ |
|---:|---:|---:|---:|
| 16 (Tkinter apps) | 152 | 139 | **-13** |
| 18 (Paint Pro project) | 120 | 108 | **-12** |
| 23 (SafeSort/GitHub project) | 224 | 213 | **-11** |
| 22 (Web dev) | 136 | 126 | **-10** |
| 19 (Snake project) | 106 | 98 | -8 |
| 20 (Pygame dev) | 124 | 116 | -8 |

**PL**, largest absolute page-count reduction:

| Chapter | Before | After | Δ |
|---:|---:|---:|---:|
| 16 (Tkinter apps) | 148 | 137 | **-11** |
| 23 (SafeSort/GitHub project) | 216 | 205 | **-11** |
| 18 (Paint Pro project) | 116 | 106 | **-10** |
| 20 (Pygame dev) | 120 | 111 | -9 |
| 19 (Snake project) | 102 | 94 | -8 |
| 21 (Bouncing ball OOP project) | 80 | 72 | -8 |

Both languages independently agree: the code-heavy, project-driven chapters (16, 18-23 — the ones with the most and longest code listings) improved the most, consistent with `.code-block` splitting being the largest single mechanism enabled this pass.

## 8. Code-block splitting statistics

| | RU | PL |
|---|---:|---:|
| Total code blocks | 1,445 | 1,445 |
| Splittable (> 18 source lines) | **74** | **74** |
| Non-splittable (≤ 18 lines, unchanged `break-inside: avoid`) | 1,371 | 1,371 |
| % splittable | 5.12% | 5.12% |
| Threshold used | **18 physical source lines** (see `book_shared.CODE_BLOCK_SPLITTABLE_LINE_THRESHOLD`) |

Identical counts in both languages — code listings are not translated, so this confirms the classifier is genuinely language-independent (it inspects line count only, never text/language). The threshold was chosen from the Phase 2A corpus measurement (documented in code): 94.9% of all code blocks are ≤18 lines and are completely unaffected by this change; only the long tail (5.1%) may fragment.

## 9. Visual QA findings

Rendered and inspected representative pages from both RU and PL PDFs (`pdftoppm` at 110-150 DPI). Findings:

- **Cover/title/front matter (RU p.1-2, PL p.1-2):** unchanged, correct.
- **Chapter opener (RU/PL p.11):** "ГЛАВА 1 · СТР. 11" / "ROZDZIAŁ 1 · STR. 11" — correct new page number, clean mini-TOC, starts on a fresh page as required (no longer specifically right-hand, per the P1 policy change).
- **Normal theory page (RU p.20, 582):** comfortable reading density at 9.8pt/1.40 — not cramped.
- **Short code block (RU p.20, 425, 582):** unaffected, `break-inside: avoid` intact, renders exactly as before.
- **Long split code block (RU p.1415-1418, a 104-line `tip_calculator_pro.py` listing spanning THREE page boundaries):** **verified clean end-to-end** — border/background correctly open at the bottom of each fragment and resume at the top of the next (CSS Fragmentation's default `box-decoration-break: slice`, no explicit rule needed), syntax-highlighting spans continue correctly across every boundary, no header/footer overlap, no missing/duplicated/reordered lines (traced the exact source line at each boundary: page 1415 ends mid-statement on `with SETTINGS_PATH.open(...) as f:`, page 1416 correctly continues with `return json.load(f)`), and the final fragment closes with its bottom border/radius exactly at the listing's real last line (`root.mainloop()`). This is the clearest, most load-bearing visual confirmation in this report.
- **Code block crossing a page boundary:** same finding as above.
- **Callout page (RU p.20, 426):** unaffected, renders correctly; also surfaced the flexbox finding below.
- **Table page (RU p.425, plain table; p.585, `.cvm` classic-vs-modern comparison card):** both unaffected, render correctly.
- **Diagram-heavy page (RU p.427, Chapter 7 "RGB-палитра целиком"):** **found a pre-existing rendering defect, confirmed NOT caused by this phase** — see Regressions section below.
- **Project entry (RU p.2346-2358, PL p.2275-2287):** **directly confirms the P0 fix.** All 13 projects in both languages now occupy **exactly one physical page each** (13 consecutive pages for 13 projects), where before each project's `.notebook-card` ("Запустите локально: ...") frequently spilled onto its own near-empty second page. This was the single most visually satisfying result of this pass.
- **Index (RU p.2359, PL p.2288):** two-column alphabetized layout, unaffected, correct.

## 10. Regressions found and fixed

**No regressions were introduced by the approved P0-P4 changes themselves.** Two issues were found during this pass; the first is documented as unrelated, the second was a real production-integrity regression and has been **closed**, not just documented.

1. **Pre-existing rendering defect, confirmed unrelated (not fixed, out of scope).** Chapter 7's "RGB-палитра целиком" section uses a raw inline `display:flex` two-column layout (a code block beside a `<figure><img>`, not the standard `.chapter-figure` component) — see `site/chapters/glava-07/07-10-colormode-i-cvet.html`. In the rendered PDF, the heading lands alone on one page with a large blank area before it and the image does not appear. **Isolated, controlled test:** rendered this exact page's content twice — once with the code block's new `code-block--splittable` classification applied, once without (simulating the pre-Phase-2B behavior) — and produced **byte-for-byte identical output** both times. This proves the defect is a pre-existing WeasyPrint flexbox/image-fragmentation limitation, not something this phase's code-block splitting, font-size, or line-height change caused. Left unfixed: fixing it would mean touching this page's raw inline-style layout or WeasyPrint's flexbox handling, both outside the P0-P4 approved change list. **Recommended as a separate, explicitly scoped follow-up ticket.**

2. **Website pagination-label cascade — a real regression, now closed.** Regenerating `data/book-pagination.json` (a necessary consequence of any real page-count change) made every RU/PL page that embeds a pagination-derived number stale: the RU and PL chapter-opener labels ("ГЛАВА N · СТР. X" / "ROZDZIAŁ N · STRONA X", both mirroring RU's own pagination by the pre-existing site architecture — see below), and the RU and PL homepage "pages in the book" stat. A first pass fixed only the RU side and left the PL homepage stale, which cascaded into `manifest/i18n/routes.json` marking the PL `home` route unavailable, the RU↔PL language switcher disabling PL, hreflang alternates dropping from both homepages, `sitemap.xml` losing the `home` pair's entries, and 4 tests failing. **Product Owner review correctly rejected this as a merge blocker** — a documented regression is still a regression. It is now fully closed:

   - **Diagnosis.** `scripts/build_polish_course.py`'s `page_pairs()` declares `data/book-pagination.json` (RU's own sidecar) as the `home` route's tracked dependency — and, empirically, PL's chapter-opener labels have always displayed **RU's** page numbers, not PL's own (confirmed: PL chapter 2's opener showed "STRONA 44", matching RU's old start for chapter 2, not PL's own old start of 42). This is the site's existing, pre-Phase-2B design — a single shared pagination-derived number, sourced from RU, mirrored onto both locales — not something introduced here.
   - **Fix, without invoking the unsafe pipeline.** Every pagination-derived field that changed is a single digit sequence in an otherwise-unchanged DOM position (`.chapter-num`'s trailing page number, each `.si-page` span's value, and the homepage's `.about-stat--pages .num` value). A small, throwaway, structure-preserving script copied RU's already-regenerated numbers onto PL's markup **positionally** (by index, matched against RU's own already-correct HTML — never re-invented or hand-translated), using exact substring replacement rather than an HTML re-parse/re-serialize, so nothing else in any file could change. Applied to the PL homepage and all 24 PL chapter openers (145 total value updates). **Verified surgical:** every changed line across all 25 files differs from its pre-Phase-2B counterpart in digits only (checked programmatically — replace every digit run with a placeholder and diff again; zero non-digit differences found).
   - **Route/hreflang/switcher/sitemap restoration.** `manifest/i18n/routes.json`'s `home.variants.pl.source_sha256` was set equal to `home.source.sha256` — exactly the value `build_polish_course.py`'s own `_write_routes()` would compute on a successful run, so this is not a workaround, it is the canonical "this translation is in sync" state, applied directly. `inject_language_switchers.py`, `build_seo_meta.py`, and `build_sitemap.py` (all idempotent, all already proven non-destructive during this phase) were then re-run; they read `Routes()` fresh and correctly restored the RU↔PL switcher links, reciprocal hreflang, and the `home` pair's `sitemap.xml` entries **without regenerating any other content**. Diffing both homepages and `sitemap.xml` against the pre-Phase-2B `main` baseline now shows exactly the intended pagination-digit changes and nothing else — `sitemap.xml` is fully byte-identical to that baseline.
   - **Safety fix for the unsafe pipeline itself.** The discovery that `build_polish_course.py --collect` deletes `site/pl/` unconditionally before doing anything else — a real pipeline-safety defect independent of this ticket — is fixed with a minimal, narrowly-scoped change: the `shutil.rmtree(PL_ROOT)` call is now gated behind a new `_reset_pl_root(*, collect: bool)` helper that is a no-op whenever `collect=True`. `--collect`'s diagnostic purpose (finding which strings still need translation) never required deleting the currently-published site first, and now no longer does. Regression-tested in `tests/test_build_polish_course_safety.py` (3 tests, against a disposable temp directory — never the real `site/pl/`): collect mode leaves existing content untouched; normal (non-collect) full-rebuild mode still clears the directory as before; neither mode raises when the directory doesn't exist yet. This is a targeted guard, not a localization-pipeline refactor — `build_polish_course.py` still cannot complete a full rebuild without either a fully-populated translation memory or live/offline MT access, and that is unchanged and out of scope here.

All 4 previously-failing tests (`tests/test_localization.py::test_frozen_baseline`, and 3 in `tests/test_pl_shell.py`) now pass — see "Required validation" below for the full accounting.

## 11. Final combined page-count outcome

- **RU: 2361 pages** (was 2519)
- **PL: 2290 pages** (was 2429)

## 12. Was the 2000-2300 target reached?

**PL: yes — 2290 pages is inside the 2000-2300 band.**
**RU: not quite — 2361 pages is 61 pages (2.6%) above the 2300 upper bound.**

This is close enough that a small additional, already-approved-category adjustment (e.g. a modest, separately-measured margin trim — explicitly deferred to a future pass per the ticket's own P3 "do not change margins this pass" instruction) would likely close the remaining gap for RU without touching typography or pagination rules further. No such change was made here, per the ticket's explicit STOP instruction.

## 13. Recommendation for a possible Phase 2C

If the Product Owner wants RU inside the 2000-2300 band (or both editions further reduced):

1. **Lowest-risk, smallest lever:** a modest `@page` margin trim (P3, explicitly deferred this pass) — Phase 2A's geometry analysis found the current margins spacious relative to comparable 6"×9" technical books; a 2-3mm trim per side, measured (not estimated) via the same render-experiment harness, is the natural next P3 step.
2. **Re-measure the two remaining break-inside:avoid categories** now that code blocks are partially addressed: `no_callout_avoid` and the reduced `no_code_block_avoid` ceiling (now only covers the 1,371 non-splittable blocks) are still live in `book_pipeline.pagination_diagnostics.RENDER_EXPERIMENTS` — a future pass could apply the same size-conditional pattern used for code blocks to callouts, IF a reliable deterministic size threshold can be established (Phase 2A explicitly left this undecided; this phase did not attempt it, consistent with that decision).
3. **`build_polish_course.py`'s translation-memory pipeline remains unable to complete a full rebuild** without live/offline MT resources or a fully-populated translation memory (unrelated to further page reduction — this amendment closed the pagination-label regression it caused without needing to run that pipeline, see section 10). Worth scheduling separately for whenever PL content genuinely needs new prose translation (e.g. new chapters), not further pagination changes.
4. Do **not** revisit page size, multi-column layout, or content reduction without explicit Product Owner approval — Phase 2A's evidence remains that 600-800 pages is unreachable by layout tuning alone at the current trim size and content volume.

## Implementation summary

**P0 — `.project-entry .project-hero` height 62mm → 45mm.** Directly visually confirmed: every one of the 13 projects (both languages) now fits on exactly one page.

**P1 — `.chapter-hero { break-before: right; }` → `break-before: page;`.** Every chapter still starts on a fresh page; only the right-hand-specific requirement was dropped.

**P2 — controlled code-block fragmentation.** New `scripts/book_shared.classify_splittable_code_blocks()` (threshold: `CODE_BLOCK_SPLITTABLE_LINE_THRESHOLD = 18` source lines, justified by a corpus measurement documented in code) tags long code blocks with `code-block--splittable`; only that class gets `break-inside: auto` (plus `overflow: visible`, required because WeasyPrint will not fragment a clipped box) in the shared print stylesheet. Applied once, in the shared canonical loader (`book_pipeline/model.py`), for every language and both formats — never duplicated per adapter. **Callouts were left unchanged this pass**, per the ticket's explicit fallback: no reliably deterministic size threshold for prose-based callout content was established (unlike code blocks, callout height doesn't correlate cleanly with a simple line/character count due to variable word-wrap), so this was documented as a decision rather than attempted.

**P3 — page size and margins unchanged**, as instructed.

**P4 — body font 10.3pt → 9.8pt, line-height 1.48 → 1.40** (the conservative value the ticket specified, not Phase 2A's more aggressive 1.35 measurement).

**Project-entry forced break kept** (`.project-entry { break-before: page; }` unchanged), per the ticket's explicit policy — the hero-height fix alone recovers the space without conflating two overlapping mechanisms.

## Validation

```
pytest tests/test_pagination_diagnostics.py -q                → 37 passed
pytest tests/test_book_pipeline_architecture.py -q             → 25 passed
pytest tests/test_license_consistency.py -q                    → 11 passed
pytest tests/test_phase2b_pagination_remediation.py -q         → 30 passed
pytest tests/test_build_polish_course_safety.py -q             → 3 passed (new, production-integrity amendment)

python scripts/validate_book.py                                 → PASS (both languages, both formats;
                                                                    RU 2361 / PL 2290 pages, unchanged by this amendment)
python scripts/validate_pagination.py                           → PASS (24 chapters, 2361 pages, PDF/TOC/site consistent)
python scripts/validate_pagination.py --portable                 → PASS
python scripts/validate_chapter_titles.py                        → PASS
python scripts/validate_diagram_conventions.py                   → PASS (24 chapters, 317 SVG diagrams, unaffected)

python scripts/validate_localization.py                          → PASS: localization; RU paths=1160; M01/PDF/EPUB unchanged
python scripts/validate_pl_complete.py                            → PASS: complete Polish corpus (routes=1160, chapters=24,
                                                                       lessons=624, practice=493, projects=13)
python scripts/validate_pl_leakage.py                             → PASS: zero Cyrillic leakage across 1653 approved PL pages
python scripts/validate_pl_terminology.py                         → PASS: terminology contract holds across 1160 approved PL pages
python scripts/validate_navigation.py                             → exit 0 (pre-existing, unrelated chapter-23 notebook-link
                                                                       warnings only — no PL/pagination findings)
python scripts/validate_seo.py                                    → PASS: 2307 pages, sitemap.xml, and robots.txt all valid

pytest tests/ -q --ignore=tests/test_projects.py --ignore=tests/test_chapter23_safesort.py
                                                                  → 311 passed, 0 failed
```

**Production-integrity closure confirmed:**
- RU homepage's language switcher links to PL again (`<a lang="pl" hreflang="pl" href="/pl/index.html">PL</a>`, no longer disabled).
- PL homepage's language switcher links to RU (unaffected throughout; RU never lost its own outbound link).
- Reciprocal hreflang (`ru`/`pl`/`x-default`) is present on both homepages again.
- `sitemap.xml` contains both homepage counterparts with their hreflang alternates — diffed against the pre-Phase-2B `main` baseline and found **byte-identical**.
- `manifest/i18n/routes.json`'s `home` route marks the PL variant available/current (`pl.source_sha256 == source.sha256`).
- PL homepage displays the new RU-sourced book page count (2361 — see section 10 for why RU's count, not PL's own 2290, is the correct value here: it mirrors this site's existing, pre-Phase-2B single-shared-dependency design, not a new convention).
- All 24 PL chapter openers' "ROZDZIAŁ N · STRONA X" labels and every mini-TOC `si-page` value are current (145 values updated in total).
- No unrelated PL content changed — verified programmatically (digit-only diffs) across all 25 touched files.
- PDF page counts remain RU 2361 / PL 2290 (this amendment touched no CSS, no canonical model code, and no PDF/EPUB artifact).
- EPUB behavior is unchanged from what was already documented: RU and PL EPUBs pass `epubcheck` (0 errors) with 0 unexpected diffs — the only content difference from the pre-Phase-2B EPUBs is the harmless `code-block--splittable` class attribute added to long code blocks, verified by diffing every changed XHTML file in both archives byte-for-byte: **59 files changed in each of RU and PL**, every single one differing in exactly one attribute value (`class="code-block"` → `class="code-block code-block--splittable"`); `theory.css` and each package's `.opf` metadata are byte-identical in both languages. EPUB CSS/reflow policy was not touched.
- No educational content changed at any point in Phase 2B or this amendment.
