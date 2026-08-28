# M01 — Binding Professorial Content Review Rubric

## Purpose

This document is the binding quality contract for the Russian `Python from Zero`
curriculum. It governs M01 review records for every unit indexed by
`manifest/ru_content_audit_inventory.json`.

M01 asks two different questions:

1. Is the material technically and factually correct?
2. Can an absolute beginner reliably learn the declared outcome from this exact
   sequence, explanation, practice, and assessment?

A unit cannot pass by being strong in only one dimension. A technically correct
but unteachable lesson fails. A friendly but technically false lesson also fails.

## Binding artifacts

The contract consists of four synchronized artifacts:

- `manifest/ru_content_review_rubric.json`: criterion catalog, score scale,
  applicability matrix, reviewer roles, severities, and state transitions;
- `manifest/schemas/ru_content_review_record.schema.json`: portable JSON wire
  format for one unit review;
- `scripts/validate_ru_content_review.py`: executable semantic and approval-gate
  validator;
- this document: the human-readable interpretation and review procedure.

If prose and executable rules conflict, the stricter rule applies and M01-I02
must be corrected before further approvals are issued.

## Unit identity and source binding

Every record binds to one stable `inventory_ref`:

```text
supplementary:<unit-id>
chapter:<NN>:theory:<unit-id>
chapter:<NN>:practice:<lesson-id>
chapter:<NN>:project:<project-id>
```

The record must preserve:

- the frozen M01 baseline commit;
- the canonical source path and its baseline SHA-256;
- the checksum of the source actually reviewed;
- the generated review-surface path and frozen checksum when one exists;
- the exact commit on which the review was completed.

Generated HTML is a review surface, not the editable source. Findings against a
generated page must be corrected in its canonical builder or canonical notebook.

## Score scale

Each applicable criterion receives one integer score. Scores are not averaged.

| Score | Meaning | Gate consequence |
| ---: | --- | --- |
| 0 | Missing, false, or educationally unsafe | Mandatory rework |
| 1 | Major defects prevent dependable learning | Mandatory rework |
| 2 | Substantially correct but incomplete or insufficiently teachable | Mandatory rework |
| 3 | Publication-quality and independently defensible | Passes criterion |
| 4 | Exemplary clarity, precision, and transfer | Passes criterion |

`APPROVED` requires every applicable criterion to score at least 3. A score of 4
cannot compensate for a score of 2 elsewhere.

## Review domains

### Subject matter — `SM`

The subject-matter domain verifies factual correctness, Python 3.14 behavior,
terminological precision, code/explanation alignment, completeness, currency,
security and reliability boundaries, and traceability of normative or
version-sensitive claims.

The reviewer must actively look for false beginner mental models, including:

- confusing variables with boxes instead of bindings where that distinction
  matters;
- confusing equality with identity;
- describing mutability as a property of variable names;
- hiding iterator consumption or generator laziness;
- presenting scope, exception propagation, encoding, asynchronous execution,
  HTTP, filesystems, package management, or security as simpler than they are;
- teaching historical syntax as the preferred modern practice;
- showing code whose real output differs from the narrative.

### Pedagogy — `PD`

The pedagogy domain verifies measurable outcomes, prerequisite discipline,
motivation, intuition, instructional sequence, cognitive load, example
progression, misconceptions, guided practice, independent work, and transfer.

A complete lesson normally follows this learning arc:

```text
motivation
  -> intuition
  -> minimal example
  -> precise model or definition
  -> realistic example
  -> typical mistakes and diagnosis
  -> guided practice with feedback
  -> independent task
  -> retrieval, synthesis, or transfer
```

This is a functional sequence, not a mandatory visual template. A reviewer may
approve a different sequence only when the evidence explains why it better serves
the declared outcome and learner level.

Learning outcomes must describe observable capability. For example:

```text
After this lesson, the learner can select dict for an appropriate problem,
read and update values safely, and explain iteration over keys, values, and pairs.
```

“The learner will know dictionaries” is not measurable and cannot pass `PD01`.

### Coherence — `CO`

The coherence domain verifies course-wide terminology, cross-references,
purposeful repetition, alignment among theory/practice/projects, and stable unit
identity and navigation.

Review is not isolated proofreading. The reviewer must compare the unit with its
prerequisites, adjacent units, related notebook, assessment, and any referenced
project. Contradictory explanations across two individually plausible lessons are
a course defect.

### Practice and assessment — `PA`

The practice domain verifies execution, expected results, instruction clarity,
assessment validity, edge cases, feedback, and safe learner operation.

Execution evidence must name the environment and exact command or notebook path.
Visual inspection of code is not execution evidence. A screenshot is supporting
evidence only; it cannot replace a reproducible result.

## Finding severities

| Severity | Definition | Approval behavior |
| --- | --- | --- |
| `blocker` | False, unsafe, non-runnable, or structurally incapable of teaching the outcome | Must be resolved |
| `major` | Creates a serious misconception, missing prerequisite, invalid assessment, or substantial learning failure | Must be resolved |
| `minor` | Local imprecision, ambiguity, weak example, or consistency defect that still reduces quality | Must be resolved |
| `suggestion` | Optional improvement beyond the publication-quality gate | May remain open |

`accepted_risk` does not close a blocker, major, or minor finding for M01. It may
document a Product Owner decision, but the unit still cannot become `APPROVED`.

## Evidence requirements

Every criterion assessment contains a substantive rationale and at least one
existing evidence reference. Evidence is immutable within a completed revision.

Supported evidence types include:

- source inspection with an exact path and location;
- official Python or upstream project documentation;
- reproducible code execution;
- notebook execution;
- automated test result;
- cross-reference comparison;
- review note explaining a pedagogical judgment;
- diff demonstrating the correction.

For `APPROVED` pedagogical units:

- at least one official-reference item is required;
- theory lessons, notebooks, and projects require passing execution evidence;
- every learning outcome must point to assessment evidence;
- all evidence IDs referenced by criteria, outcomes, and findings must exist.

Official references must support the actual claim. A general Python homepage does
not prove a detailed semantic claim.

## Reviewer accountability

AI systems may inspect sources, execute code, locate authoritative references,
identify risks, propose corrections, and prepare draft evidence. They cannot
independently issue `APPROVED`.

Approval requires accountable human coverage of three roles:

- `subject_matter_reviewer`;
- `methodology_reviewer`;
- `final_approver`.

One qualified human may hold more than one role, but every role must be explicitly
attested. A second independent human review is strongly recommended for the M01
release gate, especially for advanced, security-sensitive, or assessment-heavy
units.

The person named by `decision.decided_by` must be a human reviewer who explicitly
holds `final_approver`.

## Status machine

Only these transitions are allowed:

```text
not_started -> in_review
in_review -> needs_rework | reviewed
needs_rework -> in_review
reviewed -> needs_rework | approved
approved -> needs_rework
```

There is no direct path from `not_started` or `in_review` to `approved`.

- `needs_rework` means at least one binding deficiency remains.
- `reviewed` means the review pass is complete and the unit is ready for the
  explicit approval gate.
- `approved` means every machine and human gate passed for the reviewed checksum.
- any later canonical-source change reopens the unit as `needs_rework` and marks
  dependent translations and books stale in later milestones.

The status history must start at `not_started`, form one continuous chain, and end
at the declared decision status.

## Review procedure

For each unit, the reviewer performs these steps in order:

1. Resolve the `inventory_ref` and verify the canonical source checksum.
2. Read prerequisite, current, and successor units where applicable.
3. State or correct measurable learning outcomes.
4. Perform the full subject-matter review against Python 3.14 and authoritative
   sources.
5. Perform the full pedagogical review at absolute-beginner level.
6. Compare theory, notebook, exercises, assessment, and project expectations.
7. Execute all relevant examples, notebooks, tests, or projects safely.
8. Record every finding with severity, evidence, and required corrective action.
9. Correct canonical sources; regenerate delivery artifacts; rerun evidence.
10. Score every applicable criterion and complete human attestations.
11. Move to `reviewed`; then execute the explicit approval decision.
12. Commit the record under `evidence/m01/reviews/` and validate it.

## Validation commands

Validate the rubric, JSON Schema, inventory binding, and all discovered records:

```bash
python scripts/validate_ru_content_review.py
```

Validate selected records and require at least one:

```bash
python scripts/validate_ru_content_review.py \
  --require-records \
  evidence/m01/reviews/<record>.json
```

An empty evidence directory is acceptable in M01-I02 because this work item
defines the contract. It is not sufficient for the M01 release gate.

## M01-I02 exit criteria

M01-I02 is complete only when:

1. every inventory unit kind has an explicit criterion applicability set;
2. score and severity meanings are unambiguous;
3. false approval by averages, missing evidence, incomplete criteria, unresolved
   findings, AI-only review, checksum drift, or illegal status transitions fails;
4. valid approval and valid rework records pass;
5. the contract validates all 1,158 frozen review units without marking any of
   them reviewed;
6. CI executes the contract tests successfully.

M01-I03 will apply this contract to Chapter 1 as a calibration pilot. Criteria may
be strengthened after the pilot, but already required evidence cannot be silently
discarded or downgraded.
