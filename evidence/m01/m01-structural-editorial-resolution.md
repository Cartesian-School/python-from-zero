# M01 — structural and editorial resolution after review parts I–II

Resolution date: 2026-08-29

Scope: all confirmed findings in the supplied two-pass review. Claims withdrawn by the reviewer
are recorded but intentionally do not trigger changes.

| Finding | Source and evidence | Weight | Decision and correction | Acceptance test |
|---|---|---:|---|---|
| Chapter 8 forward prerequisites | §8.12, §8.13 and §8.22 used truthiness, `if`, loops and dictionaries before Chapters 9–11 | High | Keep stable chapter URLs; make §8.13 a complete, condition-free local introduction, defer frequency dictionaries to Chapter 11, and describe Chapter 10 as systematic treatment rather than first exposure | §8.13 requires no `if`; §8.22 word count requires no dictionary; Chapter 10 states “systematic treatment” |
| Duplicate practice ownership | 19 current collisions found by DOM analysis; one exercise appeared as new on multiple theory pages | High | Preserve stable practice IDs and saved progress. One page owns each exercise; later uses are explicitly marked “Повторное применение” and do not claim new progress | `validate_editorial_structure.py` reports 493 unique owners and zero collisions |
| Orphan practice 04-03 | Published in the catalog but absent from its numeric-type theory page | High | Attach 04-03 to `04-03-vidy-chisel.html` | Validator reports that page as the sole owner of 04-03 |
| Chapter 20 feedback gap | Industry survey 20.6–20.13 interrupted the path from first ball to the game-loop core | High | Reading/navigation order is now 20.1–20.5 → technical core 20.14–20.28 → industry appendix 20.A1–20.A8 → packaging/release → final project; four real subsections receive explicit `a` suffixes | Validator asserts the boundary-page order and navigation validation checks links; the opener contains no blank section labels |
| Chapter 23 unnumbered material | 28 substantial entries had blank section numbers | High | Introduce `23.0` (project brief), explicit 23A (Git), 23B (Projects), 23B.A (optional appendix), 23C (SafeSort implementation) and 23D (homework) labels | Every Chapter 23 `.section-item` has a non-empty `.si-num` |
| Chapter 2 homepage status | Homepage called a hands-on installation chapter “theory only” | High | Show “практика на вашем компьютере” | Generated Chapter 2 roadmap card contains the corrected label |
| Technical-review wording | Reference card implied that an independent reviewer had checked the book | Medium | Rename the page/card to technical-check status and state automated verification plus the unfilled independent-review role | Generated title, description and reference card contain no completed-review claim |
| PySH disclosure/runtime | Optional author-owned tool was presented as ordinary core material; recorded sessions used Python 3.13.5 | Medium | Mark optional status and authorship; align recorded runtime labels with the declared 3.14.7 build | Generated PySH page contains disclosure and no `Python 3.13.5` |
| Chapters 4/5 overlap | Arithmetic was presented twice without a clear route for a prepared learner | Medium | Define Chapter 4 as representation/types and 5 as reliable computation; mark 5.1–5.7 as diagnostic consolidation with an explicit skip route to new material | Chapter 5 opener contains the scope boundary and skip route; `random.random()` wording agrees in both chapters |
| Legacy Chapter 23 stubs | Six moved pages remained indexable in sitemap | Medium | Keep compatibility pages, add `noindex, follow`, exclude them from sitemap | SEO generation plus structural validator check all six URLs |
| `debug=True` warning delay | First Flask example enabled debug mode 29 sections before its warning | Low | Add immediate local-only warning and forward link to §22.34 | Generated §22.5 contains `debug=True`, “только при локальной разработке”, and `22.34` |
| MRO heading scope | Heading promised general MRO while teaching only single inheritance | Low | Rename to method lookup; add a bounded note about C3 and multiple inheritance | Generated §14.16 uses the new title and contains `C3-линеаризацию` |
| Russian counters | Generated counters used one grammatical form for every number | Low | Add Russian plural rules and avoid inflection-sensitive live-progress wording | Homepage contains `1 практическое задание`, `22 практических задания`, `493 практических задания` |
| `random.random()` range | Chapter 4 omitted the exclusive upper endpoint | Low | State `[0.0, 1.0)` in words | Both Chapter 4 and 5 generated examples say that 1.0 is excluded |
| `is` with a literal | Warning omitted CPython's diagnostic | Low | Add the exact `SyntaxWarning` and required response | Generated §9.17 contains `SyntaxWarning` and “Did you mean \"==\"?” |
| Chapter 5 practice count | Opener said 21 while the manifest contains 20 | Low | Correct the opener to 20 | Generated Chapter 5 opener says `20 практик` |
| PDF page marketing | Homepage label presented layout pages as content volume | Low | Relabel as “Страниц в PDF-макете” | Generated homepage uses the bounded label |

## Findings withdrawn or already resolved

- Browser-labelled GUI practices: withdrawn after notebook import verification; no change.
- Stable-ID gaps in Chapters 20–22: withdrawn after section-by-section reconciliation; no renumbering.
- Chapter 23 homework/title mismatch: already resolved before this work; compatibility pages retained.
- Algorithm definition and PEP 3000/3100 roles: resolved in M01-I03.
- Python 3.14.7 availability: the earlier “unlikely version” concern is rejected; GitHub Actions
  already executed the repository on Python 3.14.7.

## Architectural rule

Public practice IDs and URLs are durable identifiers, not section ordinals. They are not mass
renumbered when editorial order changes because that would break bookmarks, external links and
learner progress. Displayed section numbers describe reading order; the new validator enforces
unique exercise ownership and makes intentional revisits explicit.

## Final verification

- Canonical PDF: 4531 physical pages, WeasyPrint 69.0.
- PDF SHA-256: `7f824ff5a8a7e98cae0b7c4d30ccb70f1cecce4ae977e5dfd1886058852a788d`.
- Determinism: two consecutive builds from identical inputs produced the same SHA-256.
- Pagination: 24 chapter openers, PDF table of contents, bookmarks and website page labels agree.
- Practice structure: 493 unique owners, zero unexplained gaps and zero duplicate new-practice cards.
- Deployment validation: 1146 pages; zero broken local links/fragments; catalogs and SEO pass.
- Automated tests: 237 passed, 1 skipped. Fourteen GUI-project tests require `xvfb-run`, which
  is not installed in this workspace; those tests remain assigned to the Linux CI environment.
- Visual inspection: Chapter 5 opener, Chapter 8 contents and revised word-count project,
  Chapter 20 opener, and Chapter 23 opener rendered without clipping, overlap or missing glyphs.
- Environment limitation: `validate_book.py` validated the PDF but could not invoke the optional
  Python `epubcheck` wrapper because that module is not installed locally. Deployment, navigation,
  catalog, SEO, structure, pagination, syntax and PDF checks are unaffected; CI remains the
  authoritative EPUB validation gate.
