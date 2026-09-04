# M01-I04 — Batch F: Chapters 21-24 professorial review closure

## Identity and immutable states

- Repository: `Cartesian-School/python-from-zero`
- Branch: `audit/m01-i04-ch21-24`
- Base `main` / merge-base SHA: `f16b5c49034ebbc3614fa1285ec5686d748fa6f2`
- Audited-content commit: `f3d5bd4a302881b6012c2271ab56a7a805377ddb`
- Formal-record/contract commit: `b1511c0b5ea9fc4bf86a7e7f2124875a677155cd`
- Final report commit: the commit containing this file. This wording intentionally avoids a self-referential SHA loop.
- Inventory baseline declared by `manifest/ru_content_audit_inventory.json`: `213ba4d51b75837eee3d6fd5333910226284944a`
- Interpreter used for execution evidence: Python 3.14.6.

The formal records bind their `reviewed_source_sha256` values to the exact source blobs in the audited-content commit. The report and record commits are deliberately separate from that content state.

## Exact scope and counts

Batch F contains **223 inventory units**:

| Chapter | Theory inventory units | Chapter openers | Theory lessons excluding opener | Notebooks | Standalone projects | Total |
|---:|---:|---:|---:|---:|---:|---:|
| 21 | 27 | 1 | 26 | 15 | 1 | 43 |
| 22 | 37 | 1 | 36 | 22 | 1 | 60 |
| 23 | 73 | 1 | 72 | 24 | 7 | 104 |
| 24 | 16 | 1 | 15 | 0 | 0 | 16 |
| **Total** | **153** | **4** | **149** | **61** | **9** | **223** |

Browser grader count is **35**: Chapter 21 has 7, Chapter 22 has 14, Chapter 23 has 14, and Chapter 24 has none. Chapter 23's other 10 notebooks are intentionally `local-required`.

The final terminology register contains **84 terms**. Batch F did not add speculative synonyms. The Chapter 23 late packaging correction uses the exact current PyPA object distinctions and is recorded as F-23-L01.

Whole-inventory closure additionally supplied **13 previously uncovered records** outside Batch F: nine Chapter 1 units and four supplementary/front-matter/index units. These are reported separately and are not included in the 223-unit Batch F count.

## Findings and disposition

Exactly **15 findings were recorded; 15 are resolved; 0 are unresolved**.

| Severity | Discovered | Resolved | Unresolved |
|---|---:|---:|---:|
| Blocker | 1 | 1 | 0 |
| Major | 6 | 6 | 0 |
| Minor | 8 | 8 | 0 |
| Suggestion | 0 | 0 | 0 |
| **Total** | **15** | **15** | **0** |

Original accepted findings remain resolved:

- Chapter 21: F-001 through F-006.
- Chapter 22: F-101 through F-103.
- Chapter 23: F-201 through F-203.
- Chapter 24: F-301.

Late Chapter 23 consolidation findings are separately represented:

- **F-23-L01 — packaging terminology drift — RESOLVED.** The stale hybrid `distribution/build project` language was replaced with current PyPA distinctions among import package, Project, Project Source Tree, Distribution Package/Archive, and Installed Project. The output validator was updated to enforce the corrected vocabulary.
- **F-23-L02 — obsolete Git official-source URLs — RESOLVED.** The old `/download/win` and `/download/mac` paths were replaced with the verified official `https://git-scm.com/install/windows` and `https://git-scm.com/install/mac` destinations. The generated 64-entry source manifest and exact-source validator agree.

Chapter 24's stale validation expectations were confirmed as **consolidation/validator drift**, not a new learner-facing defect. The builder and rendered output agreed on the accepted declined Russian labels and the intentional Chapter 22 deep link. The output validator now checks the actual invariants—non-empty contextual label, correct chapter route, `.html` target, and target existence—and uses the localized terms. The sources validator now enforces the documented `2026-09-03` audit date. No F-24-L01 was created.

## Publication fixed point

Publication reached a fixed point at **pass 2**, based on sidecar hash equality rather than page-count equality:

- Pass 1 pagination SHA-256: `10d4b6e3f7fda8d6caf0cba84f0db5df04d96352e2eab86d1d17944f21cc02a4`
- Pass 2 pagination SHA-256: `10d4b6e3f7fda8d6caf0cba84f0db5df04d96352e2eab86d1d17944f21cc02a4`
- Final physical PDF page count: **4573**
- Chapter 23 start: physical page **4024**
- Chapter 24 start: physical page **4436**
- Subject index start: physical page **4570**
- Final PDF SHA-256: `124cb84976265d4935a964c7fcf54d7f525a5a8523ae5d6db8f58b0b079d2ad8`
- Final EPUB SHA-256: `a3ad09be3411e4a4678eaa25819e3695cce397243476f702797e67f0a1dbe774`

`scripts/validate_book.py` passed: PDF metadata, 4,573 uniform pages, and 1,221 bookmarks are valid; EPUBCheck reported zero errors.

## Execution and validation evidence

- Normal repository suite under working Xvfb: **182 passed, 0 failed**.
- SafeSort suite: **85 passed, 0 failed**.
- Chapter 21 notebooks: **15/15** executed successfully top-to-bottom under the repository runner/Xvfb environment.
- Chapter 22 notebooks: **22/22** executed successfully top-to-bottom.
- Chapter 23 practice contracts: **24/24** validated; 14 browser graders and 10 local-required exercises; untouched starters fail, published solutions pass, and no solution is prefilled.
- Chapter 24 notebooks: **0**, by design.
- Chapter 21 output validator: PASS, 30 required screenshots.
- Chapter 22 output validator: PASS, 12 required screenshots.
- Chapter 23 output validator: PASS, 67 canonical generated pages and 10/10 Git-branded H1 contracts.
- Chapter 23 source validator: PASS, 64 exact official sources.
- Chapter 23 practice validator: PASS.
- Chapter 24 output validator: PASS, 16 canonical pages.
- Chapter 24 source validator: PASS, 36 authoritative references.
- Pagination validator: PASS, 24 chapters and 4,573 physical pages consistent across PDF, TOC, and site.
- Chapter-title validator: PASS, 24 openers, 24 journey cards, 24 practice groups, and all practice pages.
- Full site build: PASS. It validated the 493-unit practice manifest, Chapter 23 upstream/source/output/practice contracts, Chapter 24 source/output contracts, 317 SVG diagrams, 633 orthogonal arrows, 246 standard flowchart shapes, 1,146 navigable pages with no broken links/fragments, 24 chapter cards, 493 practice cards, 13 project cards, SEO for 1,146 pages, and a 666-URL sitemap.
- Final post-site inventory regeneration: byte-identical; its four deterministic inventory tests passed.
- Whitespace gate: `git diff --check` PASS.

## Formal M01 closure

- Batch F formal records: **223**.
- Whole-inventory closure records added in this branch: **236** (223 Batch F plus 13 pre-existing uncovered units).
- Full formal record count: **1158**.
- Full inventory count: **1158**.
- Missing units: **0**.
- Duplicate or extra record coverage: **0**.
- JSON Schema validation: **1158/1158 records PASS**.
- Whole runtime contract: `PASS: review contract valid; records=1158; inventory_units=1158`.
- Whole completeness mode: `PASS: review contract valid; records=1158; inventory_units=1158`; missing = 0.
- Scoped Chapters 21-24 completeness: `PASS: review contract valid; records=1158; inventory_units=1158`; all 223 scoped units are covered and scoped missing = 0.

The review-record schema and runtime validator were narrowly extended to admit both established `F-NNN` identifiers and chapter-scoped late identifiers of the form `F-NN-LNN`. Positive coverage for `F-23-L01` and negative coverage for malformed identifiers are included in the contract tests.

## Deterministic regeneration gate

The repository's GitHub Actions sequence was reproduced from clean formal-record commit `b1511c0b5ea9fc4bf86a7e7f2124875a677155cd`:

1. regenerate Chapter 23 notebooks and graders;
2. regenerate Chapter 23 pages and source manifest;
3. regenerate practice pages and Chapter 24;
4. regenerate subject index, coverage manifest, and site index;
5. run the full repository and SafeSort suites;
6. run `scripts/build_vercel.sh`;
7. require `git diff --exit-code` and `git diff --check`.

Result: **CI-REGENERATION-CLEAN**. The earlier pre-record fixed-point check also produced identical complete diff hashes before and after regeneration (`9142e1bf973d8ff205fce1504cc4985f9589e00979c97cc2b97c9340a5721af1`).

## Final disposition

Batch F is technically ready for Product Owner review. All substantive and late findings are resolved, Chapter 24 validator drift is closed without inflating learner-defect counts, publication and inventory are stable, tests and validators are green, and the formal M01 inventory has no gaps. The pull request must remain unmerged pending explicit Product Owner review.
