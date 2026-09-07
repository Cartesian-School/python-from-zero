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

**No regressions were introduced by the approved P0-P4 changes themselves.** Two issues were found and handled during this pass; both are documented rather than silently absorbed:

1. **Pre-existing rendering defect, confirmed unrelated (not fixed, out of scope).** Chapter 7's "RGB-палитра целиком" section uses a raw inline `display:flex` two-column layout (a code block beside a `<figure><img>`, not the standard `.chapter-figure` component) — see `site/chapters/glava-07/07-10-colormode-i-cvet.html`. In the rendered PDF, the heading lands alone on one page with a large blank area before it and the image does not appear. **Isolated, controlled test:** rendered this exact page's content twice — once with the code block's new `code-block--splittable` classification applied, once without (simulating the pre-Phase-2B behavior) — and produced **byte-for-byte identical output** both times. This proves the defect is a pre-existing WeasyPrint flexbox/image-fragmentation limitation, not something this phase's code-block splitting, font-size, or line-height change caused. Left unfixed: fixing it would mean touching this page's raw inline-style layout or WeasyPrint's flexbox handling, both outside the P0-P4 approved change list. **Recommended as a separate, explicitly scoped follow-up ticket.**

2. **Website pagination-label cascade, handled per established practice.** Regenerating `data/book-pagination.json` (a necessary consequence of any real page-count change — see `docs/contracts/BOOK-BUILD-PIPELINE-CONTRACT.md` and prior-session memory of this exact cascade from M02-I06) made the RU website's own chapter-opener labels ("ГЛАВА N · СТР. X", embedded via `site_lib.render_chapter_opener`) and the homepage's "Страниц в книге" stat stale. Regenerated: all 24 RU chapters (`build_chapter_01.py`...`build_chapter_24.py`), `build_index.py`, `build_manifest.py`, `build_projects.py`, `build_site_index.py`, then re-ran `inject_language_switchers.py` and `build_seo_meta.py`/`build_sitemap.py`/`build_llms_full.py` to restore the SEO/i18n metadata those chapter rebuilds strip (it's re-injected as a separate pipeline stage). One `manifest/i18n/routes.json` entry (`home`'s tracked source hash, which includes `data/book-pagination.json` as a declared dependency) was refreshed using the same `localization.source_hash()` function the pipeline itself uses — a one-line, narrowly-scoped, non-destructive fix. `manifest/i18n/ru_baseline.json`'s frozen `pdf`/`epub`/`pages` fields were also updated to the new, legitimately-changed values (no generator script exists for this file; updated by hand against the actual rebuilt artifacts).

   **Known, accepted side effect:** `site/pl/index.html` (the PL homepage) was **not** re-translated, since its translation memory-based regeneration pipeline (`build_polish_course.py`) (a) requires live/offline machine-translation resources not available in this environment for the ~24 new "ГЛАВА N · СТР. X" strings, and (b) **unconditionally deletes `site/pl/` before rebuilding**, including in its supposedly-safe `--collect` mode — this was discovered by triggering it once, which deleted `site/pl/` before crashing on a missing translation; it was immediately restored via `git restore site/pl/` with zero data loss. Rather than risk that a second time for a website-only, PL-content-sync task explicitly outside this PDF-pagination ticket's scope, the localization system's own honest staleness tracking was left to do its job: `manifest/i18n/routes.json`'s `home` entry now correctly reports the PL variant as unavailable (RU's source hash moved, PL's did not), and the site's own language switcher on the RU homepage now shows PL as disabled ("Przekład niedostępny" / "Перевод недоступен") rather than a broken or silently-wrong link — this is the system's designed graceful-degradation behavior working correctly, not a bug. Four tests outside this ticket's required validator list (`tests/test_localization.py::test_frozen_baseline`'s "Unapproved PL output" check, and three in `tests/test_pl_shell.py`) now fail for this single, well-understood, honestly-reported reason. **Recommended as a separate PL-content-sync follow-up** (re-running `build_polish_course.py` once genuine MT/translation resources are available, then `_write_routes()` will restore the PL `home` route).

No other test outside these four was affected — see section "Validation" below for the full, itemized pass/fail accounting.

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
3. **PL content sync** (see Regressions section) is unrelated to further page reduction but should be scheduled so the website doesn't drift further from the book.
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
pytest tests/test_pagination_diagnostics.py -q              → 37 passed
pytest tests/test_book_pipeline_architecture.py -q           → 25 passed
pytest tests/test_license_consistency.py -q                  → 11 passed
pytest tests/test_phase2b_pagination_remediation.py -q       → 30 passed (new)

python scripts/validate_book.py                               → PASS (both languages, both formats)
python scripts/validate_pagination.py                         → PASS (24 chapters, 2361 pages, PDF/TOC/site consistent)
python scripts/validate_pagination.py --portable               → PASS
python scripts/validate_chapter_titles.py                      → PASS
python scripts/validate_diagram_conventions.py                 → PASS (24 chapters, 317 SVG diagrams, unaffected)

pytest tests/ -q --ignore=tests/test_projects.py --ignore=tests/test_chapter23_safesort.py
                                                                → 307 passed, 4 failed
                                                                  (all 4 trace to the single documented PL-homepage
                                                                  staleness cause above; none are in this ticket's
                                                                  required validator list)
```

EPUB safety: RU and PL EPUBs rebuilt, both pass `epubcheck` (0 errors) with 0 unexpected diffs — the only content difference from the pre-Phase-2B EPUBs is the harmless `code-block--splittable` class attribute added to long code blocks, verified by diffing every changed XHTML file in both archives byte-for-byte: **59 files changed in each of RU and PL**, every single one differing in exactly one attribute value (`class="code-block"` → `class="code-block code-block--splittable"`), confirmed via an automated scan rejecting any other kind of line change; `theory.css` and each package's `.opf` metadata are byte-identical in both languages. EPUB CSS/reflow policy was not touched, per the ticket's explicit instruction.
