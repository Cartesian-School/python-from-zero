# M01-I03 — pilot full subject-matter and methodology review of Chapter 1

Review date: 2026-08-29  
Repository: `Cartesian-School/python-from-zero`  
Review commit: `213ba4d51b75837eee3d6fd5333910226284944a`  
Rubric: `M01-RU-PROFESSORIAL-REVIEW-v1`  
Scope: Chapter 1 opener, seven theory lessons, notebook `01-01`, and its grader.

## Decision

**NEEDS REWORK.** Chapter 1 is fundamentally sound, welcoming, and suitable for a true
beginner, but it cannot pass the binding approval gate while the findings below remain open.
This is an AI-assisted pilot review, not the required human subject-matter, methodology, and
final approval.

## Reviewed sources

| Unit | Canonical/review source | SHA-256 |
|---|---|---|
| Chapter 1 canonical generator | `scripts/build_chapter_01.py` | `2cbf1b7704286dfb35ac1f470b2f520ec966c8e4a5cf601888e7a9e7a1787cb4` |
| Chapter opener | `site/chapters/glava-01/index.html` | `a3e37c801e9ef8d4bd053f5688cc5d353bff5c098f09dcfabfd0e9ced7b8f29b` |
| Lessons 1.1–1.7 | `site/chapters/glava-01/*.html` | All eight inventory-bound surface hashes reproduced exactly |
| Practice 01-01 | `notebooks/chapter-01/01-01-dobro-pozhalovat.ipynb` | `a0b828db2326b03478d952f5a17d617f69394f6cb11075d54f72b673980e5aa5` |
| Practice grader | `site/practice/graders/01-01.py` | `681894ed178cfc44a840477c5ef733bb60ad48862629c4d58fbf2260712dd542` |

## Learning outcomes reconstructed for review

After Chapter 1 the learner should be able to:

1. distinguish a program, source code, algorithm, statement, expression, interpreter,
   compiler, bytecode, and virtual machine at an introductory level;
2. explain why CPython is commonly called interpreted without claiming that compilation never
   occurs;
3. place the principal Python milestones from ABC/CWI through Python 3.14 in chronological
   order;
4. distinguish python.org, docs.python.org, PyPI, PSF, PEPs, CPython, PyPy, and MicroPython;
5. identify realistic Python application areas and important boundaries;
6. execute simple `print(...)` expressions, rebind a name, and treat an error message as
   diagnostic information;
7. describe effective study habits for the remainder of the course.

## Confirmed strengths

- The two-level interpreter explanation avoids the common false claim that Python is never
  compiled and introduces CPython bytecode without making it a prerequisite for practice.
- The historical sequence and dates inspected in the chapter are internally coherent.
- The chapter explicitly presents limitations of Python instead of marketing it as universal.
- The name-to-value model is substantially better than the misleading “variable as a box”
  model for later aliasing and mutation topics.
- The notebook begins with zero prerequisites, uses immediate feedback, includes guided and
  independent practice, an intentional error, `type()`, `help()`, and the Zen of Python.
- The practice manifest binds notebook 01-01 to the browser runner and an automatic grader.

## Findings

### F-001 — inaccurate definition of algorithm

- Severity: **major**
- Criteria: `SM01`, `SM03`, `SM05`, `CO01`
- Source: `scripts/build_chapter_01.py`, lesson 1.1, “Алгоритм, инструкция, выражение”
- Evidence: an algorithm is described as a recipe that “always leads to one result”. This
  omits termination/bounded completion and incorrectly makes deterministic output universal;
  randomized algorithms and algorithms with external input need not produce one fixed result.
- Required correction: define an algorithm as a finite, unambiguously specified sequence of
  steps transforming permitted inputs into a result or terminating state; keep the recipe only
  as an intuition and acknowledge dependence on inputs/conditions.
- Acceptance test: the phrase `всегда приводит к одному результату` is absent; the replacement
  contains a finiteness/termination boundary and does not exclude randomized algorithms.

### F-002 — PEP 3100 is assigned the wrong documentary role

- Severity: **minor**
- Criteria: `SM01`, `SM08`, `CO02`
- Source: `scripts/build_chapter_01.py`, lesson 1.2, Python 3 transition callout
- Evidence: PEP 3100 is presented as the complete and exact list of reasons for moving to
  Python 3. Its stated role is a collection of miscellaneous Python 3.0 plans, not a complete
  rationale for the transition.
- Required correction: cite PEP 3000 for the Python 3000 plan and “What’s New In Python 3.0”
  for user-visible changes; retain PEP 3100 only as a detailed change-plan reference.
- Acceptance test: no sentence describes PEP 3100 as the complete list of reasons; all links
  resolve to authoritative Python documentation.

### F-003 — learning outcomes are implicit rather than measurable

- Severity: **minor**
- Criteria: `PD01`, `PD10`
- Source: Chapter 1 opener and lesson 1.7 summary
- Evidence: the opener describes topics and duration, while the closing summary lists content
  encountered. Neither states observable “after this chapter you can…” outcomes.
- Required correction: add a short outcome block using observable verbs such as distinguish,
  explain, identify, execute, and diagnose; align the closing retrieval questions with it.
- Acceptance test: each declared outcome maps to at least one lesson or practice check.

### F-004 — introductory interpreter wording still over-compresses execution

- Severity: **minor**
- Criteria: `SM03`, `SM04`, `PD05`
- Source: lesson 1.1 opening and level-1 explanation
- Evidence: wording says the interpreter turns source into actions the computer understands and
  that translation and execution occur “as if simultaneously”. The level-2 correction is good,
  but the opening can still create a direct source-to-machine mental model.
- Required correction: state that this is a deliberately simplified model and that CPython
  compiles to bytecode executed by its evaluation loop; avoid implying direct translation to
  processor instructions.
- Acceptance test: level 1 and level 2 do not contradict one another when read literally.

### F-005 — notebook teaches names before the theory sequence introduces them

- Severity: **minor**
- Criteria: `PD02`, `CO04`, `PA03`
- Source: notebook 01-01 “Типичная ошибка” and Chapter 1 navigation
- Evidence: the notebook explains an unquoted word as a variable/function name, while the
  formal name-to-value lesson 1.6 comes later. The notebook is linked from lesson 1.5, before
  lesson 1.6.
- Required correction: either introduce the minimal concept immediately in the notebook as a
  local definition, or move the practice link after lesson 1.6.
- Acceptance test: the learner does not need unexplained terms to understand the intended
  `NameError`.

### F-006 — grader verifies output shape but not the declared three semantic categories

- Severity: **minor**
- Criteria: `PA04`, `PA05`
- Source: `site/practice/graders/01-01.py`
- Evidence: the basic task asks for name, favourite colour, and a number, but the grader accepts
  any three non-empty lines. The advanced task requests text, a number, and an arithmetic
  result, but the grader checks only one line with at least three whitespace-separated tokens.
- Required correction: either label the checks honestly as structural participation checks or
  instrument the runner so the grader can validate cell source/values without leaking answers.
- Acceptance test: grader names and logic measure the same contract and reject a trivial output
  that does not attempt the requested categories.

### F-007 — Python 3.14 execution evidence is absent in this pilot environment

- Severity: **major**
- Criteria: `SM02`, `PA01`, `PA02`
- Source: notebook 01-01, browser runner declaration, and review environment
- Evidence: the repository declares Python/Pyodide 3.14, but the available local interpreter
  is Python 3.12.13. No Python 3.14 execution was fabricated. The intentionally failing
  `print(Привет)` cell also requires expected-error semantics in the runner.
- Required correction: execute the notebook and grader through the declared Pyodide 3.14
  browser runner, capture runtime version, per-cell outcomes, expected error classification,
  and final grader result.
- Acceptance test: captured runtime begins with `3.14`; all normal cells pass; the intentional
  NameError is classified as expected; grader result and runner logs are retained.

### F-008 — final human approval roles remain unfulfilled

- Severity: **major**
- Criteria: approval gate, not a content defect
- Source: binding rubric `M01-RU-PROFESSORIAL-REVIEW-v1`
- Evidence: approval requires human `subject_matter_reviewer`, `methodology_reviewer`, and
  `final_approver`; this pilot was performed by an AI assistant.
- Required correction: after content rework and execution evidence, obtain named human
  attestations and record the permitted status transitions.
- Acceptance test: validator passes an `approved` record containing all three required human
  roles and no open blocker/major/minor finding.

## Rubric score summary

| Domain | Result |
|---|---|
| Subject matter | Strong core; blocked by F-001, F-002, F-004, F-007 |
| Pedagogy | Good motivation and pacing; outcomes and prerequisite alignment need repair |
| Coherence | Navigation is coherent; notebook/name ordering needs repair |
| Practice and assessment | Useful first experience; execution evidence and grader validity are incomplete |

No score of 3 or 4 is asserted as an approval attestation. The binding process requires
evidence per criterion and human accountability after rework.

## Pilot conclusion

Chapter 1 does not require structural rewriting. It requires targeted corrections to the
algorithm definition, documentary references, learning outcomes, interpreter wording, the
practice sequence, and grader contract, followed by a real Python 3.14 browser execution and
human review. The appropriate state is `needs_rework`.
