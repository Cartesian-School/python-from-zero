# M02-I06 — Unified Canonical Book Build Pipeline: Implementation Report

**Branch:** `feat/m02-i06-unified-book-pipeline`
**Contract:** `docs/contracts/BOOK-BUILD-PIPELINE-CONTRACT.md`
**Scope:** Phase 1 (architecture stabilization only) — no pagination redesign, no typography changes, no content changes.

## 1. Files changed

New package:

- `scripts/book_pipeline/__init__.py` — public API (`build_book`, `get_locale`, `SUPPORTED_LANGUAGES`, `SUPPORTED_FORMATS`)
- `scripts/book_pipeline/config.py` — `BookLocaleConfig` / `ProjectEntry` contract
- `scripts/book_pipeline/locale_ru.py` — RU locale config + content discovery
- `scripts/book_pipeline/locale_pl.py` — PL locale config + content discovery
- `scripts/book_pipeline/locales.py` — language → config registry
- `scripts/book_pipeline/model.py` — `CanonicalBookLoader` / `CanonicalBookModel`
- `scripts/book_pipeline/pdf_adapter.py` — PDF publication adapter
- `scripts/book_pipeline/epub_adapter.py` — EPUB publication adapter
- `scripts/book_pipeline/pipeline.py` — `build_book(language, output_format)`

Modified:

- `scripts/book_shared.py` — added `extract_page_title()` (locale-agnostic; used by the PL config's title discovery, previously private to `build_epub_pl.py`)
- `scripts/build_book.py` — rewritten as the canonical `--language`/`--format`/`--all` CLI
- `scripts/build_pdf.py`, `scripts/build_pdf_pl.py`, `scripts/build_epub.py`, `scripts/build_epub_pl.py` — reduced to thin compatibility wrappers
- `scripts/validate_pagination.py` — routes its fingerprint check through `book_pipeline` instead of importing `build_pdf.py` internals
- `scripts/README.md` — documents the new architecture

New test:

- `tests/test_book_pipeline_architecture.py` — 15 tests enforcing the contract

Unchanged (verified byte-identical, so nothing to commit): `book/pdf/*.pdf`, `book/epub/*.epub`, `data/book-pagination.json`, `data/book-pagination-pl.json`.

## 2. Old architecture

```
build_book.py  --(subprocess)-->  build_epub.py   (RU EPUB: full independent implementation)
               --(subprocess)-->  build_pdf.py    (RU PDF: `import build_epub as be` for content,
                                                    own build_full_html()/main())
               --(subprocess)-->  build_epub_pl.py (PL EPUB: `import build_epub as be` for RU
                                                     page identity, own extraction/packaging)
               --(subprocess)-->  build_pdf_pl.py  (PL PDF: `import build_epub_pl as be`,
                                                     own build_full_html()/main())
               --(subprocess)-->  validate_book.py
```

`book_shared.py` held the locale-agnostic mechanics (link rewriting, SVG repair, EPUB packaging determinism, PDF anchor/pagination bookkeeping), but title/copyright/TOC construction, chapter iteration, `build_full_html()`, WeasyPrint rendering, `EpubBook` construction, and spine/TOC assembly were each independently duplicated across the four scripts. PDF depended on EPUB's module object for content discovery (`import build_epub as be`), an inverted, incidental coupling rather than a designed shared model.

## 3. New architecture

```
language (ru|pl) --> BookLocaleConfig (locale_ru.py / locale_pl.py, via locales.py)
                              |
                              v
                  CanonicalBookLoader.load(config)   [model.py — one implementation, both languages]
                              |
                              v
                     CanonicalBookModel               [front_matter, chapters, projects, index_page —
                                                        content already run through the shared
                                                        extract_article/extract_opener/extract_project]
                              |
                    +---------+---------+
                    v                   v
            pdf_adapter.build()   epub_adapter.build()
            (WeasyPrint, print          (EbookLib, spine/nav,
             CSS, pagination)            reflowable XHTML)
```

`build_book(language, output_format)` (`pipeline.py`) is the single canonical entry point. `scripts/build_book.py` exposes it as a CLI; `build_pdf.py`/`build_pdf_pl.py`/`build_epub.py`/`build_epub_pl.py` each call it with a fixed `language`/`output_format` pair and contain no other logic.

## 4. Duplicate logic removed

- Title page / copyright page / TOC-entry construction (previously 4 near-identical copies) → one implementation each in `pdf_adapter.py`, parameterized by `BookLocaleConfig`.
- `build_full_html()` chapter/front-matter/project/index iteration (previously 2 copies, RU and PL) → one implementation in `pdf_adapter.py`, driven by `CanonicalBookModel`.
- `EpubBook` construction, CSS/asset packaging, spine/TOC assembly, `build_item`/`build_project_item`/`build_copyright_item` (previously 2 copies) → one implementation in `epub_adapter.py`.
- RU vs. PL content-extraction call sites (`extract_article`/`extract_opener`/`extract_project`) were already calling the same `book_shared` functions in both formats; this is now done exactly **once** per page in `CanonicalBookLoader.load()` instead of once per adapter per language (4 call sites → 1).
- The PL `project_css` stylesheet and EPUB reproducible-timestamp (`EPUB_BUILD_MTIME`) logic, previously copy-pasted verbatim into `build_epub_pl.py`, are now single module-level definitions in `epub_adapter.py`.
- PDF's former dependency on EPUB's module for content discovery (`import build_epub as be` inside `build_pdf.py`) is gone — both adapters now depend only on the shared `CanonicalBookModel`.

## 5. Compatibility wrappers retained

`build_pdf.py`, `build_pdf_pl.py`, `build_epub.py`, `build_epub_pl.py` are retained as thin wrappers (23–32 lines each, down from 240–335) that only call `book_pipeline.build_book(...)`. `build_epub.py` additionally re-exports two data constants (`RIGHTS_NOTICE_PLAIN`, `CONTENT_LICENSE_URL`) for `tests/test_license_consistency.py`'s existing backward-compatible import. `tests/test_book_pipeline_architecture.py::test_compatibility_wrapper_is_thin` enforces both the delegation call and the absence of independent-logic markers (`build_full_html`, `EpubBook()`, `WeasyPrint`, `PAGES`, etc.) in all four.

## 6. Commands used

```bash
# Canonical CLI
python scripts/build_book.py --language ru --format pdf
python scripts/build_book.py --language ru --format epub
python scripts/build_book.py --language pl --format pdf
python scripts/build_book.py --language pl --format epub

# Compatibility wrappers (equivalent)
python scripts/build_pdf.py
python scripts/build_epub.py
python scripts/build_pdf_pl.py
python scripts/build_epub_pl.py

# Validation
python scripts/validate_book.py
python scripts/validate_pagination.py
python scripts/validate_pagination.py --portable
```

## 7. Tests executed

```
pytest tests/test_book_pipeline_architecture.py -q   → 15 passed
pytest tests/test_license_consistency.py -q          → 11 passed
pytest tests/ -q --ignore=tests/test_projects.py --ignore=tests/test_chapter23_safesort.py
                                                       → 244 passed
```
(`test_projects.py`/`test_chapter23_safesort.py` need Xvfb/an editable SafeSort install not provisioned in this environment; both are unrelated to the book pipeline and untouched by this change.)

## 8. Validation executed

```
scripts/validate_book.py    → RU PDF: 2519 pages, metadata present, 1221 bookmarks, epubcheck 0 errors
                               PL PDF: 2429 pages, metadata present, 1221 bookmarks, epubcheck 0 errors
                               ВАЛИДАЦИЯ ПУБЛИКАЦИИ: PASS
scripts/validate_pagination.py            → PASS (24 chapters, 2519 pages, PDF/TOC/site consistent)
scripts/validate_pagination.py --portable → PASS (24 chapters, 2519 pages, PDF/TOC/site consistent)
```

## 9. Output SHA-256 values

| Artifact | SHA-256 | vs. pre-refactor baseline |
|---|---|---|
| `book/pdf/python-s-nulya-ru.pdf` | `60e512cf6fe07b35d5c5bcf535c05e13980bfc33841bc263ef22dbfffe14720a` | identical |
| `book/pdf/python-od-zera-pl.pdf` | `bc7e51a3b755c23bbf8fc15e0520fe81db470877a1bd7158e27497ee2e8b11cb` | identical |
| `book/epub/python-s-nulya-ru.epub` | `e03d691a68590d3a83613f20dd22a95acc2c338320671f5beb9c12944a43be9a` | identical |
| `book/epub/python-od-zera-pl.epub` | `80ada70b4ded00aeb0898ab3c94b426ab2f1ec342796e64a2136e7cafef0d938` | identical |
| `data/book-pagination.json` | `799fb0bf1cb5bb2d8e3c822a37adb04c36e0905ef2748738219b5bda1463f29b` | identical |
| `data/book-pagination-pl.json` | `be8ab69ecfa8159b77c211c6013f51d611ceae03aacfe3db3ef86d8a918b9b14` | identical |

Baseline was captured from `main`/HEAD (commit `c3bbba4e`) before any refactor code was written.

## 10. Known intentional byte differences

**None in the committed artifacts.** All four publication artifacts and both pagination sidecars are byte-for-byte identical to the pre-refactor baseline.

One transcription bug was caught and fixed during verification, not shipped: the first draft of `locale_ru.py`/`locale_pl.py` stored the copyright page's "electronic edition" sentence as a normally-wrapped Python string, losing the original source's embedded `"\n      "` (a literal newline + 6-space indent inside the old f-string). This is whitespace inside HTML source (collapses identically under HTML rendering, so the rendered PDF pixels are unaffected) but it changed the generated HTML string's byte content and therefore the `pdf_source_fingerprint` recorded in the pagination JSON. It was found by diffing the full generated HTML string against the pre-refactor generator (byte for byte) before trusting any output, and fixed by restoring the exact original line-wrap in both locale configs. Final rebuild is confirmed byte-identical (section 9).

## 11. Proof that language and format are now parameters

`tests/test_book_pipeline_architecture.py`:
- `test_language_is_an_input_parameter` — intercepts `CanonicalBookLoader.load` and shows `build_book(language=X, ...)` resolves to `get_locale(X)`'s exact config object, for both `ru` and `pl`.
- `test_format_is_an_output_parameter` — intercepts the adapter dispatch table and shows `build_book(..., output_format=Y)` invokes exactly the adapter registered for `Y`.
- `test_unsupported_language_fails_explicitly` / `test_unsupported_format_fails_explicitly` — an unsupported value raises `ValueError` naming the bad value and the supported set, rather than silently falling back or crashing deep in the call stack.

## 12. Proof that all four current artifacts are generated by the same canonical pipeline

- `pipeline.py`'s `_ADAPTERS = {"pdf": pdf_adapter.build, "epub": epub_adapter.build}` is a single dict shared by every `build_book()` call regardless of language — `test_single_canonical_pipeline_implementation` asserts this identity directly.
- `test_ru_and_pl_route_through_the_identical_adapter_functions` drives all four `(language, format)` combinations through one instrumented pipeline and shows the call sequence is `load → adapter` every time, with no per-language branch in `pipeline.py` (there is none — grep confirms `pipeline.py` has no `if language ==` branching).
- `test_pdf_and_epub_adapters_receive_the_same_canonical_model` shows a single `CanonicalBookModel` instance produced by one `CanonicalBookLoader.load()` call is what both `pdf_adapter.build` and `epub_adapter.build` receive.
- End-to-end: rebuilding all four artifacts (RU×PDF, RU×EPUB, PL×PDF, PL×EPUB) through `book_pipeline.build_book()` and diffing their SHA-256 against the pre-refactor, four-independent-script baseline shows byte-for-byte parity (section 9) — the same content the old four-script architecture produced now comes from the one shared pipeline.

## Acceptance checklist

- [x] Exactly one canonical book-build pipeline exists (`book_pipeline.pipeline.build_book`)
- [x] Language is an input parameter
- [x] Format is an output parameter
- [x] RU and PL do not have independent build implementations
- [x] PDF and EPUB share one canonical content model
- [x] Compatibility scripts are thin wrappers only
- [x] The RU/PL × PDF/EPUB matrix passes (`validate_book.py`, `validate_pagination.py`)
- [x] Output content is unchanged (byte-identical SHA-256, section 9)
- [x] `BOOK-BUILD-PIPELINE-CONTRACT.md` is satisfied
