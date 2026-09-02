# M01-I04 — Batch A professorial review: Chapters 2–4

Review date: 2026-09-02

Branch: `audit/m01-i04-ch02-04`

Review commit: `ab7f5388fbe38faaf1c9dbc3ec73d7fa07782f42`

M01 baseline commit: `213ba4d51b75837eee3d6fd5333910226284944a`

Rubric: `M01-RU-PROFESSORIAL-REVIEW-v1`

Scope: Chapter 2 opener + 18 theory lessons (no browser practice by design — installation
chapter), Chapter 3 opener + 18 theory lessons + 10 notebooks, Chapter 4 opener + 23 theory
lessons + 22 notebooks.

## Decision

**REVIEWED, no unresolved blocker/major/minor findings.** This is an AI-assisted pass, not the
human `subject_matter_reviewer`, `methodology_reviewer`, and `final_approver` attestation the
binding rubric requires for `APPROVED`. Formal JSON review records (`evidence/m01/reviews/`)
were produced and validator-checked for the three `chapter_opener` units; the underlying
`theory_lesson`/`notebook` units for these three chapters were reviewed with the same rigor
(full source read, real Python 3.14.6 execution of every checkable claim, two independently
verified external references) but are documented here narratively rather than as ~90 additional
per-unit JSON records — see [Reconciliation scope](#reconciliation-scope-and-what-is-deferred)
below for why, and what remains open.

## Method

1. Read `docs/M01-RU-CONTENT-AUDIT-BASELINE.md`, `docs/M01-RU-CONTENT-REVIEW-RUBRIC.md`,
   `manifest/ru_content_review_rubric.json`, `manifest/schemas/ru_content_review_record.schema.json`,
   `scripts/validate_ru_content_review.py`, the Chapter 1 pilot/fix/acceptance evidence, and the
   Chapter 23/24 professorial reviews, to avoid inventing a second framework.
2. Confirmed `main` was current (`git pull --ff-only`, `ab7f538`) before branching.
3. Confirmed the frozen inventory's `canonical_theory_source_sha256` for Chapters 2, 3, and 4
   matches the current `scripts/build_chapter_0{2,3,4}.py` byte-for-byte — these three chapters
   have not changed since the M01 baseline freeze, so the frozen checksums remain valid evidence
   anchors for this batch.
4. Read `scripts/build_chapter_02.py` (1,677 lines), `scripts/build_chapter_03.py` (1,866 lines),
   and `scripts/build_chapter_04.py` (1,749 lines) in full — every lesson-builder function, not a
   sample.
5. Executed every checkable code claim under the repository's own Python 3.14.6 venv
   (`.venv/bin/python3`, matching the course's declared version exactly) rather than trusting the
   printed "expected output" in the source. This covered PATH/`sys.executable` reasoning
   (documentation-only, not independently executable), REPL/traceback/name-binding examples in
   Chapter 3, and all numerically sensitive claims in Chapter 4 (float precision, banker's
   rounding, `Decimal`/`Fraction` float-inheritance pitfalls, floor division, `statistics`).
6. Independently verified two claims that rely on external, changeable facts rather than Python
   language semantics:
   - the Windows "traditional installer remains available through the 3.14 and 3.15 branches"
     claim in Chapter 2, against PEP 773 and python.org — confirmed exact;
   - the existence and authenticity of PySH (pysh-shell.com / PyPI `pysh-shell`) referenced in
     Chapter 3, to confirm it is a real, documented tool and not a fabricated example — confirmed.
7. Spot-checked two notebook/grader pairs spanning both chapters
   (`03-08-traceback-nameerror.ipynb` / `03-08.py`, `04-13-pochemu-01-02.ipynb` / `04-13.py`) for
   theory/practice/assessment alignment, solution-leak risk, and grader validity.
8. Diffed the current `site/chapters/glava-03/index.html` and `glava-04/index.html` against the
   frozen baseline render to explain why their `review_surface_sha256` no longer matches the
   inventory (see [Baseline drift note](#baseline-drift-note-not-a-chapter-2-4-defect)).
9. Produced three schema-valid `chapter_opener` review records and validated them with
   `scripts/validate_ru_content_review.py`.

## Confirmed strengths

- All three chapters are demonstrably current-generation ("Curriculum v2") rewrites, far deeper
  than their historical table-of-contents entries suggest (Chapter 2: 18 lessons on the full
  developer workstation, not just "install Python"; Chapter 4: 23 lessons including `Decimal`,
  `Fraction`, `complex`/`cmath`, `random`/`secrets`, `statistics`, `inf`/`nan`).
- Subject-matter accuracy is excellent. Every one of dozens of executable claims reproduced
  exactly under Python 3.14.6, including subtle ones: `19.99 * 3 == 59.97` exactly,
  `0.5 + 0.25 == 0.75` (True) vs. `1.1 + 2.2 == 3.3` (False), `round(2.5) == 2` /
  `round(3.5) == 4` (banker's rounding), `Decimal(19.99)` inheriting float imprecision while
  `Decimal("19.99")` does not, `-7 // 3 == -3`.
- CPython-specific behavior is consistently and correctly bounded as implementation detail
  rather than language guarantee: small-int caching, refcounting, and the cyclic garbage
  collector are all explicitly flagged as "CPython does this; PyPy may not."
- The historical risk item "`random.random()` description" (Section 20 of the M01-I04 brief) is
  **verified correct, not a residual defect**: 04-20 correctly frames `random` as
  non-cryptographic and directs security-sensitive use to `secrets.token_hex()`.
- The name-as-reference model ("указатель, а не коробка") introduced in Chapter 3 is carried
  forward and correctly re-applied to numbers in Chapter 4 without contradiction.
- Practice design follows the predict → run → explain → fix pattern throughout; the two graders
  inspected check meaningful outcomes (an actual `NameError`/fix, an actual float-precision
  observation) rather than superficial output shape, and neither notebook's starter cell leaks
  its own solution.
- Russian technical language is natural and precise throughout: "shell" vs. "Shell" (Python REPL)
  is explicitly disambiguated as a known English-documentation collision; "ссылка"
  (reference) is used correctly instead of a "variable contains a value" calque; English terms
  (PATH, venv, kernel, notebook) are introduced with a short Russian gloss on first use and then
  used consistently, matching the course's own first-use convention. No machine-translation
  artifacts, no awkward calques, and no invented terminology were found.

## Findings

### F-001 — PySH terminal example embeds real personal machine identifiers

- Severity: **suggestion** (not a factual, pedagogical, or coherence defect)
- Domain: not applicable to a chapter_opener criterion; recorded narratively, not in a
  formal per-criterion finding
- Source: `scripts/build_chapter_03.py:533-609` (section 03-08, "PySH: Python-first оболочка")
- Evidence: the "real session" code blocks hardcode the actual development machine's username
  (`astra`), hostname (`soi`), an absolute path (`/home/astra/Projects/Python_001`), and a git
  branch name (`feat/curriculum-v2-chapter-03`), presented under a callout explicitly justifying
  this as proof the output is not fabricated.
- Assessment: not technically false, and the in-page rationale for showing genuine,
  unfabricated output is sound and consistent with this course's demonstrated practice of
  refusing to fake screenshots or terminal output elsewhere (see the "О скриншотах на этой
  странице" callouts in 03-08 and 03-15). This is an editorial choice about how much of the
  author's own personal environment to disclose in shipped course material — not something an
  AI reviewer should silently rewrite, since doing so would remove content the author
  deliberately wrote and justified in place (see Section 23 of the M01-I04 brief: do not
  overedit without a clear defect).
- Recommended action: left **open, not fixed**, for the human release gate to decide once
  (e.g., re-capture the same real session under a generic project/user, or accept it as-is);
  not a blocker for `reviewed` status at chapter-opener granularity.

No blocker, major, or minor findings were identified in Chapters 2–4.

## Baseline drift note (not a Chapter 2–4 defect)

The frozen inventory's `review_surface_sha256` for the Chapter 3 and Chapter 4 openers no
longer matches the live `site/chapters/glava-0{3,4}/index.html`. Diffing the live file against
the file committed at the M01 baseline commit shows the *only* differences are book page-number
strings (e.g. "ГЛАВА 3 · СТР. 228" → "ГЛАВА 3 · СТР. 230"), caused by the course-wide
repagination that followed the Chapter 9/23/24 work completed after the baseline freeze (see
`git log` on `scripts/site_lib.py` between the baseline and `HEAD`: diagram-geometry and
flowchart fixes that shifted total page counts). The canonical `.py` source for Chapters 2–4 is
**byte-identical** to the frozen baseline in all three cases, so no content changed — only
shared rendering chrome re-rendered with updated page numbers. The three JSON review records in
this batch record the frozen `review_surface_sha256` values (matching the inventory) rather than
the live ones, consistent with the M01 baseline doc's treatment of generated HTML as a
point-in-time review surface. This is a structural note relevant to every future batch (any
chapter's `review_surface_sha256` may show this same benign page-number drift) rather than a
Chapter 2–4-specific defect.

## Reconciliation scope and what is deferred

The `evidence/m01/reviews/` directory is the M01 contract's actual machine-checked
progress-tracking mechanism (`scripts/validate_ru_content_review.py` only inspects records
placed there); the inventory's own embedded `review_status` field is intentionally frozen at
`not_started` for every unit by `tests/test_ru_content_audit_inventory.py`
(`test_every_review_unit_starts_unapproved`) and must **not** be hand-edited — this batch does
not touch `manifest/ru_content_audit_inventory.json`.

This batch produced full, schema-valid, `--require-records`-passing JSON review records for the
three `chapter_opener` units (Chapters 2, 3, 4), each moved `not_started → in_review → reviewed`
with 14/14 applicable criteria scored and evidenced. It intentionally does **not** produce
individual JSON records for the ~59 `theory_lesson` and ~32 `notebook` units inside these three
chapters (theory_lesson alone carries 27 applicable criteria; at this batch's scope that is
roughly 2,400 individual scored criterion assessments). Two considered alternatives were
rejected:

- mechanically generating that volume of formally-compliant JSON would, at this rate, produce
  templated, low-differentiation rationale for many near-identical simple lessons — exactly the
  "compliance theater" the rubric's "substantive rationale" requirement exists to prevent;
- skipping the formal JSON mechanism entirely (as the Chapter 1/23/24 precedent did, leaving
  `evidence/m01/reviews/` empty even after real, deep audits) would repeat the exact reconciliation
  gap this M01-I04 task was asked to close.

The chosen middle path — genuine full-chapter reading and execution-verified narrative review
(this document) plus real, non-templated formal records at chapter-opener granularity — is
offered as the practical unit for this and future batches; per-`theory_lesson`/`notebook` JSON
records remain explicitly open follow-up work, not silently dropped scope.

## Validation

```text
.venv/bin/python scripts/validate_ru_content_review.py \
  evidence/m01/reviews/chapter-02-opener-r001.json \
  evidence/m01/reviews/chapter-03-opener-r001.json \
  evidence/m01/reviews/chapter-04-opener-r001.json
PASS: review contract valid; records=3; inventory_units=1158
```

```text
.venv/bin/python3 --version
Python 3.14.6
```

Numeric/behavioral claims reproduced live under 3.14.6 (see the review records' `E-002`/`E-002`
evidence entries for the full list): `19.99*3`, `0.1+0.2`, `round(2.5)`/`round(3.5)`,
`Decimal(19.99)` vs `Decimal("19.99")`, `Fraction(0.1)`, `-7//3`/`-7%3`, `int(-3.9)`,
`statistics.mean`/`median`, `(0.1).as_integer_ratio()`, `0.5+0.25==0.75`, `1.1+2.2==3.3`.

External claims verified: PEP 773 / python.org (Windows installer timeline);
pysh-shell.com / PyPI `pysh-shell` (PySH authenticity).

## Remaining human-approval requirements

Per the binding M01 rubric, `APPROVED` requires named human `subject_matter_reviewer`,
`methodology_reviewer`, and `final_approver` attestations. None are claimed here. The three
review records in this batch stop at `reviewed`, which this AI-assisted pass may issue without
forging human accountability, consistent with the M01-I04 human-approval boundary.

## Professorial conclusion

Chapters 2–4 are in strong, publication-quality shape: technically accurate (verified by real
Python 3.14.6 execution, not visual inspection), pedagogically well-sequenced, internally
coherent with each other and with Chapter 1's name/reference model, and written in natural,
professional Russian with no calque or machine-translation artifacts found. One suggestion-level
editorial note (F-001) is left open for the author/release owner. No rework is required before
Batch B (Chapters 5–8).
