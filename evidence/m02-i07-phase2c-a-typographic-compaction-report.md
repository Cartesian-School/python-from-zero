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

## 7a. Correction — the EPUBs above were not actually rebuilt (found during final pre-PR validation)

Section 7's claim above is **wrong for the bytes that were actually committed** on this branch until commit `af9cfb63`. A final, independent pre-PR validation pass diffed the committed EPUBs against a fresh rebuild and found both `book/epub/python-s-nulya-ru.epub` and `book/epub/python-od-zera-pl.epub` still carried **pre-Phase-2C-A** chapter-opener page-number labels in all 24 chapters of both languages (e.g. RU chapter 1 showed "СТР. 11", the old 2361-page-era number, not the current "СТР. 10") — 48/48 chapter-opener labels checked (24 chapters × 2 languages) matched the old pagination, 0/48 matched the new. `scripts/validate_book.py`'s `epubcheck` pass does not catch this, since it validates EPUB structural conformance only, not page-number-label freshness against `data/book-pagination*.json`.

Root cause: the original build attempt's EPUB stage failed transiently (Section 6) and the retry that followed evidently did not fully replace the previously-committed (Phase 2B-era) EPUB bytes before they were staged and committed in `dd580b3c`.

**Fixed in `af9cfb63`:** both EPUBs rebuilt again via the unmodified `scripts/build_book.py --format epub` (once per language). Verified this time: all 48 chapter-opener labels now match the current 2097/2035-page pagination exactly, `epubcheck` reports 0 errors for both, and `manifest/i18n/ru_baseline.json`'s frozen `epub.sha256` (which Section 8's `ru_baseline.json` update below had correctly updated for `pdf.sha256`/`pages` but missed for `epub.sha256`, since the stale EPUB bytes matched what was frozen) was corrected to match. `pytest tests/ -q` went 385 passed/1 failed → 386 passed/0 failed as a direct result.

Current, correct SHA-256:
- `book/epub/python-s-nulya-ru.epub`: `cde31690987bbe6c245f78d04556d7820d90854251774178b4f60230d3996cb1`
- `book/epub/python-od-zera-pl.epub`: `72b4aaf3e66075721726259b000e3900453e950850e15ef9cf45318053b5dc22`

## 8. Site/localization regeneration — full RU+PL closure (mirrors `0d4e72e2` + `348fc46a`)

`data/book-pagination.json`'s new RU page numbers are a declared input to every RU chapter opener's embedded "ГЛАВА N · СТР. X" label, every mini-TOC `.si-page` value, and the homepage's "Страниц в книге" stat. This phase reproduced Phase 2B's own two-stage post-merge remediation in full, both stages, on this branch:

**Stage 1 — RU resync (mirrors `0d4e72e2`).** Regenerated all 24 RU chapter openers (`scripts/build_chapter_01.py` … `_24.py`) and the RU homepage (`scripts/build_site_index.py`), then re-ran the SEO-meta (`scripts/build_seo_meta.py`) and language-switcher (`scripts/inject_language_switchers.py`) injection passes — both idempotent, separate pipeline stages that chapter/homepage regeneration strips and that must be re-applied afterward. `manifest/i18n/ru_baseline.json`: updated the frozen RU PDF/EPUB `sha256` and page count (2361→2097) to the actually-rebuilt artifacts.

**Stage 2 — PL resync (mirrors `348fc46a`).** An initial version of this phase left the `pl` variant's `source_sha256` untouched, reproducing the exact 4-test failure signature Phase 2B's own `0d4e72e2` amendment had left behind — **this was independently identified as the wrong closure**: Product Owner review had already explicitly rejected exactly this state once before (`348fc46a`'s own commit message: *"leaving the PL homepage's pagination-derived fields stale ... is a production regression on the completed M02-I04 bilingual site, not an acceptable side effect of a PDF-pagination ticket"*). Correction applied, reproducing `348fc46a`'s own technique with this run's numbers:

- **Root cause (pre-existing, confirmed again):** PL chapter openers and the PL homepage stat have always mirrored **RU's** page numbers, not translated PL content — `build_polish_course.py`'s `page_pairs()` declares `data/book-pagination.json` as the `home` route's tracked dependency regardless of locale. No translation work is required, only copying already-correct digits.
- **Fix, without invoking the unsafe full-site rebuild:** a throwaway script (`sync_pl_pagination.py`) copied RU's already-regenerated numbers onto PL's markup **positionally**, via exact substring replacement only (never an HTML re-parse/re-serialize) — the `.chapter-num` trailing page number and every `.si-page` span, matched by index against RU's structurally-identical section-list order (verified: identical `.si-page` counts in every one of the 24 chapters between languages), plus the homepage's `about-stat--pages` digit. Touched exactly 25 files: the PL homepage and all 24 PL chapter openers.
- **Verified surgical:** every one of the 25 changed files, diffed against its pre-change (`HEAD`) state with every digit run replaced by a placeholder, produces **zero non-digit differences** — confirmed programmatically, same check `348fc46a` used.
- `manifest/i18n/routes.json`: `home.variants.pl.source_sha256` set equal to `home.source.sha256` — the canonical "in sync" state `build_polish_course.py`'s own `_write_routes()` would compute on success, not a workaround.
- Re-ran the idempotent `inject_language_switchers.py`, `build_seo_meta.py`, and `build_sitemap.py`: RU↔PL switcher links restored on both homepages (PL no longer shows `aria-disabled`), reciprocal `hreflang` (ru/pl/x-default) restored on both homepages, `sitemap.xml` required **no changes** (already byte-identical, matching `348fc46a`'s own finding).

**`build_polish_course.py` itself was never invoked** — still destructive (unconditional `shutil.rmtree(PL_ROOT)` outside its already-fixed `--collect` no-op path) and requires live/offline MT resources not available in this environment; not needed here since no new translation was required, only digit resync.

## 9. Test suite result

```
pytest tests/ -q   →   386 passed, 0 failed
```

Fully green. All 4 previously-failing tests (`test_localization.py::test_frozen_baseline`, and 3 in `test_pl_shell.py`) now pass. Additional validators, all PASS: `validate_localization.py` (RU paths=1160), `validate_pl_complete.py` (routes=1160, chapters=24, lessons=624, practice=493, projects=13), `validate_pl_leakage.py` (zero Cyrillic leakage, 1653 approved PL pages), `validate_pl_terminology.py` (terminology contract holds, 1160 approved PL pages), `validate_seo.py` (2307 pages, sitemap.xml, robots.txt valid). `validate_book.py`: PASS, PDF page counts and EPUB behavior **unaffected** by this website-only work — RU 2097 pages / PL 2035 pages, both EPUBs 0 `epubcheck` errors, identical to Section 3/7's figures. This confirms the site-sync work touched no book/PDF/EPUB artifact.

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
                                                                    bookmarks; both EPUBs 0 epubcheck errors) —
                                                                    re-confirmed PASS, unaffected, after the PL
                                                                    site-sync closure below
python scripts/build_book.py --language pl --format pdf (2nd run) → byte-identical to the 1st run (PDF + pagination JSON)
python scripts/analyze_book_pagination.py --all                  → evidence/m02-i07-pagination-diagnostics-{ru,pl}.json
                                                                    written; RU median 109 words/page, PL median 111
pytest tests/ -q                                                 → 386 passed, 0 failed
pytest tests/ -q  (pristine main, stashed)                       → 362 passed, 0 failed
python scripts/validate_localization.py                          → PASS: RU paths=1160; M01/PDF/EPUB unchanged
python scripts/validate_pl_complete.py                            → PASS: routes=1160, chapters=24, lessons=624,
                                                                       practice=493, projects=13
python scripts/validate_pl_leakage.py                             → PASS: zero Cyrillic leakage, 1653 approved PL pages
python scripts/validate_pl_terminology.py                         → PASS: terminology contract holds, 1160 approved
                                                                       PL pages
python scripts/validate_seo.py                                    → PASS: 2307 pages, sitemap.xml, robots.txt valid
```

**Production-integrity closure confirmed** (mirrors `348fc46a`'s own checklist):
- RU homepage's language switcher links to PL again (`<a lang="pl" hreflang="pl" href="/pl/index.html">PL</a>`, no longer `aria-disabled`).
- PL homepage's language switcher links to RU (unaffected throughout).
- Reciprocal `hreflang` (ru/pl/x-default) present on both homepages again.
- `sitemap.xml` required no changes — already byte-identical, matching `348fc46a`'s own finding.
- `manifest/i18n/routes.json`'s `home` route marks the PL variant available/current (`pl.source_sha256 == source.sha256`).
- PL homepage displays the new RU-sourced page count (2097 — mirrors this site's pre-existing, pre-Phase-2B single-shared-dependency design, not a new convention).
- All 24 PL chapter openers' "ROZDZIAŁ N · STRONA X" labels and every mini-TOC `.si-page` value are current (25 files, digit-only changes, verified surgical — Section 8).
- No unrelated PL content changed — verified programmatically (digit-only diff against `HEAD`) across all 25 touched files.
- PDF page counts unaffected: RU 2097 / PL 2035 (this closure touched no CSS, canonical model code, or PDF/EPUB artifact — confirmed via `git status -- book/ data/` showing zero changes, and `validate_book.py` re-run clean).
- EPUB behavior unaffected — 0 `epubcheck` errors both languages.
- No educational content changed at any point in this phase or this closure.

**Before-PR checklist:**
- RU PDF builds: **yes** (2097 pages).
- PL PDF builds: **yes** (2035 pages) — confirmed completely unaffected by the site-sync closure (byte-identical `sha256`, zero `git status` changes under `book/`/`data/`).
- EPUB unchanged: **no** — changed only in pagination-derived digits (Section 7), same class of change as Phase 2B's own EPUB diff, confirmed harmless.
- One canonical pipeline: **yes** — `scripts/build_book.py` unmodified in shape; only shared CSS changed.
- No content loss: **yes** — words-per-page increased (Section 4); RU/PL frozen route inventories otherwise unchanged; visual spot-check clean.
- Diagrams not newly damaged: **yes** — flowchart page-break spot-check clean (Section 10).
- No clipping/overlap: **yes** (Section 10).
- Git diff deterministic: **yes** (Section 5).
- All tests pass: **yes** — 386 passed, 0 failed, after closing the PL site-sync gap exactly as `348fc46a` established (Section 8).
