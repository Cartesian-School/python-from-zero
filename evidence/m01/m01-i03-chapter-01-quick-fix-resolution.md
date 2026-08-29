# M01-I03 — Chapter 1 quick-fix resolution

Resolution date: 2026-08-29
Approved review baseline: `213ba4d51b75837eee3d6fd5333910226284944a`
Scope: approved quick corrections only; no Chapter 8–10 architecture change.

## Resolved findings

| Finding | Resolution | Acceptance evidence |
|---|---|---|
| F-001 | Replaced deterministic recipe wording with a finite, unambiguous, input-bounded definition that allows randomness. | Forbidden phrase removed from canonical generator and generated HTML. |
| F-002 | Reassigned PEP 3000, What's New In Python 3.0, and PEP 3100 to their correct documentary roles. | No complete-rationale claim remains for PEP 3100. |
| F-003 | Added six observable Chapter 1 learning outcomes. | Generated lesson begins with `После этой главы вы сможете`; each outcome maps to chapter content or practice. |
| F-004 | Rewrote the introductory execution model as an explicit simplification and aligned it with CPython bytecode execution. | Level 1 no longer implies direct source-to-processor translation or simultaneous translation/execution. |
| F-005 | Defined “name” locally before the intentional `NameError` notebook cell. | The learner no longer needs the later variable lesson to understand the error. |
| F-006 | Renamed grader checks as structural participation checks, matching what stdout-only evidence can actually prove. | Check labels no longer claim semantic validation of name, colour, numeric type, or expression provenance. |
| R-002 | Reconciled the generated inventory baseline with M01-I03A commit `213ba4d…`; updated the locked test expectation. | Deterministic inventory comparison passes and all 1,158 stable unit identities remain covered. |

## Final gate resolution

- **F-007 — closed:** the release owner confirmed manual browser execution of practice `01-01`
  at `https://www.cartesianschool.org/practice/01-01/index.html` on 2026-08-29.
- **F-008 — closed:** the release owner accepted the subject-matter and methodology review in
  the roles of subject-matter reviewer, methodology reviewer, and release owner.
- **R-006:** Chapter 8–10 prerequisite architecture remains deliberately deferred.
- Full-course candidate findings from the submitted report remain carried forward until each is
  reproduced against the reconciled commit.

## Validation

- Chapter 1 generator: deterministic rebuild PASS.
- M01 inventory generator: deterministic rebuild PASS.
- Review-contract validator: PASS; 1,158 inventory units.
- Inventory contract tests: 4/4 PASS through direct function execution.
- Review contract tests: 9/9 PASS through direct function execution.
- Python compilation: PASS for modified Python sources.
- Notebook JSON parsing: PASS.
- SEO validation: PASS for 1,146 pages, sitemap, and robots.
- Canonical PDF rebuild: PASS; 4,529 physical pages, SHA-256
  `b5cb5a301b31e3cfd43083aaeb9cbf7c1068707742e43e3f23a89a30bdfd3bde`.
- PDF portability: PASS; the required emoji fallback is repository-pinned and checksum-locked,
  so rendering no longer depends on host-installed fallback fonts.
- PDF semantic extraction: PASS for the reviewed Chapter 1 targets (`pypdf` 6.16.1).
- PDF determinism: PASS; two independent renders produced identical PDF and pagination hashes.
- PDF visual inspection: PASS for pages 18, 22, 24, 26, and 39 (learning outcomes,
  algorithm, interpreter levels, and PEP correction); no clipping, overlap, or broken glyphs.
- `git diff --check`: PASS.
- Full site build: PASS, including all manifest, source, notebook/grader, navigation, catalog,
  pagination, and SEO validators.
- Local nongraphical test selection: 156 PASS; 14 graphical tests require `xvfb-run`, which is
  unavailable in the review container. The preceding GitHub Actions run passed all 170 course
  tests and 85 SafeSort tests on Python 3.14.7 before stopping only at the now-corrected stale
  pagination fingerprint.
- Browser/Playwright automation was not executed; the approved manual browser check closes F-007
  for this content-review milestone.

## Decision

Chapter 1 is **ACCEPTED** for M01-I03. All findings F-001–F-008 are resolved or accepted by the
release owner. No Chapter 8–10 architectural reordering is authorized by this resolution.
