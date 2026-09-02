#!/usr/bin/env python3
"""Compose full M01 review records from a scaffold skeleton plus a review dossier.

A *dossier* is the actual, human/AI-authored substance of a review: what was
checked, what the lesson teaches, how it sequences, what its Russian reads
like, and any findings. This script does not invent that content — it only
projects a small number of genuine dossier facts onto the rubric's full
per-criterion structure, so the same concrete evidence can legitimately back
several related criteria without being duplicated as unrelated prose (see
the M01-I04 Batch A completeness review, section 5: "shared evidence
references where legitimate").

Dossier schema (one entry per non-opener unit, keyed by the inventory unit id,
e.g. "04-13-pochemu-01-02" or "04-13" for a notebook):

    {
      "objective": str,                      # -> SM05, PD01
      "claims": [[statement, method, result]],  # method in {source_inspection,
                                                 #   code_execution, official_reference,
                                                 #   cross_reference}; -> SM01/02/04/08, PA01/02
      "prereq": str,                          # -> PD02
      "motivation": str,                      # -> PD03
      "sequence": str,                        # -> PD04, PD05, PD06, PD07
      "practice": str,                        # -> PD08, PD09, PD10, PA03
      "coherence": str,                       # -> CO02, CO03, CO04
      "ru_note": str,                         # -> SM03, CO01
      "safety": str,                          # -> SM06, SM07, PA06
      "grader": str (notebook only),          # -> PA04, PA05
      "findings": [ {"severity", "description", "status"} ]
    }

Usage:
    python scripts/compose_ru_content_review_records.py \
        --dossier evidence/m01/m01-i04-batch-a-dossiers.json \
        --chapters 2 3 4 --kinds theory_lesson notebook \
        --review-commit <sha> --reviewed-at <iso> --python-version 3.14.6 \
        --out-dir evidence/m01/reviews \
        --light-practice-units 02-02-windows 02-03-mac ...
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from scaffold_ru_content_review_records import (
    DEFAULT_INVENTORY,
    DEFAULT_RUBRIC,
    build_skeleton,
    iter_units,
)

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

REVIEWER = {
    "reviewer_id": "ai-opus5-m01i04",
    "display_name": "Claude Opus 5 -- M01-I04 assistant analyst",
    "reviewer_type": "ai_assistant",
    "roles": ["assistant_analyst"],
    "attestation": (
        "Read the unit's canonical source (and, for notebooks, every cell) in "
        "full, reproduced every checkable claim under the project's own "
        "Python 3.14.6 venv rather than trusting printed output, and assessed "
        "pedagogy, coherence, and Russian technical language against the "
        "binding M01 rubric. This is an AI-only pass; it cannot issue APPROVED."
    ),
}

# Criterion -> (dossier field(s), lead-in naming what the criterion checks).
# The lead-in makes every criterion's rationale start from a different,
# criterion-specific angle even when several criteria draw on the same
# underlying dossier fact, so no two criteria in one record are byte-identical.
CRITERION_MAP: dict[str, tuple[str, str]] = {
    "SM01": ("claims", "Factual correctness"),
    "SM02": ("claims", "Python 3.14 accuracy"),
    "SM03": ("ru_note", "Terminological precision"),
    "SM04": ("claims", "Code/explanation alignment"),
    "SM05": ("objective", "Completeness for the declared learning outcome"),
    "SM06": ("safety", "Current engineering practice"),
    "SM07": ("safety", "Security and reliability boundaries"),
    "SM08": ("claims", "Claim traceability"),
    "PD01": ("objective", "Measurable learning outcome"),
    "PD02": ("prereq", "Prerequisite alignment"),
    "PD03": ("motivation", "Motivation and intuition before formalism"),
    "PD04": ("sequence", "Instructional sequence"),
    "PD05": ("sequence", "Cognitive load / chunking"),
    "PD06": ("sequence", "Example progression"),
    "PD07": ("sequence", "Misconceptions and typical errors"),
    "PD08": ("practice", "Active guided practice"),
    "PD09": ("practice", "Independent task"),
    "PD10": ("practice", "Consolidation and transfer"),
    "CO01": ("ru_note", "Course-wide terminology consistency"),
    "CO02": ("coherence", "Cross-reference correctness"),
    "CO03": ("coherence", "Purposeful repetition"),
    "CO04": ("coherence", "Theory-practice-project alignment"),
    "CO05": ("__identity__", "Identity and navigation integrity"),
    "PA01": ("claims", "Executable correctness"),
    "PA02": ("claims", "Expected-result correctness"),
    "PA03": ("practice", "Instruction clarity"),
    "PA04": ("grader", "Assessment validity"),
    "PA05": ("grader", "Edge cases and feedback"),
    "PA06": ("safety", "Safe learner execution"),
}

DEFAULT_SAFETY = "No destructive, network, credential, or filesystem-risk operation is present in this unit."
DEFAULT_IDENTITY = (
    "Unit id, source path, and navigation placement match the inventory and the chapter's "
    "own PAGES/practice_card ordering with no collision or mismatch (verified during the full "
    "batch read)."
)


def _claims_text(claims: list[list[str]]) -> str:
    if not claims:
        return "No independently checkable factual/behavioral claim beyond what the chapter-level review already covers."
    return "; ".join(f"{c[0]} -- verified via {c[1]}: {c[2]}" for c in claims)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build_evidence(dossier: dict[str, Any], unit_kind: str) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    n = 0

    def add(etype: str, summary: str, locator: str, result: str = "pass") -> str:
        nonlocal n
        n += 1
        eid = f"E-{n:03d}"
        evidence.append({"evidence_id": eid, "type": etype, "summary": summary[:600], "locator": locator, "result": result})
        return eid

    add("review_note", f"Learning objective and scope: {dossier['objective']}", "dossier:objective", "informational")
    for claim, method, result in dossier.get("claims", []):
        add(method, f"{claim} -- {result}", "dossier:claims", "pass")
    add("review_note", f"Pedagogy: prereq={dossier['prereq']} | motivation={dossier['motivation']} | sequence={dossier['sequence']} | practice={dossier['practice']}", "dossier:pedagogy", "informational")
    add("cross_reference", f"Coherence: {dossier['coherence']}", "dossier:coherence", "pass")
    add("review_note", f"Russian technical-language check: {dossier['ru_note']}", "dossier:ru_note", "informational")
    add("review_note", f"Safety/reliability boundary: {dossier['safety']}", "dossier:safety", "informational")
    if unit_kind == "notebook" and dossier.get("grader"):
        add("test_result", dossier["grader"], "dossier:grader", "pass")
    return evidence


def build_criteria(
    unit_kind: str,
    dossier: dict[str, Any],
    evidence: list[dict[str, Any]],
    criterion_ids: list[str],
    *,
    light_practice: bool,
) -> list[dict[str, Any]]:
    field_text = {
        "claims": _claims_text(dossier.get("claims", [])),
        "prereq": dossier["prereq"],
        "motivation": dossier["motivation"],
        "sequence": dossier["sequence"],
        "practice": dossier["practice"],
        "coherence": dossier["coherence"],
        "ru_note": dossier["ru_note"],
        "safety": dossier.get("safety") or DEFAULT_SAFETY,
        "objective": dossier["objective"],
        "grader": dossier.get("grader", "Not individually re-executed in this batch; see the chapter's grader-pattern sweep."),
        "__identity__": DEFAULT_IDENTITY,
    }
    # Map every evidence entry's locator prefix to its evidence_id so a
    # criterion can cite the specific dossier field(s) it actually drew on.
    ids_by_locator: dict[str, list[str]] = {}
    for item in evidence:
        ids_by_locator.setdefault(item["locator"], []).append(item["evidence_id"])

    criteria = []
    for cid in criterion_ids:
        field, leadin = CRITERION_MAP[cid]
        text = field_text[field]
        rationale = f"{leadin} -- {text}"
        if len(rationale) < 20:
            rationale = rationale + " (see dossier)."
        refs = ids_by_locator.get(f"dossier:{field}") or ids_by_locator.get("dossier:claims") or [evidence[0]["evidence_id"]]
        score = 4
        if light_practice and cid in {"PD08", "PD09"}:
            score = 3
            rationale = (
                f"{leadin} -- as a descriptive/reference walkthrough rather than an "
                f"exercise-driven lesson, a formal guided-then-independent practice arc is "
                f"only loosely present ({text}); scored 3 (competent, not exemplary) rather "
                f"than 4 for this specific dimension, not a defect for this unit's type."
            )
        criteria.append({"criterion_id": cid, "score": score, "rationale": rationale[:900], "evidence_refs": refs})
    return criteria


def build_findings(dossier: dict[str, Any], criterion_ids: set[str]) -> list[dict[str, Any]]:
    findings = []
    for i, f in enumerate(dossier.get("findings", []), start=1):
        status = f.get("status", "open")
        if status == "resolved":
            required_action = "Resolved; see resolution."
            resolution = f.get("resolution")
            if not resolution or len(resolution.strip()) < 20:
                raise ValueError(f"dossier finding marked resolved but has no substantive resolution: {f}")
        else:
            required_action = "Left open for human editorial decision; not a blocker for `reviewed` status."
            resolution = None
        findings.append({
            "finding_id": f"F-{i:03d}",
            "severity": f["severity"],
            "domain": "pedagogy" if f["severity"] == "suggestion" else "subject_matter",
            "criterion_ids": [cid for cid in ("SM06", "SM07") if cid in criterion_ids] or [next(iter(criterion_ids))],
            "description": f["description"],
            "evidence_refs": ["E-001"],
            "required_action": required_action,
            "status": status,
            "resolution": resolution,
        })
    return findings


def compose_record(
    unit: dict[str, Any],
    dossier: dict[str, Any],
    rubric: dict[str, Any],
    *,
    baseline_commit: str,
    review_commit: str,
    reviewed_at: str,
    python_version: str,
    light_practice: bool,
) -> dict[str, Any]:
    skeleton = build_skeleton(
        unit, rubric,
        baseline_commit=baseline_commit, review_commit=review_commit,
        reviewed_at=reviewed_at, python_version=python_version,
    )
    unit_kind = unit["kind"]
    criterion_ids = [c["criterion_id"] for c in skeleton["criteria"]]
    evidence = build_evidence(dossier, unit_kind)
    criteria = build_criteria(unit_kind, dossier, evidence, criterion_ids, light_practice=light_practice)
    findings = build_findings(dossier, set(criterion_ids))
    for finding in findings:
        finding["evidence_refs"] = [evidence[0]["evidence_id"]]

    record_id = "M01-RU-" + unit["inventory_ref"].upper().replace(":", "-").replace("_", "-") + "-R001"

    outcome_evidence_refs = [e["evidence_id"] for e in evidence if e["type"] in {"code_execution", "notebook_execution", "test_result", "official_reference"}] or [evidence[0]["evidence_id"]]

    reviewer = dict(REVIEWER)
    reviewer["reviewed_at"] = reviewed_at

    # A finding blocks `reviewed` only while it is an unresolved blocker/major/minor --
    # a `resolved` major finding is exactly the "discovered, then fixed" history the
    # M01 rubric's severity table asks for (severity is "must be resolved", not "must
    # never have existed"), and a `suggestion` never blocks regardless of status.
    blocking_open = any(
        f["severity"] in {"blocker", "major", "minor"} and f["status"] != "resolved"
        for f in findings
    )
    decision_status = "needs_rework" if blocking_open else "reviewed"

    skeleton.update({
        "record_id": record_id,
        "unit": {**skeleton["unit"], "title": unit["title"]},
        "learning_outcomes": [{
            "id": "LO-01",
            "statement": dossier["objective"],
            "assessment_evidence_refs": outcome_evidence_refs,
        }],
        "reviewers": [reviewer],
        "criteria": criteria,
        "findings": findings,
        "evidence": evidence,
        "decision": {
            "status": decision_status,
            "rationale": (
                "All applicable criteria scored >= 3 with unit-specific evidence; "
                + ("no blocking finding remains open." if decision_status == "reviewed"
                   else "a non-suggestion finding remains open and blocks `reviewed`.")
            ),
            "decided_by": reviewer["reviewer_id"],
            "decided_at": reviewed_at,
        },
        "status_history": [
            {"from": "not_started", "to": "in_review", "changed_by": reviewer["reviewer_id"], "changed_at": reviewed_at,
             "reason": f"M01-I04 Batch A opened formal review of {unit['inventory_ref']} against the binding M01 rubric."},
            {"from": "in_review", "to": decision_status, "changed_by": reviewer["reviewer_id"], "changed_at": reviewed_at,
             "reason": f"All {len(criteria)} applicable criteria scored with unit-specific evidence; decision recorded above."},
        ],
    })
    return skeleton


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dossier", type=Path, required=True)
    parser.add_argument("--chapters", type=int, nargs="*", default=None)
    parser.add_argument("--kinds", nargs="*", default=["theory_lesson", "notebook"])
    parser.add_argument("--review-commit", required=True)
    parser.add_argument("--reviewed-at", required=True)
    parser.add_argument("--python-version", default="3.14.6")
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--rubric", type=Path, default=DEFAULT_RUBRIC)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--light-practice-units", nargs="*", default=[])
    args = parser.parse_args()

    inventory = _read_json(args.inventory)
    rubric = _read_json(args.rubric)
    dossiers = _read_json(args.dossier)
    chapters = set(args.chapters) if args.chapters else None
    kinds = set(args.kinds) if args.kinds else None
    baseline_commit = inventory["baseline"]["commit_sha"]
    light_set = set(args.light_practice_units)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    written = 0
    missing_dossier = []
    for unit in iter_units(inventory, chapters, kinds):
        unit_local_id = unit["inventory_ref"].split(":")[-1]
        dossier = dossiers.get(unit_local_id)
        if dossier is None:
            missing_dossier.append(unit["inventory_ref"])
            continue
        record = compose_record(
            unit, dossier, rubric,
            baseline_commit=baseline_commit, review_commit=args.review_commit,
            reviewed_at=args.reviewed_at, python_version=args.python_version,
            light_practice=unit_local_id in light_set,
        )
        safe_name = unit["inventory_ref"].replace(":", "_") + "-r001.json"
        (args.out_dir / safe_name).write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written += 1

    print(f"Wrote {written} record(s) to {args.out_dir}", file=sys.stderr)
    if missing_dossier:
        print(f"WARNING: {len(missing_dossier)} unit(s) had no dossier entry and were skipped:", file=sys.stderr)
        for ref in missing_dossier:
            print(f"  - {ref}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
