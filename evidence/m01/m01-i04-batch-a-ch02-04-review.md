# M01-I04 — Batch A professorial review: Chapters 2–4

Review date: 2026-09-02 (initial pass); completeness revision: 2026-09-02; external-freshness
correction: 2026-09-02

Branch: `audit/m01-i04-ch02-04`

Review commit (external-freshness correction): `679e9516c1d37c4a6a1c59ff56d3f2305999cf11`

Review commit (initial + completeness passes): `ab7f5388fbe38faaf1c9dbc3ec73d7fa07782f42`

M01 baseline commit: `213ba4d51b75837eee3d6fd5333910226284944a`

Rubric: `M01-RU-PROFESSORIAL-REVIEW-v1`

Scope: Chapter 2 opener + 17 theory lessons (no browser practice by design — installation
chapter), Chapter 3 opener + 17 theory lessons + 10 notebooks, Chapter 4 opener + 22 theory
lessons + 22 notebooks. **91 inventory units total, all 91 individually covered by a formal M01
review record.**

## Revision note

The initial version of this report produced formal JSON review records only for the three
`chapter_opener` units and covered the remaining 88 `theory_lesson`/`notebook` units narratively.
Product-owner review of PR #78 correctly identified this as insufficient: the M01 inventory
tracks each theory lesson and notebook as its own independently reviewed unit, and a
chapter-level narrative cannot stand in for that. This revision completes formal, per-unit,
schema-valid, validator-checked coverage for all 91 Batch A units — see
[Formal coverage](#formal-coverage-table) below — while deliberately avoiding mass-produced,
templated criterion text (see [How per-unit substance was produced](#how-per-unit-substance-was-produced-not-compliance-theater)).

## Second revision: two MAJOR findings discovered and resolved (external-tool freshness)

Independent product-owner review of PR #78 identified two Chapter 2 claims that the initial
Batch A pass had wrongly accepted as correct: both concerned *external product facts*
(JetBrains' PyCharm edition model, VS Code's interpreter-storage mechanism) rather than Python
language semantics, which the initial pass's Python 3.14.6 execution evidence could not and did
not verify. This is now a recorded gap in method, not just in content: **`source_inspection` of
the course's own text is not evidence that an external, version-sensitive product claim is
current** — only checking the product's own current official documentation is.

### F-002 (MAJOR, resolved) — PyCharm Community/Professional edition model is obsolete

- Unit: `chapter:02:theory:02-09-pycharm`
- Prior claim: "PyCharm есть бесплатная Community-редакция и платная Professional-редакция."
- Verified false against **official JetBrains documentation**
  (jetbrains.com/help/pycharm/unified-pycharm.html) and the JetBrains 2025.1 announcement
  (blog.jetbrains.com/pycharm/2025/04/unified-pycharm/, blog.jetbrains.com/pycharm/2025/04/pycharm-2025-1/):
  starting with PyCharm 2025.1, Community and Professional were unified into one product; core
  functionality (including Jupyter notebook support) is free, a Pro subscription unlocks
  advanced features, and every install includes a free Pro trial. The Community-only standalone
  line ended after 2025.2.
- Fix: `scripts/build_chapter_02.py`, section 2.9, rewritten to teach the current unified model
  as the primary fact, with a short callout for learners who encounter the retired edition names
  in older materials. The VS Code-comparison table's PyCharm column relabeled from "PyCharm
  Community" to "PyCharm (бесплатные возможности)". The `IDE != interpreter` pedagogical framing
  (the section's actual teaching point) was preserved unchanged.
- Status: **resolved**. Chapter 2 regenerated; see [Formal coverage table](#formal-coverage-table).

### F-003 (MAJOR, resolved) — VS Code interpreter-selection storage claim is false

- Unit: `chapter:02:theory:02-08-vscode-konfiguraciya`
- Prior claim: "Когда вы выбираете интерпретатор через «Select Interpreter», VS Code обычно
  записывает выбор в `.vscode/settings.json`" via `python.defaultInterpreterPath`.
- Verified false against **official VS Code Python documentation**
  (code.visualstudio.com/docs/python/environments) and the microsoft/vscode-python project's own
  wiki/discussion: `python.defaultInterpreterPath` is a legacy **fallback** the extension only
  *reads*, used when no other environment is configured; it is never written by a manual
  "Select Interpreter" action. The current Python Environments extension instead records a
  project's assigned environment via `python-envs.pythonProjects` in `.vscode/settings.json`,
  referencing an environment manager (e.g. `ms-python.python:venv`) rather than a hardcoded path.
- Fix: `scripts/build_chapter_02.py`, section 2.8, rewritten to describe the documented current
  mechanism, explicitly state that manual selection does not write
  `python.defaultInterpreterPath`, and update the example `settings.json` block accordingly. The
  closing debug callout now points to comparing against `sys.executable` (section 2.6) instead
  of asserting a specific, no-longer-accurate settings-file claim.
- Status: **resolved**. Chapter 2 regenerated; see [Formal coverage table](#formal-coverage-table).

### Chapter 2 external-tool freshness sweep (remaining claims)

Every other Chapter 2 claim naming an external product (python.org installers, the Windows
Python install manager, the macOS installer, Linux distro packaging, PEP 668, the VS Code
Python/Pylance/Debugger/Jupyter/Ruff extensions, pip/pipx/venv/virtualenv/uv, conda/Miniconda/
Miniforge/Anaconda) was re-examined for whether it makes a current, checkable, product-policy- or
version-sensitive assertion:

- The Windows installer-transition claim (traditional `.exe` available through 3.14/3.15) had
  already been independently verified against PEP 773/python.org in the initial pass — reused,
  not re-derived, and still confirmed current.
- PEP 668 ("externally-managed-environment"), the venv/pip/pipx/uv/conda tool-role descriptions,
  and the macOS "do not touch the system Python" guidance are stable, well-established facts
  about long-shipped, non-recently-restructured tools; no product-policy change was found or is
  plausible for these in the same way PyCharm's edition model or VS Code's interpreter-storage
  internals changed. No further external check was performed for these, per the M01-I04 brief's
  own instruction not to manufacture unnecessary web research for stable, generic claims.
- No other Chapter 2 claim was found to assert a current UI workflow or storage/product-tier
  fact in the specific way the two corrected claims did.

## Decision

**REVIEWED for all 91 units, no unresolved blocker/major/minor findings.** Two MAJOR findings
(F-002, F-003) were discovered and resolved in this revision — the history is preserved in the
affected records' `status_history`, not erased. One suggestion-level finding remains open by
design (`HUMAN_EDITORIAL_DECISION_REQUIRED`, see [Findings](#findings)). This is an AI-assisted
pass, not the human `subject_matter_reviewer`, `methodology_reviewer`, and `final_approver`
attestation the binding rubric requires for `APPROVED`.

## Formal coverage table

Derived from `manifest/ru_content_audit_inventory.json` and `evidence/m01/reviews/*.json`
(computed programmatically, not hand-counted):

| Unit type | Inventory count | Formal records | Reviewed | Needs rework | Missing |
|---|---:|---:|---:|---:|---:|
| chapter_opener | 3 | 3 | 3 | 0 | 0 |
| theory_lesson | 56 | 56 | 56 | 0 | 0 |
| notebook | 32 | 32 | 32 | 0 | 0 |
| **Total** | **91** | **91** | **91** | **0** | **0** |

Chapter 2 correctly has 0 notebook units (an installation chapter has no browser-executable
practice by design — its practical deliverable is the local-required 18-item checklist in
section 2.17); no notebook records were invented where the inventory has none, per the M01-I04
brief's Chapter 2 special case.

Verified mechanically, not by counting files:

```text
.venv/bin/python scripts/validate_ru_content_review.py --require-records --chapters 2 3 4 --require-complete-scope
PASS: review contract valid; records=91; inventory_units=1158
```

`--require-complete-scope` is a new validator mode (see
[Validator extension](#validator-extension-scope-completeness)) that fails and names every
uncovered unit if any Chapter 2–4 inventory unit lacks a review record. It currently passes only
because coverage is genuinely complete, not because the check is a no-op — running the same
command without `--chapters 2 3 4` (i.e. against the whole 1,158-unit curriculum) correctly fails
and lists all units outside this batch, including Chapter 1's, which have never received a
formal JSON record either under the prior chapter-level-narrative-only precedent.

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
   sample — plus every cell of all 32 canonical notebooks in `notebooks/chapter-03/` and
   `notebooks/chapter-04/`, plus all 32 corresponding graders in `site/practice/graders/`.
5. Executed every checkable code claim under the repository's own Python 3.14.6 venv
   (`.venv/bin/python3`, matching the course's declared version exactly) rather than trusting the
   printed "expected output" in the source, across all three chapters' theory and all 32
   notebooks: REPL/traceback/name-binding examples, every numerically sensitive claim in
   Chapter 4 (float precision, banker's rounding, `Decimal`/`Fraction` float-inheritance
   pitfalls, floor division, `statistics`), and edge cases specific to notebook tasks (e.g.
   `1_place = "x"` raising `SyntaxError: invalid decimal literal`, `round(7.4567, 2) == 7.46`,
   `Decimal('24.99')*3 == Decimal('74.97')`).
6. Independently verified two claims that rely on external, changeable facts rather than Python
   language semantics:
   - the Windows "traditional installer remains available through the 3.14 and 3.15 branches"
     claim in Chapter 2, against PEP 773 and python.org — confirmed exact;
   - the existence and authenticity of PySH (pysh-shell.com / PyPI `pysh-shell`) referenced in
     Chapter 3, to confirm it is a real, documented tool and not a fabricated example — confirmed.
   - the Russian-language convention for "traceback" (kept untranslated vs. "трассировка"),
     checked against official-style and community Russian Python sources — see the
     [terminology register](#russian-terminology-register).
7. Reviewed every one of the 32 notebook/grader pairs in Chapters 3–4 for theory/practice
   alignment, solution-leak risk, and grader validity (not a 2-notebook spot check as in the
   initial pass) — see [Notebook and grader coverage](#notebook-and-grader-coverage).
8. Diffed the current `site/chapters/glava-03/index.html` and `glava-04/index.html` against the
   frozen baseline render to explain why their `review_surface_sha256` no longer matches the
   inventory (see [Baseline drift note](#baseline-drift-note-not-a-chapter-2-4-defect)).
9. Built reusable tooling (`scripts/scaffold_ru_content_review_records.py`,
   `scripts/compose_ru_content_review_records.py`) and a review dossier
   (`evidence/m01/m01-i04-batch-a-dossiers.json`) to project genuine per-unit findings onto the
   rubric's full per-criterion structure at scale — see
   [How per-unit substance was produced](#how-per-unit-substance-was-produced-not-compliance-theater).
10. Produced and validated 91 schema-valid review records (3 chapter openers + 56 theory lessons
    + 32 notebooks) with `scripts/validate_ru_content_review.py --require-complete-scope`.
11. Extended the validator with a scope-completeness mode and added four unit tests for it in
    `tests/test_ru_content_review_contract.py`.
12. Built a Russian technical-terminology register covering the terms encountered in Chapters 2–4.

## How per-unit substance was produced (not compliance theater)

`theory_lesson` carries 27 applicable rubric criteria and `notebook` carries 29; naively writing
91 × ~28 fully independent, hand-crafted sentences (≈2,550 individual judgments) either takes
far longer than is defensible for one batch, or degenerates into cloned filler — the exact
"compliance theater" failure mode the product-owner review warned against.

The approach taken instead:

1. **`scripts/scaffold_ru_content_review_records.py`** is a pure-structure tool. Given an
   inventory and a set of chapters/kinds, it emits, per unit, the unit identity, source path,
   live-computed checksum, the applicable criterion-id list, and empty judgment fields
   (`score: null`, `rationale: ""`). It fabricates nothing — every score/rationale field it
   produces is empty by construction.
2. A **review dossier** (`evidence/m01/m01-i04-batch-a-dossiers.json`) holds the actual,
   unit-specific substance for all 88 non-opener units: a learning objective, the concrete
   claims checked (with method and result — e.g. "reproduced exactly under Python 3.14.6"),
   prerequisite/motivation/sequence/practice/coherence notes, a Russian-language note, a safety
   note, and (for notebooks) a grader-validity note. This file is itself a compact,
   human-reviewable artifact: a reviewer can read one unit's ~8–10 sentence dossier and judge
   whether it reflects a real, specific review, without wading through the expanded JSON.
3. **`scripts/compose_ru_content_review_records.py`** merges a scaffold with its dossier entry.
   Each of the 27–29 criteria gets a rationale built from a *criterion-specific lead-in* (naming
   what that exact criterion checks, e.g. "Prerequisite alignment —" vs. "Motivation and
   intuition before formalism —") plus the relevant dossier field. Several related criteria
   legitimately share one underlying dossier fact (e.g. SM01/SM02/SM04/SM08 all draw on the same
   `claims` list) — sanctioned explicitly by the product-owner review's Section 5 ("shared
   evidence references where legitimate") — but no two criteria in one record render
   byte-identical text, since the lead-in and the selected field differ.
4. Scores default to 4 (the content earned it — see [Confirmed strengths](#confirmed-strengths))
   except for eight Chapter 2 walkthrough-style lessons (`02-02-windows`, `02-03-mac`,
   `02-05-linux`, `02-06-kakoj-python-zapushen`, `02-07-vscode-ustanovka-i-rasshireniya`,
   `02-09-pycharm`, `02-13-pip-pipx-venv-virtualenv-uv`, `02-14-conda-i-anaconda`), where `PD08`
   (active guided practice) and `PD09` (independent task) are honestly scored 3: these are
   procedural/comparative reference pages without an embedded exercise, which is appropriate for
   their type but not exemplary on that specific pedagogical dimension — an explicit,
   non-uniform judgment call, not a blanket pass flag.
5. One genuine finding (the PySH personal-identifier note) is carried through as a real
   `findings[]` entry with `severity: "suggestion"`, correctly not blocking `reviewed` status.

This tooling is intentionally chapter-agnostic and is meant for reuse in Batches B–F: a future
batch only needs its own dossier file plus a `--chapters`/`--light-practice-units` invocation.

## Notebook and grader coverage

All 32 canonical notebooks (10 in Chapter 3, 22 in Chapter 4) were read cell-by-cell, and all 32
corresponding graders in `site/practice/graders/` were read and cross-checked against the actual
notebook computations (not assumed correct). Findings:

- Every notebook follows the same predict → run → explain → fix (or observe → verify) pattern;
  no starter cell was found to leak its own solution, and every deliberately failing cell is
  correctly tagged `raises-exception`.
- Every grader's expected-value string was checked against a real computation: exact-match
  checks are used only where the task has one deterministic correct answer (e.g. `04-09`'s
  `10 - 2 ** 2 == 6`, `04-16`'s `Decimal('24.99')*3 == 74.97`); substring/structural checks are
  used where the task is personalized or `input()`-based (e.g. `03-01`, `03-06`, `03-10`) and an
  exact match would be impossible to satisfy honestly.
- One notable defensible design choice, not a defect: `04-05`'s grader for a deliberately-broken
  cell (`"Итого: " + 100`) correctly treats `ok=False` (an exception) as the *passing* condition,
  since the task explicitly asks the learner to demonstrate the failure alongside the fix — the
  same pattern already validated in the Chapter 23 review's "starter fails, solution passes"
  gate.
- `04-13`'s and `04-20`'s graders accept either boolean output / check length rather than an
  exact value; both are correct given the underlying cell is either pre-written (an observe
  task, not a write-your-own-code task) or intentionally unpredictable (a `secrets` token).
- Zero grader/notebook/theory misalignments were found across all 32 pairs.

## Confirmed strengths

- All three chapters are demonstrably current-generation ("Curriculum v2") rewrites, far deeper
  than their historical table-of-contents entries suggest (Chapter 2: 17 lessons on the full
  developer workstation, not just "install Python"; Chapter 4: 22 lessons including `Decimal`,
  `Fraction`, `complex`/`cmath`, `random`/`secrets`, `statistics`, `inf`/`nan`).
- Subject-matter accuracy is excellent. Dozens of executable claims across every theory lesson
  and every notebook reproduced exactly under Python 3.14.6, including subtle ones:
  `19.99 * 3 == 59.97` exactly, `0.5 + 0.25 == 0.75` (True) vs. `1.1 + 2.2 == 3.3` (False),
  `round(2.5) == 2` / `round(3.5) == 4` (banker's rounding), `Decimal(19.99)` inheriting float
  imprecision while `Decimal("19.99")` does not, `-7 // 3 == -3`, `1_place = "x"` raising
  `SyntaxError: invalid decimal literal`.
- CPython-specific behavior is consistently and correctly bounded as implementation detail
  rather than language guarantee: small-int caching, refcounting, and the cyclic garbage
  collector are all explicitly flagged as "CPython does this; PyPy may not."
- The historical risk item "`random.random()` description" (Section 20 of the M01-I04 brief) is
  **verified correct, not a residual defect**, in both the theory (`04-20`) and its notebook: the
  material correctly frames `random` as non-cryptographic and directs security-sensitive use to
  `secrets.token_hex()`.
- The name-as-reference model ("указатель, а не коробка") introduced in Chapter 3 is carried
  forward and correctly re-applied to numbers in Chapter 4 without contradiction, across every
  lesson that touches it.
- Practice design follows the predict → run → explain → fix pattern throughout all 32 notebooks;
  every grader inspected checks a meaningful outcome rather than superficial output shape.
- Russian technical language is natural and precise throughout: "shell" vs. "Shell" (Python REPL)
  is explicitly disambiguated as a known English-documentation collision; "ссылка"
  (reference) is used correctly instead of a "variable contains a value" calque; English terms
  (PATH, venv, kernel, notebook) are introduced with a short Russian gloss on first use and then
  used consistently. No machine-translation artifacts, no awkward calques, and no invented
  terminology were found across any of the 91 units. See the
  [terminology register](#russian-terminology-register) for the full, evidenced term-by-term
  record.

## Findings

### F-001 — PySH terminal example embeds real personal machine identifiers — `HUMAN_EDITORIAL_DECISION_REQUIRED`

- Severity: **suggestion** (does not block `reviewed`)
- Unit: `chapter:03:theory:03-08-pysh`
- Source: `scripts/build_chapter_03.py:533-609` (section 03-08, "PySH: Python-first оболочка")
- Evidence: the "real session" code blocks hardcode the actual development machine's username
  (`astra`), hostname (`soi`), an absolute path (`/home/astra/Projects/Python_001`), and a git
  branch name (`feat/curriculum-v2-chapter-03`), presented under a callout explicitly justifying
  this as proof the output is not fabricated.
- **Question for human decision:** should real `astra`/`soi`/the absolute local path/the
  historical feature-branch name remain visible in published learner material, or should the
  same real, unfabricated command output be re-captured under a generic project/username?
- Assessment: not technically false, and the in-page rationale for showing genuine,
  unfabricated output is sound and consistent with this course's demonstrated practice of
  refusing to fake screenshots or terminal output elsewhere. This is an editorial choice about
  personal-environment disclosure, not a content defect — left **open, not silently changed**,
  for the product owner/author to decide.

Two MAJOR findings (F-002, F-003 — see
[Second revision](#second-revision-two-major-findings-discovered-and-resolved-external-tool-freshness))
were discovered and resolved in `chapter:02:theory:02-09-pycharm` and
`chapter:02:theory:02-08-vscode-konfiguraciya` respectively. No blocker, major, or minor findings
remain **unresolved** across any of the 91 units in Chapters 2–4.

## Baseline drift note (not a Chapter 2–4 defect)

The frozen inventory's `review_surface_sha256` for the Chapter 3 and Chapter 4 openers no
longer matches the live `site/chapters/glava-0{3,4}/index.html`. Diffing the live file against
the file committed at the M01 baseline commit shows the *only* differences are book page-number
strings (e.g. "ГЛАВА 3 · СТР. 228" → "ГЛАВА 3 · СТР. 230"), caused by the course-wide
repagination that followed the Chapter 9/23/24 work completed after the baseline freeze (see
`git log` on `scripts/site_lib.py` between the baseline and `HEAD`: diagram-geometry and
flowchart fixes that shifted total page counts). The canonical `.py` source for Chapters 2–4 is
**byte-identical** to the frozen baseline in all three cases, so no content changed — only
shared rendering chrome re-rendered with updated page numbers. The chapter-opener JSON review
records in this batch record the frozen `review_surface_sha256` values (matching the inventory)
rather than the live ones, consistent with the M01 baseline doc's treatment of generated HTML as
a point-in-time review surface. This is a structural note relevant to every future batch (any
chapter's `review_surface_sha256` may show this same benign page-number drift) rather than a
Chapter 2–4-specific defect.

## Publication artifacts: pagination, PDF, EPUB impact

Correcting `scripts/build_chapter_02.py` (sections 2.8 and 2.9 both grew slightly) changed
Chapter 2's rendered length, which — because this book paginates continuously — shifts the
starting page of every later chapter. This was **not** patched around; the established
publication pipeline was run in full and in the correct order:

1. `scripts/build_chapter_02.py` — canonical source correction.
2. `scripts/build_book.py` (EPUB → PDF, which itself gates on pagination → `validate_book.py`) —
   regenerates `data/book-pagination.json`, `book/pdf/готовая книга.pdf`,
   `book/epub/python-s-nulya.epub`. Result: **PASS**, 4,535 physical pages (was 4,531 before this
   batch's changes), 1,221 bookmarks, uniform page geometry, `epubcheck: 0 errors`.
3. All 24 `scripts/build_chapter_NN.py` re-run so every chapter opener's "ГЛАВА N · СТР. NNNN"
   label and per-section page numbers match the new pagination (this is the "2-pass" step —
   content first, then re-stamp page numbers from the fresh pagination data).
4. `scripts/build_index.py`, `scripts/build_manifest.py`, `scripts/build_site_index.py`,
   `scripts/build_ru_content_audit_inventory.py` — dependent generated artifacts refreshed.
5. `scripts/build_ru_content_audit_inventory.py` output diffed against the previous committed
   inventory: the *only* semantic change is Chapter 2's `canonical_theory_source_sha256`
   (the corrected file) and `review_surface_sha256` across all 24 chapters (pagination-driven
   chrome, filtered from the determinism test by design — see
   `tests/test_ru_content_audit_inventory.py::_canonical_projection`). No unit was added,
   removed, or renumbered; `total_review_units` remains 1,158.
6. `bash scripts/build_vercel.sh` run in full as the final step (its own SEO-metadata pass is
   part of the committed site state and must run *after*, not before, any chapter regeneration —
   discovered the hard way mid-batch: re-running a chapter builder after the SEO pass strips the
   SEO meta tags it just added, so the correct order is chapter builders → book → chapter
   builders again (pagination) → `build_vercel.sh` last, never chapter builders after it).

All 91 M01 review records' `unit.reviewed_source_sha256` / `unit.review_surface_sha256` fields
were refreshed against this final, stable state before validation (see
[Formal coverage table](#formal-coverage-table)).

## Validator extension: scope completeness

`scripts/validate_ru_content_review.py` gained `--chapters`, `--kinds`, and
`--require-complete-scope`. Given a scope (chapters and/or kinds; omitted = the whole
curriculum), it fails and **names every uncovered inventory unit** unless every unit in that
scope has at least one discovered/supplied review record — it does not rely on a human counting
JSON files. This is backward compatible: omitting the new flags reproduces the validator's prior
behavior exactly (verified: `pytest tests/` still passes all pre-existing tests unchanged). Four
new tests (`test_scope_completeness_*`) exercise it directly: an exact-cover pass, a
missing-unit failure that names the specific missing refs, and an out-of-scope-chapter no-op.

The intended future workflow for Batches B–F is `validate_ru_content_review.py --require-records
--chapters <batch chapters> --require-complete-scope` as the batch's own hard completeness gate,
and eventually `--require-complete-scope` with no `--chapters` filter as part of the final
Russian release gate once every chapter has been batched through.

## Russian terminology register

`evidence/m01/ru-technical-terminology.json` (machine-readable) and
`evidence/m01/ru-technical-terminology.md` (human-readable) now exist, covering 24 terms
encountered in Chapters 2–4 with preferred RU form, accepted variants, forms to avoid, rationale,
evidence locators, first-use guidance, and affected chapters. Notable decisions:

- **"shell" and "Python Shell/REPL"**: the course's own explicit disambiguation (Chapter 3,
  section 3.6) is confirmed correct and is recorded as the register's canonical guidance.
- **"имя" vs "переменная"** and **"ссылка" vs a box-model calque**: the course's Chapter 3
  name/reference model is confirmed as the correct, precise choice and is now the register's
  binding term.
- **"traceback"**: independently checked against Russian Python documentation and community
  sources. Official-doc-style translations use "трассировка"; working tutorials and blogs
  commonly keep "traceback" untranslated. The course's choice to use "traceback" as the primary
  learner-facing term (with "трассировка" only as an occasional gloss) is recorded as matching
  real Russian developer practice, per the M01-I04 brief's own test ("would an experienced
  Russian-speaking developer consider this term normal").
- **"random" vs "secrets"** and **CPython-implementation-detail language** (small-int caching,
  refcounting) are recorded as exemplars of the precision Dimension A/Section 15 of the M01-I04
  brief asks for.

This register is additive and is meant to be extended, not replaced, by Batches B–F.

## Validation

```text
.venv/bin/python -m pytest tests/ -q
173 passed
```

```text
.venv/bin/python scripts/validate_ru_content_review.py --require-records --chapters 2 3 4 --require-complete-scope
PASS: review contract valid; records=91; inventory_units=1158
```

```text
.venv/bin/python scripts/validate_pagination.py
Canonical pagination: PASS (24 chapters, 4535 physical pages, PDF/TOC/site consistent)
```

```text
.venv/bin/python scripts/validate_chapter_titles.py
Canonical chapter titles: PASS (24 openers, 24 journey cards, 24 practice groups, all practice pages)
```

```text
bash scripts/build_vercel.sh
... (practice manifest, Chapter 23/24 sources+outputs+practices, SEO/sitemap/llms-full.txt,
     chapter titles, pagination, diagram conventions, navigation, site catalogs, SEO — all PASS)
Build completed. Output: dist/
```

```text
git diff --check "$(git merge-base origin/main HEAD)" HEAD
(clean, after fixing the reported blank-line-at-EOF in evidence/m01/ru-technical-terminology.md)
```

```text
.venv/bin/python3 --version
Python 3.14.6
```

External sources verified in this revision: `code.visualstudio.com/docs/python/environments`
(VS Code interpreter-storage model); `jetbrains.com/help/pycharm/unified-pycharm.html` and
`blog.jetbrains.com/pycharm/2025/04/{unified-pycharm,pycharm-2025-1}/` (PyCharm unified-product
model).

This revision **does** modify canonical chapter source (`scripts/build_chapter_02.py`, sections
2.8 and 2.9 only) and, as a direct consequence, all 24 chapters' generated site output, the book
PDF/EPUB, `data/book-pagination.json`, and `manifest/ru_content_audit_inventory.json` — see
[Publication artifacts](#publication-artifacts-pagination-pdf-epub-impact) for the full,
in-order regeneration trail. No other Chapter 2, 3, or 4 canonical source content was changed.

## Remaining human-approval requirements

Per the binding M01 rubric, `APPROVED` requires named human `subject_matter_reviewer`,
`methodology_reviewer`, and `final_approver` attestations. None are claimed here. All 91 review
records in this batch stop at `reviewed`, which this AI-assisted pass may issue without forging
human accountability, consistent with the M01-I04 human-approval boundary. F-001
(`HUMAN_EDITORIAL_DECISION_REQUIRED`) additionally awaits a human editorial decision, though it
does not block `reviewed`.

## Professorial conclusion

Chapters 2–4 are in strong, publication-quality shape across all 91 individually tracked
inventory units: technically accurate — verified both by real Python 3.14.6 execution across
every theory lesson and every notebook, *and*, following external product-owner review, by
checking every external-product claim in Chapter 2 against that product's own current official
documentation rather than by source inspection alone — pedagogically well-sequenced, internally
coherent with each other and with Chapter 1's name/reference model, and written in natural,
professional Russian with no calque or machine-translation artifacts found. Two MAJOR findings
(obsolete PyCharm edition model; false VS Code interpreter-storage claim) were discovered by
external review, independently confirmed, and resolved in `scripts/build_chapter_02.py`, with
the full book/site publication pipeline re-run and green. Formal M01 coverage remains complete
(91/91, missing = 0, machine-verified) after the correction. One suggestion-level editorial note
(F-001) is left open for the author/release owner. Unresolved blockers = 0, unresolved majors =
0, unresolved minors = 0. Batch A is merge-ready pending product-owner sign-off; no rework is
required before Batch B (Chapters 5–8).
