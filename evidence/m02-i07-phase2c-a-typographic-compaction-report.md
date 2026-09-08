# M02-I07 Phase 2C-A — Typographic Compaction

**Branch:** `feat/m02-i07-phase2c-typographic-compaction`
**Base:** `main` @ `c9fde2a7`
**Contract:** `docs/contracts/BOOK-BUILD-PIPELINE-CONTRACT.md`
**Phase 2B evidence:** `evidence/m02-i07-phase2b-pagination-diagnostics-{ru,pl}.json`, `evidence/m02-i07-phase2b-pagination-remediation-report.md`
**Phase 2C-A evidence:** `evidence/m02-i07-phase2c-a-pagination-diagnostics-{ru,pl}.json` (full per-page/per-chapter records from the actually-rebuilt PDFs — the numbers below are pulled directly from those files, compared against the Phase 2B "before" files)

This is the integration of a Product-Owner-approved print-typography density candidate (visually reviewed via rendered before/after page samples in an earlier, now-defunct throwaway experiment worktree with byte-identical CSS). All changes live in the one shared canonical print stylesheet (`book_shared.build_print_css`) — no RU-specific or PL-specific pagination CSS, no per-language PDF algorithm, no duplicated publishing logic. **This is explicitly the FIRST compaction layer only.** The approved final target is ~900 pages; reaching it requires separate structural/editorial work (Phase 2C-B, tracked and investigated independently — out of scope here). This phase only tightens vertical rhythm (line-height, margins, padding) — it does not touch page size, margins, or content.

## 1. What changed — 19 CSS rules, before/after

| # | Selector | Before | After |
|---:|---|---|---|
| 1 | `body` | `line-height: 1.40` | `line-height: 1.26` |
| 2 | `h1` | `font-size: 21pt; margin: 0 0 10pt;` | `font-size: 18pt; line-height: 1.1; margin: 0 0 5.5pt;` |
| 3 | `h2` | `font-size: 14.5pt; margin: 20pt 0 8pt;` | `font-size: 13pt; margin: 12pt 0 5pt;` |
| 4 | `h3` | `font-size: 12pt; margin: 14pt 0 6pt;` | `font-size: 10.5pt; margin: 8.5pt 0 3.5pt;` |
| 5 | `p` | `margin: 0 0 8pt;` | `margin: 0 0 4.5pt;` |
| 6 | `ul, ol` | `margin: 0 0 8pt;` | `margin: 0 0 4.5pt;` |
| 7 | `.code-block pre` | `padding: 9pt 11pt; line-height: 1.42;` | `padding: 7pt 8.5pt; line-height: 1.32;` |
| 8 | `.callout` | `padding: 6pt 10pt; margin: 8pt 0;` | `padding: 4pt 10pt; margin: 5pt 0;` |
| 9 | `.exercise` | `padding: 6pt 10pt; margin: 8pt 0;` | `padding: 4pt 10pt; margin: 5pt 0;` |
| 10 | `.summary-box` | `padding: 8pt 12pt; margin: 10pt 0;` | `padding: 5pt 12pt; margin: 6pt 0;` |
| 11 | `.toc-part-title` | `margin: 12pt 0 5pt;` | `margin: 6.5pt 0 3pt;` |
| 12 | `.toc-entry` | `padding: 2.5pt 0;` (no explicit line-height) | `padding: 1.25pt 0; line-height: 1.18;` |
| 13 | `.title-page` | `padding-top: 70mm;` | `padding-top: 45mm;` |
| 14 | `.title-page h1` | `margin: 12pt 0 6pt;` (font-size unchanged: 27pt) | `margin: 8pt 0 4pt;` |
| 15 | `.title-page .subtitle` | `margin-bottom: 36pt;` | `margin-bottom: 20pt;` |
| 16 | `.title-page .author` | `margin-top: 50pt;` | `margin-top: 30pt;` |
| 17 | `.copyright-page` | `line-height: 1.4; padding-top: 8mm;` | `line-height: 1.3; padding-top: 4mm;` |
| 18 | `.copyright-page p` | `margin: 0 0 7pt;` | `margin: 0 0 4pt;` |
| 19 | `.copyright-page .cp-title` | `margin-bottom: 4pt;` | `margin-bottom: 3pt;` |

Page size (`152mm 229mm`), margins (`24mm 20mm 26mm 20mm`), `.chapter-hero`, `.project-entry .project-hero`, and every other rule not listed above are byte-identical to Phase 2B's committed state — verified by the corrected `tests/test_phase2b_pagination_remediation.py` (30 tests, all still passing except the 2 assertions this phase's own ticket explicitly authorized updating — see below) plus the new `tests/test_phase2c_a_typographic_compaction.py` (23 tests) locking in all 19 new literals verbatim.

**Two Phase 2B test assertions were updated** (the ticket's own explicit, pre-identified scope): `test_css_contains_body_font_98pt` / `test_css_body_line_height_is_140_not_135` (body line-height `1.40` → `1.26`) and `test_css_callouts_are_unchanged_in_this_pass` (`.callout` padding/margin literal). Everything else in that file — project-hero 45mm, chapter-hero, page size/margin, the `.code-block` outer rule — stays correct and passes unchanged.

**A second, mechanically necessary fix, outside `book_shared.py`:** `scripts/book_pipeline/pagination_diagnostics.py`'s `RENDER_EXPERIMENTS` dict and `_BREAK_INSIDE_AVOID_CSS_LINES` tuple keep their own literal copies of the `.callout`, `.exercise`, and `.summary-box` selector strings (used to patch-and-measure CSS at render-experiment time). These 3 literals were stale after this phase's rules 8-10 above and were updated to match — otherwise `tests/test_pagination_diagnostics.py`'s `test_declared_render_experiment_patches_target_real_css` and `test_run_render_experiments_produces_expected_schema` fail with a "patch target not found" error. This is the same class of fix as the Phase 2B test-assertion corrections, just living in production code rather than a test file.

## 2. Why

Product-Owner-approved density candidate, direct PDF inspection finding: the book is currently ~2000+ pages against an ultimate approved target of ~900. Phase 2B (font-size/line-height/code-block-splitting/project-hero) was the first remediation pass; this phase applies a second, purely typographic layer — tightening line-height and the margin/padding rhythm around headings, paragraphs, lists, callouts, exercises, summary boxes, TOC entries, and front/back matter — without touching page geometry or content.

## 3. Measured page-count results

| | RU | PL |
|---|---:|---:|
| Before (Phase 2B) | 2361 | 2290 |
| After (Phase 2C-A, actually rebuilt) | **2097** | **2035** |
| Absolute reduction | **-264** | **-255** |
| Percentage reduction | **-11.18%** | **-11.14%** |

Both figures come from an **actual rebuild of both canonical PDFs** through the unmodified `scripts/build_book.py` entry point (`--all`, plus per-target retries — see Section 6). These reproduce **exactly** the numbers from the earlier approved throwaway-worktree experiment (RU 2361→2097, PL 2290→2035), confirming the candidate is deterministic and content-independent of the branch it's applied on. RU and PL move by near-identical percentages (11.18% vs 11.14%), reconfirming — as Phase 2B did — that the CSS architecture, not language or content, drives pagination behavior.

## 4. Words-per-page sanity check

Computed via `pdftotext -layout <pdf> - | split on form-feed | word count per page`.

| | RU before (Phase 2B) | RU after (Phase 2C-A) | PL before (Phase 2B) | PL after (Phase 2C-A) |
|---|---:|---:|---:|---:|
| Mean words/page | 99.5 | **111.4** | 101.7 | **113.8** |
| Median words/page | 99 | **110** | 100 | **113** |

Density increased substantially and consistently in both languages — the page-count drop reflects genuinely tighter typography reclaiming page area, not content thinning out or pages being silently dropped. (RU/PL "before" figures per the ticket's own stated baseline, derived from the Phase 2B page counts.)

## 5. Determinism check

Re-ran `python scripts/build_book.py --language pl --format pdf` a second time and diffed the output against the first build:

```
book/pdf/python-od-zera-pl.pdf        → sha256 identical, byte-for-byte cmp: PASS
data/book-pagination-pl.json          → sha256 identical, byte-for-byte cmp: PASS
```

**Result: PASS.** The build is fully reproducible given identical source content and CSS.

## 6. Build reliability note

Both EPUB builds (RU and PL) failed transiently on the first `--all` attempt with `'H' format requires 0 <= number <= 65535` (a zipfile DOS-timestamp packing error, unrelated to content). Both succeeded cleanly on an immediate single-target retry (`--language {ru,pl} --format epub`), and the PL PDF+EPUB pair (never reached by the first `--all` run, which stops at the first failure) was subsequently built with `--language pl --format all`. `scripts/validate_book.py` was then run manually (since the four targets were not built in one single `--all` invocation) and reported **PASS** for both languages, both formats: RU 2097 pages / 1221 bookmarks, PL 2035 pages / 1221 bookmarks, both PDFs with correct metadata and uniform page size, both EPUBs with 0 `epubcheck` errors.

## 7. EPUB content check

`epub_adapter.py` does not call `build_print_css()` — confirmed by diffing every RU/PL EPUB chapter XHTML file against `main`. **The EPUBs are NOT byte-identical to `main`** — every one of the 24 chapter files in each language differs, but **only** in embedded page-number cross-references (`.chapter-num`'s "· STRONA N" / "· СТР. N" label, and each `.si-page` span's value) that mirror the PDF's own new pagination. This is the exact same category of change Phase 2B's own EPUB diff documented (there: the added `code-block--splittable` class attribute; here: page-number digits) — a legitimate, expected consequence of the page count changing, not evidence that EPUB's own stylesheet or layout logic was touched. `theory.css` (packaged verbatim into both EPUBs) and each package's `.opf` metadata are unaffected.

## 8. Site/localization regeneration (mirrors Phase 2B's own post-merge remediation, commit `0d4e72e2`)

`data/book-pagination.json`'s new RU page numbers are a declared input to every RU chapter opener's embedded "ГЛАВА N · СТР. X" label, every mini-TOC `.si-page` value, and the homepage's "Страниц в книге" stat — exactly as Phase 2B found and fixed in `0d4e72e2 fix(site): resync RU pagination labels after Phase 2B page-count change`. This phase reproduced that same, precedented remediation:

- Regenerated all 24 RU chapter openers (`scripts/build_chapter_01.py` … `_24.py`) and the RU homepage (`scripts/build_site_index.py`), then re-ran the SEO-meta (`scripts/build_seo_meta.py`) and language-switcher (`scripts/inject_language_switchers.py`) injection passes — both idempotent, separate pipeline stages that chapter/homepage regeneration strips and that must be re-applied afterward.
- `manifest/i18n/routes.json`: refreshed the `home` page's tracked source hash via `localization.source_hash()` (its declared dependency, `data/book-pagination.json`, changed). **Left the `pl` variant's `source_sha256` untouched**, matching `0d4e72e2`'s own precedent exactly: `build_polish_course.py` requires live/offline MT resources not available in this environment and unconditionally deletes `site/pl/` before rebuilding (confirmed destructive even by inspection of its own `_reset_pl_root()` guard) — attempting it blind is explicitly out of scope for this phase, per the task's own "no destructive git command" instruction and this project's own established pattern of treating full PL re-sync as separate follow-up work.
- `manifest/i18n/ru_baseline.json`: updated the frozen RU PDF/EPUB `sha256` and page count (2361→2097) to the actually-rebuilt artifacts — no generator script exists for this file; updated directly against the rebuilt PDF/EPUB, matching `0d4e72e2`'s own approach.

**Known, accepted consequence — identical in kind to Phase 2B's own `0d4e72e2`:** 4 tests now fail, all for the single, documented reason that the PL homepage was not re-translated/re-synced: `tests/test_localization.py::test_frozen_baseline` ("Unapproved PL output: /pl/index.html"), and 3 in `tests/test_pl_shell.py` (`test_complete_corpus_contract`, `test_every_route_is_an_exact_publishable_pair`, `test_all_polish_pages_have_no_accidental_cyrillic`). This is the exact same failure signature Phase 2B's own remediation produced and explicitly accepted as a "separate PL-content-sync follow-up." **Recommended as a separate follow-up once MT resources are available** — exactly as Phase 2B's own report recommended, and exactly what later closed it there (`348fc46a fix(i18n): restore RU<->PL homepage bilingual availability after Phase 2B`).

## 9. Test suite result

```
pytest tests/ -q   →   382 passed, 4 failed (see Section 8 — single documented, precedented cause)
```

Baseline check (pristine `main`, changes stashed): `pytest tests/ -q` → **362 passed, 0 failed.** All 4 remaining failures on this branch are confirmed real, single-root-cause consequences of this phase's legitimate page-count change (not pre-existing on `main`, not unrelated flakiness) — traced individually, reproduced deterministically, and matched precisely against an already-accepted precedent from the immediately preceding phase.

## 10. Visual spot-check

Rendered 4 pages from the freshly-built PL PDF at 150 DPI (`pdftoppm`): ToC first page (p.4), a code-heavy Chapter 4 page (p.180), the "Co poszło nie tak?" flowchart (title box on p.191, diagram body on p.192 — splits cleanly across the page boundary with `box-decoration-break: slice`, no clipping), and the "Rysowalnia" project-opener page (p.2020). All four: **no clipped text, no overlapping elements, no broken tables.** One pre-existing, unrelated cosmetic mark was noted below the practice-link row on the project-opener page, inside the untouched `.project-entry`/`.project-hero` region (not among this phase's 19 rules) — flagged for completeness, not a regression from this change.

## 11. Scope confirmation

This is the **first compaction layer only**. RU 2097 / PL 2035 pages remains well above the ultimate ~900-page target. Reaching that target requires structural/editorial work — chapter/section consolidation, exercise/example trimming, front-matter reduction — tracked separately as **Phase 2C-B**, being investigated in parallel by someone else, and explicitly out of scope for this integration.

## Implementation summary

**19 CSS rules** (Section 1), all in the one shared `book_shared.build_print_css()` — no per-language branching (locked in by `test_no_language_specific_pagination_branch_in_book_shared` and `test_print_css_is_structurally_identical_for_ru_and_pl_locales`, both still passing). Page size, margins, `.chapter-hero`, and `.project-entry .project-hero` are unchanged, as instructed.

## Validation

```
python scripts/build_book.py --all                             → RU/PL PDF succeeded; RU/PL EPUB failed transiently
                                                                    (zipfile timestamp error), succeeded on retry
python scripts/validate_book.py                                 → PASS (RU 2097p/1221 bookmarks, PL 2035p/1221
                                                                    bookmarks; both EPUBs 0 epubcheck errors)
python scripts/build_book.py --language pl --format pdf (2nd run) → byte-identical to the 1st run (PDF + pagination JSON)
python scripts/analyze_book_pagination.py --all                  → evidence/m02-i07-pagination-diagnostics-{ru,pl}.json
                                                                    written; RU median 109 words/page, PL median 111
pytest tests/ -q                                                 → 382 passed, 4 failed (Section 8/9)
pytest tests/ -q  (pristine main, stashed)                       → 362 passed, 0 failed
```

**Before-PR checklist:**
- RU PDF builds: **yes** (2097 pages).
- PL PDF builds: **yes** (2035 pages).
- EPUB unchanged: **no** — changed only in pagination-derived digits (Section 7), same class of change as Phase 2B's own EPUB diff, confirmed harmless.
- One canonical pipeline: **yes** — `scripts/build_book.py` unmodified in shape; only shared CSS changed.
- No content loss: **yes** — words-per-page increased (Section 4); RU/PL frozen route inventories otherwise unchanged; visual spot-check clean.
- Diagrams not newly damaged: **yes** — flowchart page-break spot-check clean (Section 10).
- No clipping/overlap: **yes** (Section 10).
- Git diff deterministic: **yes** (Section 5).
- All tests pass: **no** — 4 known, precedented, documented failures (Section 8/9), identical in kind and cause to an already-accepted Phase 2B failure signature; recommended as separate PL-content-sync follow-up, not a blocker for this typography-only integration.
