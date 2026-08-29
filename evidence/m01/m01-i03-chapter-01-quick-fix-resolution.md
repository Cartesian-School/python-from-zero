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

## Still open

- **F-007:** real browser execution evidence under the declared Python/Pyodide 3.14 runtime.
- **F-008:** accountable human subject-matter, methodology, and final approval attestations.
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
- `git diff --check`: PASS.
- Browser/Playwright suite: not executed because project dependencies are not installed in the
  review workspace; no false PASS is recorded.

## Decision

Quick textual and contract corrections are complete. Chapter 1 remains **NEEDS REWORK** only
for the real Python 3.14 browser evidence and required human approval gate. No architectural
reordering is authorized by this resolution.
