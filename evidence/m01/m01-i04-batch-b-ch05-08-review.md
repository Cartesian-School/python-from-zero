# M01-I04 — Batch B: Chapters 5-8 professorial review report

1. **Branch:** `audit/m01-i04-ch05-08`
2. **Head SHA:** `ba5c280` (parent content-fix commit: `d86ab31`) — the branch's actual final Head SHA after pushing may be one small metadata commit ahead of this; see the PR for the exact tip.
3. **Chapters reviewed:** 5, 6, 7, 8
4. **Exact inventory count (Chapters 5-8):** 167 units (85 theory lessons + 4 chapter openers + 78 notebooks + 0 standalone projects)
5. **Theory lesson count:** 85 (plus 4 chapter openers, reviewed separately per the established chapter-opener record pattern)
6. **Notebook count:** 78
7. **Project count:** 0
8. **Grader count:** 43 (Ch5: 20, Ch6: 2, Ch7: 3, Ch8: 18 — see item 17 for why Ch6/Ch7 have so few relative to notebook count)
9. **Formal record count:** 167 (163 generated via `scaffold_ru_content_review_records.py` + `compose_ru_content_review_records.py`, plus 4 hand-authored chapter-opener records following the exact schema and precedent established by Batch A's `chapter-0N-opener-r001.json` files — chapter openers all share the literal inventory id `index`, which collides in the dossier-lookup-by-bare-id path used by the compose script's default `--kinds theory_lesson notebook`, so Batch A's own openers were never dossier/compose-driven either)
10. **Missing units:** 0
11. **BLOCKER discovered / resolved / unresolved:** 0 / 0 / 0
12. **MAJOR discovered / resolved / unresolved:** 4 / 4 / 0
13. **MINOR discovered / resolved / unresolved:** 1 / 1 / 0
14. **Russian-language corrections:** One (F-006): removed an unlabeled ternary conditional expression (`X if cond else Y`) from the Chapter 8 e-mail-validation mini-project (08-22), which was the only forward-referenced construct in the chapter without an explicit "Забегаем вперёд" disclaimer. No other Russian-terminology or phrasing defects were found; Chapters 5-8's existing terminology (выражение/инструкция, приоритет, ассоциативность, истинность, неизменяемость, срез, индекс, курс, etc.) was independently reviewed and found precise, natural, and free of calques.
15. **Terminology decisions:** Extended `evidence/m01/ru-technical-terminology.json`/`.md` with 15 new terms (24 → 39 total), covering: expression vs statement, operator precedence, associativity, truthiness, immutability (string), membership (in/not in), index, slice, sequence, escape sequence, raw string, f-string, equality vs identity (== vs is), heading/курс (Turtle), and seed (random module). All existing Batch A terms preserved unchanged (additive extension only, diff-verified).
16. **Chapter 4/5 duplication conclusion:** **Intentional, well-labeled, pedagogically justified repetition — not a defect.** Chapter 5 revisits some Chapter 4 operators (`//`, `%`, `divmod()`) but adds substantial genuinely new content: geometric visualizations, the expression-vs-statement distinction, the full precedence/associativity ladder, formula-translation, a much deeper `math` module (gcd/lcm/factorial/comb/perm/geometry/trig/logarithms vs. Chapter 4's basics only), a much deeper `random` module (randint/randrange/uniform/choice/choices/sample/shuffle/seed vs. Chapter 4's random-vs-secrets basics only), and a debugging-methodology mini-project. Every instance of reused content is explicitly cross-referenced ("мы уже решали эту задачу в главе 4").
17. **Chapter 8 prerequisite/dependency conclusion:** **Explicitly resolved.** A full pass through Chapter 8's actual reading order (not just section-number order) found every for/while/if/in/truthiness forward reference except one is properly labeled with an explicit "Забегаем вперёд" callout naming the future chapter (9, 10, or 11) and bounding the explanation appropriately — including the historically-flagged truthiness risk area (08-05), which correctly scopes its claim to strings only rather than generalizing prematurely. The one gap found (an unlabeled ternary expression at 08-22) was fixed as F-006 by removing the construct entirely (Option B — the smallest fix), since it was not needed for correctness. See the full dependency matrix below. Per instruction, no chapters were reordered and no whole-chapter moves were made.
18. **Canonical files changed:** `scripts/build_chapter_05.py` (F-005), `scripts/build_chapter_08.py` (F-006), `notebooks/chapter-08/08-07-vvod-polzovatelya.ipynb`, `notebooks/chapter-08/08-09-krik-perevorot.ipynb`, `notebooks/chapter-08/08-10-dinamicheskaya-matematika.ipynb` (F-007, surgical cell insertion preserving all pre-existing cell ids/content).
19. **Publication impact:** `site/chapters/glava-05/05-11-skobki-i-formuly.html` and `site/chapters/glava-08/08-22-mini-proekt-parol-i-email.html` regenerated; full publication pipeline re-run (`build_book.py` → all 24 `build_chapter_NN.py` for pagination → `build_index.py`/`build_manifest.py`/`build_site_index.py` → `build_ru_content_audit_inventory.py` → `build_vercel.sh` last); no other chapter's rendered content changed (verified by diff — only the two touched pages differ).
20. **Final PDF page count:** 4535 physical pages (24 chapters + subject index), validated by `validate_book.py` (4535 pages, metadata present, 1221 bookmarks, uniform page size) and `validate_pagination.py` (PDF/TOC/site consistent).
21. **pytest result:** 177 passed, 0 failed.
22. **M01 completeness validator result:** `PASS: review contract valid; records=258; inventory_units=1158` (258 = 91 Batch A + 167 Batch B; `--require-complete-scope` for `--chapters 5 6 7 8` confirms 0 missing units).
23. **GitHub Actions result:** Pending — to be confirmed once pushed and PR opened.
24. **Vercel result:** `bash scripts/build_vercel.sh` passed locally in full (practice manifest, Chapter 23/24 contracts, SafeSort sync, chapter titles, PDF pagination, diagram conventions, navigation, site catalogs, and SEO metadata all green); live Vercel preview to be confirmed once PR is opened.
25. **PR URL:** https://github.com/Cartesian-School/python-from-zero/pull/79

---

## Confirmed defects (discovered → classified → fixed → validated)

### F-005 (MAJOR, resolved) — Chapter 5, factual error in a "wrong answer" comment
`scripts/build_chapter_05.py`'s "Скобки для людей, а не только для Python" example (05-11) computed `4 + 7 + 9 / 3` and labeled the result `# 12.0 — НЕПРАВИЛЬНО!` — but the actual value under Python 3.14 is `14.0` (`9/3=3.0`, `4+7+3.0=14.0`). The comment demonstrating the "wrong" answer was itself wrong. Verified via `.venv/bin/python3 -c "print(4 + 7 + 9 / 3)"` → `14.0`. Fixed by correcting the comment to `# 14.0 — НЕПРАВИЛЬНО!`.

### F-006 (MINOR, resolved) — Chapter 8, unlabeled forward reference
The 08-22 mini-project's e-mail check used `est_tochka_posle = "." in email[email.find("@"):] if est_sobachka else False` — a ternary conditional expression with no forward-reference disclaimer, unlike every other forward-referenced construct in the chapter (all explicitly labeled "Забегаем вперёд"). Verified the ternary was not needed for correctness (the surrounding `and`-chain already short-circuits any wrong value from the no-`@`-found case). Fixed by removing it: `est_tochka_posle = "." in email[email.find("@"):]`. Verified behaviorally identical output for both a valid e-mail and a string with no `@`.

### F-007 (MAJOR × 3, resolved) — Chapter 8, stale generated notebooks
`notebooks/chapter-08/08-07-vvod-polzovatelya.ipynb`, `08-09-krik-perevorot.ipynb`, and `08-10-dinamicheskaya-matematika.ipynb` were stale relative to their own canonical builder (`scripts/build_notebooks_ch08.py`), which already defines and calls an `input_setup()` mock-input helper specifically so `input()`-using notebooks can execute without a live human (per the builder's own module docstring) — but the three committed `.ipynb` files lacked it, failing with `StdinNotImplementedError` under standard automated execution (`scripts/run_notebook.py`), while sibling notebook 08-21 (which had the mock) worked correctly. Discovered by actually executing every Chapter 5-8 notebook rather than trusting committed output cells. Fixed by surgically inserting the missing `input_setup()` markdown+code cells at the exact position the builder specifies in each notebook, preserving every pre-existing cell's id and content byte-for-byte (verified by diff) — a wholesale regeneration was tried first and found to reassign every cell's id randomly (nbformat does not seed them), a general pipeline hazard avoided in favor of the surgical fix.

No blocker-severity or unresolved findings of any severity remain.

## Chapter 8 dependency matrix (HIGH-PRIORITY check)

Concepts searched for: `for`, `while`, `in`, `not in`, iterable, iteration, truthiness, collections, list/string membership, `any`/`all`, boolean coercion, nested control flow. Full `for`/`if`/truthiness/`in`/collections are formally taught starting Chapter 9 (control flow) through Chapter 11 (dicts).

| Lesson | Concepts required | Already taught before Ch8 | Introduced locally (this lesson) | Only formally taught later | Handling |
|---|---|---|---|---|---|
| 08-05 (in, сравнение, истинность) | `in`, truthiness | — | `in`/`not in` (full); truthiness bounded to strings only | Full boolean logic / `if`: Ch9 | Option C — explicit, correctly-bounded disclaimer |
| 08-17 (методы проверки) | `if`/`else` statement | — | Brief inline `if/else` around `isdigit()` | Full `if`/`elif`/`else`: Ch9 | Option C — explicit disclaimer |
| 08-18 (цикл по строке) | `for` loop | — | `for ch in text:` (literal, bounded) | Full `for`: Ch9-10 | Option C — explicit, thorough disclaimer; anchor for all later for-loop reuse |
| 08-06 (форматирование) | `for` + tuple unpacking | Multiple assignment (Ch3-5) | Reuses 08-18's already-disclaimed `for`; tuple-unpacking is a natural generalization of taught multiple assignment | Full `for`/unpacking: Ch9-10 | Reviewed — no fresh disclaimer needed; re-disclaiming an already-covered construct at every subsequent use would be repetitive labeling noise, not a gap |
| 08-19 (генератор приветствий), 08-23 (счётчик слов) | dict literal + `.get()` | — | `.get(key, default)` mechanism explained inline | Full dict: Ch11 | Option C — explicit disclaimer |
| 08-22 (проверка пароля) | `any()` + generator expression | Reuses 08-18's `for` | Explicitly named as "compact form of the loop from 8.13" | Full comprehensions/`and`/`or`: Ch9-10 | Option C — explicit disclaimer |
| 08-22 (проверка email) | Ternary conditional expression | — | *(was unlabeled — F-006)* | Full conditional expressions: not formally covered by name in this course | **Fixed via Option B** — removed, since unnecessary for correctness |

**Conclusion:** every forward reference in Chapter 8 is either genuinely new-but-disclaimed (Option C, done correctly throughout) or a natural extension of already-taught material not requiring a fresh disclaimer — with the single exception of the ternary expression, now fixed. No chapter reordering was performed or is recommended; the existing Chapter 8 → 9 → 10 → 11 sequencing is sound as designed.

## Notebook/grader execution summary

Every one of the 78 Chapter 5-8 notebooks was executed via `scripts/run_notebook.py` (Chapters 6-7 under `xvfb-run` for real Turtle rendering; Chapters 5 and 8 headless). All executed cleanly after the F-007 fix. Chapter 6's real-rendered Turtle pipeline was independently re-validated via `scripts/validate_chapter_06_outputs.py` (33/33 non-empty PNGs) and Chapter 7's via `scripts/validate_chapter_07_outputs.py` (39/39). All 43 graders' expected values (including every seeded-random value: `seed(1)→randint(1,10)==3`, `seed(3)→sample(range(1,6),k=3)==[2,5,4]`, `seed(5)→randint(1,100)==80`, `seed(42)→randint(1,100)==82` reproducibly) were independently re-derived against the actual Python 3.14.6 interpreter and confirmed correct.

The low grader-to-notebook ratio for Chapter 6 (2/18) and Chapter 7 (3/22) was investigated and confirmed intentional, not a gap: the vast majority of those chapters' notebooks are local-required Turtle exercises whose correct output is a rendered drawing, not a machine-checkable printed value — there is no automated way to grade "did this draw the right picture" in a browser-based Pyodide grader. The chapters compensate with dedicated browser-gradeable companion notebooks (06-19/06-20, 07-23/07-24/07-25) that restate the same core formula or reasoning as pure arithmetic/prediction exercises requiring no live window, and those are exactly the ones with graders.
