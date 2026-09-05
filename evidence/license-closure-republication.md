# Dual-license closure — publication republication record

## Why this exists

The PDF copyright page previously embedded the full MIT license text from the
repository's root `LICENSE.md` as the book's own license notice, wrongly
implying the entire book (educational content included) was MIT-licensed.
The EPUB had no rights/copyright notice at all. This closure adopts an
explicit dual-license model — see `LICENSE.md`, `LICENSE-CODE.md`,
`LICENSE-CONTENT.md`, and `site/front-matter/litsenziya.html` — and this
document records the resulting publication rebuild.

This record covers two closure rounds:

1. The initial dual-license adoption (CC BY-NC-SA 4.0 for content, MIT for
   software) and its first publication rebuild.
2. A follow-up correction: the website license page originally described
   inline lesson code snippets as part of the CC-licensed prose, while the
   PDF/EPUB notice already said "code" was MIT — an internal inconsistency.
   The binding rule was normalized repository-wide: **all code, including
   inline snippets/listings printed inside lesson text, is MIT**; only
   prose/explanations/diagrams/assignments are CC BY-NC-SA 4.0. This round
   also fixed a real EPUB byte-reproducibility defect discovered while
   rebuilding (see below) — it is no longer merely documented as a caveat.

## Binding licensing model (final)

- **Educational/editorial content** (book/course prose, explanations,
  diagrams, educational illustrations, assignments/instructions, the
  website's own editorial material): Creative Commons
  Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0),
  © Siergej Sobolewski / Cartesian School.
- **Code** — Python/JavaScript source, build/tooling scripts, standalone
  example projects, AND every inline code snippet/listing/example shown
  inside the book/course text itself: MIT (`LICENSE-CODE.md`), unless a
  file/directory states otherwise (e.g. `projects/python/safesort/LICENSE`,
  also MIT). Code never becomes CC-licensed merely by being printed inside a
  CC-licensed lesson page.
- Both the PDF copyright page (`scripts/build_pdf.py::build_copyright_page`)
  and the EPUB's copyright page + `dc:rights` metadata
  (`scripts/build_epub.py::build_copyright_item` / `main`) render the exact
  same shared constants (`build_epub.RIGHTS_NOTICE_PARAGRAPHS_HTML` /
  `RIGHTS_NOTICE_PLAIN`) — the two publication formats cannot independently
  drift on the licensing text. `site/front-matter/litsenziya.html`
  (`scripts/build_license_page.py`) states the identical split for the
  website, including an explicit note on what `<link rel="license">` does
  and does not cover (it describes a page's text/editorial content only,
  never the code samples embedded in it).
- `tests/test_license_consistency.py` (10 tests, letters A–H per the closure
  spec plus two supporting checks) enforces this consistency across
  `LICENSE.md`, `LICENSE-CODE.md`, `README.md`, the website license page,
  the PDF, and the EPUB in one place, including a direct regression guard
  (`test_c_license_page_does_not_classify_inline_snippets_as_cc_only`)
  against the exact inconsistency this round fixed.

## Publication fixed point

- `data/book-pagination.json` (excluding the `pdf_sha256` / `generated_from`
  fingerprint fields, which change with content by design): byte-identical
  across every rebuild in both closure rounds, and to the original
  pre-change committed baseline. Both the shorter copyright notice (round 1)
  and the slightly longer, disambiguated wording (round 2) fit within the
  same single physical page the old notice occupied, so **no chapter start
  pages ever shifted and no chapter regeneration was required**.
- Two full PDF rebuilds from the final (round 2) wording produced
  byte-identical `data/book-pagination.json` and byte-identical
  `book/pdf/готовая книга.pdf`.
- Final physical PDF page count: **4575** (unchanged from the pre-change
  baseline throughout both rounds).
- Chapter 1 start: physical page **18** (unchanged).
- Chapter 23 start: physical page **4026** (unchanged).
- Chapter 24 start: physical page **4438** (unchanged).
- Subject index start: physical page **4572** (unchanged).
- Final PDF SHA-256 (round 2, final wording):
  `a5b7be5f3e2921e89d784505a6ad7090eb9d234d185d1a406ef3ddeeee786ef7`
  (round 1: `80f14d20069d825533ac704b7e96d2baa4b394b516a2a681197d95311462a34a`;
  pre-change baseline: `ee42f84f5f1a10f9542d9119bbcb030b6f3f48ea260b901595dc5dac52bea948`).
- Final EPUB SHA-256 (round 2, final wording, deterministic build):
  `2ba8282bfcc4ca998104e25dd63eae5db231e3203888ca36e82624d407b55c72`
  (round 1: `2fafd5b063a2cc9cf6eed87945c44f657d4b0c301d87553345ace6182412c283`;
  pre-change baseline: `1f939a01af20452f08b139d8dbeb85095e5b7f9ef22143bcd2b72e56f07a7df1`).

## EPUB determinism — fixed (was a documented caveat in round 1; now closed)

Round 1 found that rebuilding the EPUB twice from identical source produced
two files differing only in one `<meta property="dcterms:modified">`
timestamp inside `EPUB/content.opf`, because `ebooklib` stamps it with
`datetime.datetime.now()` unless told otherwise. That was documented as a
pre-existing limitation, not fixed. Round 2 fixes it properly:

- **Root cause, precisely identified**: `ebooklib.epub.EpubWriter._write_opf_metadata`
  (`.venv/lib/python3.14/site-packages/ebooklib/epub.py`) uses
  `self.options["mtime"]` if present, else `datetime.datetime.now()`, for
  `dcterms:modified`. Separately — and *not* fixed by that option alone —
  every ZIP member is written via `zipfile.ZipFile.writestr(plain_filename,
  data)`, and CPython's `zipfile` stamps each such entry's `ZipInfo.date_time`
  with `time.localtime()` at write time. Both are real, independent sources
  of non-determinism; round 1 only measured the first (via content-only
  diffing, which cannot see ZipInfo timestamp bytes).
- **Fix, without touching ebooklib in site-packages**:
  `scripts/build_epub.py` now defines `EPUB_BUILD_MTIME` — a fixed instant
  honoring `SOURCE_DATE_EPOCH` when set (mirroring `build_pdf.py`'s own
  reproducibility contract), clamped to 1980-01-01 (ZIP's DOS date format
  cannot represent anything earlier) when unset. `epub.write_epub(str(OUT),
  book, {"mtime": EPUB_BUILD_MTIME})` fixes the OPF's `dcterms:modified`.
  A new `normalize_epub_zip_determinism()` then reopens the just-written
  file with the stdlib `zipfile` module and rewrites every entry with the
  exact same filename, content, compression method, and other metadata —
  only `date_time` changes, to the same fixed instant — preserving member
  order exactly.
- **Verification, member-by-member, not just top-level SHA-256**: two builds
  separated by a 3-second sleep were compared entry-by-entry —
  `(filename, date_time, compress_type, external_attr, internal_attr,
  create_system, content)` for all **1014** members were identical, member
  order and names were identical, and both raw files hashed to the same
  SHA-256: `2ba8282bfcc4ca998104e25dd63eae5db231e3203888ca36e82624d407b55c72`.
  `epubcheck` reports 0 errors on the resulting file.

## Validation (final, round 2)

- `scripts/validate_book.py`: PASS — PDF 4575 pages, metadata present, 1221
  bookmarks, uniform page size; EPUB epubcheck 0 errors.
- `scripts/validate_pagination.py`: PASS — 24 chapters, 4575 physical pages,
  PDF/TOC/site consistent.
- `scripts/validate_chapter_titles.py`: PASS — 24 openers, 24 journey cards,
  24 practice groups, all practice pages.
- `scripts/validate_diagram_conventions.py`: PASS — 24 chapters, 317 SVG
  diagrams, 633 orthogonal arrows, 246 standard flowchart shapes (untouched
  by this change; re-run as a regression guard).
- `python3 -m epubcheck book/epub/python-s-nulya.epub`: 0 errors.
- PDF determinism: two full rebuilds, byte-identical
  `data/book-pagination.json` and byte-identical PDF SHA-256.
- EPUB determinism: two full rebuilds, byte-identical SHA-256, verified at
  the individual-member level (see above) — no longer just a top-level hash
  coincidence.
- `pytest tests/`: **192 passed** (182 pre-existing + 10 in
  `tests/test_license_consistency.py`, letters A–H plus two supporting
  checks), including `test_ru_content_audit_inventory.py` /
  `test_ru_content_review_contract.py` unchanged —
  `scripts/build_front_matter.py` (the M01-tracked front-matter canonical
  source) was never touched by any round of this closure.
- `scripts/validate_site_catalogs.py`, `scripts/validate_seo.py`: PASS.
- `scripts/validate_navigation.py`: output byte-identical to the pre-change
  baseline (diffed directly) — its ~497 pre-existing "missing notebook"
  warnings for Chapters 22–23 predate this closure entirely.
- `git diff --check`: clean.

## Incidental EPUB CSS fix (discovered in round 1 while rebuilding, not a licensing change)

Rebuilding the EPUB for the first time since the Cartesian mobile-navigation
redesign landed (`site/assets/css/theory.css` gained two `body:has(...)`
rules for the mobile nav-drawer backdrop and hiding the floating
back-to-top button while the drawer is open) surfaced two latent
`epubcheck` `CSS-008` errors: `:has()` is valid modern CSS for browsers but
unsupported by epubcheck's CSS3-level parser — this is the exact same
class of incompatibility `build_epub.py` already documents and works around
for `homepage.css` (see its `project_css` comment). Confirmed pre-existing
and unrelated to this change: `epubcheck` on the previously-committed EPUB
(`git show HEAD:book/epub/python-s-nulya.epub`) reports **zero** errors,
because it was last built before that CSS landed and therefore never
bundled the offending rules.

Fix: `scripts/build_epub.py` strips any CSS rule whose selector contains
`:has(` before embedding `theory.css` into the EPUB
(`strip_has_selector_rules()`) — both affected rules are purely cosmetic,
JS-driven mobile-drawer behavior that means nothing in a reflowable e-reader
(there is no `#mobile-nav-panel` there to react to). The live site's
`theory.css` is untouched; only the EPUB's embedded copy is filtered.

## M01 impact

None, in either round. `scripts/build_front_matter.py` (the canonical
source the M01 inventory hashes for the `ob-avtore` /
`o-tehnicheskom-recenzente` / `vvedenie` front-matter units) was not
modified. The license page lives in its own sibling file,
`scripts/build_license_page.py`, specifically so it never touches those
units' `canonical_source_sha256`. `manifest/ru_content_audit_inventory.json`
is unchanged; `pytest tests/test_ru_content_audit_inventory.py` and
`tests/test_ru_content_review_contract.py` both pass unchanged (records ==
inventory units == 1158, missing == 0). No checksums were rewritten.
Publication artifacts (`book/pdf/*`, `book/epub/*`) are explicitly listed
under M01's own `excluded_from_m01` policy.
