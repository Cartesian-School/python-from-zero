"""Validate M01 Russian curriculum review records and approval gates.

This validator uses only the Python standard library so the review contract can
run in the repository's existing CI environment.  JSON Schema documents the wire
format; this module additionally enforces cross-field, inventory-binding, status-
transition, reviewer-accountability, and approval-gate rules that JSON Schema
alone cannot express clearly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUBRIC = REPOSITORY_ROOT / "manifest" / "ru_content_review_rubric.json"
DEFAULT_INVENTORY = REPOSITORY_ROOT / "manifest" / "ru_content_audit_inventory.json"
DEFAULT_SCHEMA = (
    REPOSITORY_ROOT / "manifest" / "schemas" / "ru_content_review_record.schema.json"
)
DEFAULT_REVIEWS_DIRECTORY = REPOSITORY_ROOT / "evidence" / "m01" / "reviews"

TOP_LEVEL_KEYS = {
    "schema_version",
    "rubric_id",
    "record_id",
    "curriculum_id",
    "language",
    "unit",
    "review_context",
    "learning_outcomes",
    "reviewers",
    "criteria",
    "findings",
    "evidence",
    "decision",
    "status_history",
}
SHA256_LENGTH = 64
GIT_SHA_LENGTH = 40


def _read_json(path: Path) -> Any:
    """Read a UTF-8 JSON document."""

    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    """Calculate a SHA-256 checksum for a repository source file."""

    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _is_hex(value: Any, length: int) -> bool:
    """Return true when value is a lowercase hexadecimal identifier."""

    return (
        isinstance(value, str)
        and len(value) == length
        and all(character in "0123456789abcdef" for character in value)
    )


def _valid_timestamp(value: Any) -> bool:
    """Accept an ISO-8601 timestamp with an explicit UTC offset."""

    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _text(value: Any, minimum: int = 1) -> bool:
    """Return true when value is non-whitespace text of the required length."""

    return isinstance(value, str) and len(value.strip()) >= minimum


def build_inventory_index(inventory: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Build stable review references for every M01 inventory unit."""

    index: dict[str, dict[str, Any]] = {}
    for unit in inventory["supplementary_units"]:
        reference = f"supplementary:{unit['id']}"
        index[reference] = {
            "kind": unit["kind"],
            "title": unit.get("heading") or unit.get("title") or unit["id"],
            "canonical_source_path": unit["canonical_source"],
            "baseline_source_sha256": unit["canonical_source_sha256"],
            "review_surface_path": unit["review_surface"],
            "review_surface_sha256": unit["review_surface_sha256"],
        }

    for chapter in inventory["chapters"]:
        chapter_token = f"{chapter['number']:02d}"
        for unit in chapter["theory_units"]:
            reference = f"chapter:{chapter_token}:theory:{unit['id']}"
            index[reference] = {
                "kind": unit["kind"],
                "title": unit.get("heading") or unit.get("title") or unit["id"],
                "canonical_source_path": chapter["canonical_theory_source"],
                "baseline_source_sha256": chapter["canonical_theory_source_sha256"],
                "review_surface_path": unit["review_surface"],
                "review_surface_sha256": unit["review_surface_sha256"],
            }
        for unit in chapter["practice_units"]:
            reference = f"chapter:{chapter_token}:practice:{unit['id']}"
            index[reference] = {
                "kind": unit["kind"],
                "title": unit["title"],
                "canonical_source_path": unit["canonical_source"],
                "baseline_source_sha256": unit["canonical_source_sha256"],
                "review_surface_path": None,
                "review_surface_sha256": None,
            }
        for unit in chapter["projects"]:
            reference = f"chapter:{chapter_token}:project:{unit['id']}"
            index[reference] = {
                "kind": unit["kind"],
                "title": unit["title"],
                "canonical_source_path": unit["source_path"],
                "baseline_source_sha256": unit["canonical_source_sha256"],
                "review_surface_path": None,
                "review_surface_sha256": None,
            }
    return index


def applicable_criterion_ids(rubric: dict[str, Any], unit_kind: str) -> set[str]:
    """Return the exact criterion set required for a unit kind."""

    return {
        criterion["id"]
        for criterion in rubric["criteria"]
        if unit_kind in criterion["applies_to"]
    }


def validate_contract_documents(
    rubric: dict[str, Any], inventory: dict[str, Any], schema: dict[str, Any]
) -> list[str]:
    """Validate internal consistency of the rubric, inventory, and JSON Schema."""

    errors: list[str] = []
    if rubric.get("schema_version") != "1.0.0":
        errors.append("rubric.schema_version must be 1.0.0")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("review schema must declare JSON Schema draft 2020-12")
    if inventory.get("language") != "ru":
        errors.append("inventory.language must be ru")

    criteria = rubric.get("criteria")
    if not isinstance(criteria, list) or not criteria:
        errors.append("rubric.criteria must be a non-empty array")
        return errors

    criterion_ids = [criterion.get("id") for criterion in criteria]
    if len(criterion_ids) != len(set(criterion_ids)):
        errors.append("rubric criterion IDs must be unique")
    valid_domains = {"subject_matter", "pedagogy", "coherence", "practice_assessment"}
    valid_kinds = {
        "chapter_opener",
        "theory_lesson",
        "front_matter",
        "subject_index",
        "notebook",
        "standalone_project",
    }
    for criterion in criteria:
        criterion_id = criterion.get("id", "<missing>")
        if criterion.get("domain") not in valid_domains:
            errors.append(f"criterion {criterion_id} has an invalid domain")
        applies_to = criterion.get("applies_to")
        if not isinstance(applies_to, list) or not applies_to:
            errors.append(f"criterion {criterion_id} must apply to at least one unit kind")
        elif not set(applies_to) <= valid_kinds:
            errors.append(f"criterion {criterion_id} contains an invalid unit kind")

    transitions = rubric.get("allowed_status_transitions", {})
    statuses = {"not_started", "in_review", "needs_rework", "reviewed", "approved"}
    if set(transitions) != statuses:
        errors.append("rubric transitions must define every review status exactly once")
    for source, destinations in transitions.items():
        if not isinstance(destinations, list) or not set(destinations) <= statuses:
            errors.append(f"rubric transitions from {source} are invalid")
    if "approved" in transitions.get("not_started", []):
        errors.append("direct not_started -> approved transition is forbidden")

    inventory_index = build_inventory_index(inventory)
    expected_count = inventory["counts"]["total_review_units"]
    if len(inventory_index) != expected_count:
        errors.append(
            f"inventory index contains {len(inventory_index)} units; expected {expected_count}"
        )
    return errors


def _validate_shape(record: Any) -> list[str]:
    """Validate the core record shape before semantic checks."""

    errors: list[str] = []
    if not isinstance(record, dict):
        return ["record must be a JSON object"]
    missing = TOP_LEVEL_KEYS - set(record)
    extra = set(record) - TOP_LEVEL_KEYS
    if missing:
        errors.append(f"record is missing top-level keys: {sorted(missing)}")
    if extra:
        errors.append(f"record contains unknown top-level keys: {sorted(extra)}")
    for key in (
        "unit",
        "review_context",
        "decision",
    ):
        if key in record and not isinstance(record[key], dict):
            errors.append(f"{key} must be an object")
    for key in (
        "learning_outcomes",
        "reviewers",
        "criteria",
        "findings",
        "evidence",
        "status_history",
    ):
        if key in record and not isinstance(record[key], list):
            errors.append(f"{key} must be an array")
    return errors


def _duplicate_values(items: Iterable[Any]) -> set[Any]:
    """Return values that occur more than once."""

    seen: set[Any] = set()
    duplicates: set[Any] = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return duplicates


def validate_review_record(
    record: Any,
    rubric: dict[str, Any],
    inventory: dict[str, Any],
    *,
    repository_root: Path = REPOSITORY_ROOT,
) -> list[str]:
    """Validate one record against all binding M01 review and approval gates."""

    errors = _validate_shape(record)
    if errors or not isinstance(record, dict):
        return errors

    if record.get("schema_version") != "1.0.0":
        errors.append("schema_version must be 1.0.0")
    if record.get("rubric_id") != rubric.get("rubric_id"):
        errors.append("rubric_id does not match the binding rubric")
    if record.get("curriculum_id") != "python-from-zero":
        errors.append("curriculum_id must be python-from-zero")
    if record.get("language") != "ru":
        errors.append("language must be ru")
    if not _text(record.get("record_id")):
        errors.append("record_id must be non-empty text")

    unit = record["unit"]
    context = record["review_context"]
    decision = record["decision"]
    if not isinstance(unit, dict) or not isinstance(context, dict) or not isinstance(decision, dict):
        return errors

    inventory_index = build_inventory_index(inventory)
    inventory_ref = unit.get("inventory_ref")
    expected_unit = inventory_index.get(inventory_ref)
    if expected_unit is None:
        errors.append(f"unknown unit.inventory_ref: {inventory_ref!r}")
    else:
        for key in (
            "kind",
            "canonical_source_path",
            "baseline_source_sha256",
            "review_surface_path",
            "review_surface_sha256",
        ):
            if unit.get(key) != expected_unit.get(key):
                errors.append(f"unit.{key} does not match the frozen M01 inventory")

        source_path = repository_root / expected_unit["canonical_source_path"]
        if not source_path.is_file():
            errors.append(f"canonical source does not exist: {source_path}")
        elif unit.get("reviewed_source_sha256") != _sha256(source_path):
            errors.append("unit.reviewed_source_sha256 does not match the current source file")

    if not _is_hex(unit.get("baseline_source_sha256"), SHA256_LENGTH):
        errors.append("unit.baseline_source_sha256 must be a lowercase SHA-256")
    if not _is_hex(unit.get("reviewed_source_sha256"), SHA256_LENGTH):
        errors.append("unit.reviewed_source_sha256 must be a lowercase SHA-256")
    if not _text(unit.get("title")):
        errors.append("unit.title must be non-empty text")

    if context.get("baseline_commit") != inventory.get("baseline", {}).get("commit_sha"):
        errors.append("review_context.baseline_commit must match the frozen inventory baseline")
    if not _is_hex(context.get("review_commit"), GIT_SHA_LENGTH):
        errors.append("review_context.review_commit must be a lowercase 40-character Git SHA")
    if not str(context.get("python_version", "")).startswith("3.14"):
        errors.append("review_context.python_version must identify Python 3.14")
    for field in ("started_at", "completed_at"):
        if not _valid_timestamp(context.get(field)):
            errors.append(f"review_context.{field} must be an ISO-8601 timestamp with timezone")
    if _valid_timestamp(context.get("started_at")) and _valid_timestamp(
        context.get("completed_at")
    ):
        started = datetime.fromisoformat(context["started_at"].replace("Z", "+00:00"))
        completed = datetime.fromisoformat(context["completed_at"].replace("Z", "+00:00"))
        if completed < started:
            errors.append("review_context.completed_at cannot precede started_at")

    unit_kind = unit.get("kind")
    outcomes = record["learning_outcomes"]
    evidence = record["evidence"]
    reviewers = record["reviewers"]
    criteria = record["criteria"]
    findings = record["findings"]
    history = record["status_history"]
    if not all(isinstance(value, list) for value in (outcomes, evidence, reviewers, criteria, findings, history)):
        return errors

    evidence_ids = [item.get("evidence_id") for item in evidence if isinstance(item, dict)]
    duplicate_evidence = _duplicate_values(evidence_ids)
    if duplicate_evidence:
        errors.append(f"duplicate evidence IDs: {sorted(duplicate_evidence)}")
    evidence_index = {
        item.get("evidence_id"): item for item in evidence if isinstance(item, dict)
    }
    for item in evidence:
        if not isinstance(item, dict):
            errors.append("every evidence entry must be an object")
            continue
        if not _text(item.get("summary"), 20):
            errors.append(f"evidence {item.get('evidence_id')} needs a substantive summary")
        if not _text(item.get("locator")):
            errors.append(f"evidence {item.get('evidence_id')} needs a locator")
        if item.get("result") not in {"pass", "fail", "informational"}:
            errors.append(f"evidence {item.get('evidence_id')} has an invalid result")

    required_outcomes = unit_kind in rubric["learning_outcome_unit_kinds"]
    if required_outcomes and not outcomes:
        errors.append(f"{unit_kind} requires at least one measurable learning outcome")
    outcome_ids = [item.get("id") for item in outcomes if isinstance(item, dict)]
    if _duplicate_values(outcome_ids):
        errors.append("learning outcome IDs must be unique")
    for outcome in outcomes:
        if not isinstance(outcome, dict):
            errors.append("every learning outcome must be an object")
            continue
        if not _text(outcome.get("statement"), 20):
            errors.append(f"learning outcome {outcome.get('id')} is not measurable/substantive")
        refs = outcome.get("assessment_evidence_refs")
        if not isinstance(refs, list) or not refs:
            errors.append(f"learning outcome {outcome.get('id')} lacks assessment evidence")
        elif not set(refs) <= set(evidence_index):
            errors.append(f"learning outcome {outcome.get('id')} references unknown evidence")

    expected_criteria = applicable_criterion_ids(rubric, str(unit_kind))
    criterion_ids = [item.get("criterion_id") for item in criteria if isinstance(item, dict)]
    duplicate_criteria = _duplicate_values(criterion_ids)
    if duplicate_criteria:
        errors.append(f"duplicate criterion assessments: {sorted(duplicate_criteria)}")
    if set(criterion_ids) != expected_criteria:
        missing = sorted(expected_criteria - set(criterion_ids))
        extra = sorted(set(criterion_ids) - expected_criteria)
        errors.append(f"criterion coverage mismatch; missing={missing}, extra={extra}")
    for assessment in criteria:
        if not isinstance(assessment, dict):
            errors.append("every criterion assessment must be an object")
            continue
        criterion_id = assessment.get("criterion_id")
        score = assessment.get("score")
        if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 4:
            errors.append(f"criterion {criterion_id} score must be an integer from 0 to 4")
        if not _text(assessment.get("rationale"), 20):
            errors.append(f"criterion {criterion_id} needs a substantive rationale")
        refs = assessment.get("evidence_refs")
        if not isinstance(refs, list) or not refs:
            errors.append(f"criterion {criterion_id} must reference evidence")
        elif not set(refs) <= set(evidence_index):
            errors.append(f"criterion {criterion_id} references unknown evidence")

    finding_ids = [item.get("finding_id") for item in findings if isinstance(item, dict)]
    if _duplicate_values(finding_ids):
        errors.append("finding IDs must be unique")
    for finding in findings:
        if not isinstance(finding, dict):
            errors.append("every finding must be an object")
            continue
        finding_id = finding.get("finding_id")
        if finding.get("severity") not in {"blocker", "major", "minor", "suggestion"}:
            errors.append(f"finding {finding_id} has an invalid severity")
        if finding.get("status") not in {"open", "resolved", "accepted_risk"}:
            errors.append(f"finding {finding_id} has an invalid status")
        if finding.get("status") == "resolved" and not _text(finding.get("resolution"), 20):
            errors.append(f"resolved finding {finding_id} needs a substantive resolution")
        finding_criteria = finding.get("criterion_ids")
        if not isinstance(finding_criteria, list) or not set(finding_criteria) <= expected_criteria:
            errors.append(f"finding {finding_id} references invalid criteria")
        refs = finding.get("evidence_refs")
        if not isinstance(refs, list) or not refs or not set(refs) <= set(evidence_index):
            errors.append(f"finding {finding_id} references invalid evidence")

    reviewer_ids = [item.get("reviewer_id") for item in reviewers if isinstance(item, dict)]
    if _duplicate_values(reviewer_ids):
        errors.append("reviewer IDs must be unique")
    reviewer_index = {
        item.get("reviewer_id"): item for item in reviewers if isinstance(item, dict)
    }
    for reviewer in reviewers:
        if not isinstance(reviewer, dict):
            errors.append("every reviewer must be an object")
            continue
        if reviewer.get("reviewer_type") not in {"human", "ai_assistant"}:
            errors.append(f"reviewer {reviewer.get('reviewer_id')} has an invalid type")
        if not _text(reviewer.get("attestation"), 20):
            errors.append(f"reviewer {reviewer.get('reviewer_id')} needs an attestation")
        if not _valid_timestamp(reviewer.get("reviewed_at")):
            errors.append(f"reviewer {reviewer.get('reviewer_id')} needs a valid reviewed_at")

    transitions = rubric["allowed_status_transitions"]
    previous_to: str | None = None
    for position, transition in enumerate(history):
        if not isinstance(transition, dict):
            errors.append("every status transition must be an object")
            continue
        source = transition.get("from")
        destination = transition.get("to")
        if destination not in transitions.get(source, []):
            errors.append(f"forbidden status transition: {source} -> {destination}")
        if position == 0 and source != "not_started":
            errors.append("status history must begin at not_started")
        if previous_to is not None and source != previous_to:
            errors.append("status history must form one continuous chain")
        previous_to = destination
        if not _valid_timestamp(transition.get("changed_at")):
            errors.append("every status transition needs a valid changed_at")
        if not _text(transition.get("reason"), 20):
            errors.append("every status transition needs a substantive reason")

    decision_status = decision.get("status")
    if history:
        if previous_to != decision_status:
            errors.append("final status history state must equal decision.status")
    elif decision_status != "not_started":
        errors.append("a non-initial decision requires status history")
    if decision.get("decided_by") not in reviewer_index:
        errors.append("decision.decided_by must identify a declared reviewer")
    if not _valid_timestamp(decision.get("decided_at")):
        errors.append("decision.decided_at must be a valid timestamp")
    if not _text(decision.get("rationale"), 20):
        errors.append("decision.rationale must be substantive")

    if decision_status == "approved":
        minimum = rubric["approval_minimum_score"]
        low_scores = [
            item.get("criterion_id")
            for item in criteria
            if isinstance(item, dict)
            and (not isinstance(item.get("score"), int) or item.get("score", -1) < minimum)
        ]
        if low_scores:
            errors.append(f"approved record has criteria below {minimum}: {sorted(low_scores)}")

        blocking = set(rubric["blocking_finding_severities"])
        unresolved = [
            item.get("finding_id")
            for item in findings
            if isinstance(item, dict)
            and item.get("severity") in blocking
            and item.get("status") != "resolved"
        ]
        if unresolved:
            errors.append(f"approved record has unresolved blocking findings: {sorted(unresolved)}")

        human_roles: set[str] = set()
        for reviewer in reviewers:
            if isinstance(reviewer, dict) and reviewer.get("reviewer_type") == "human":
                human_roles.update(reviewer.get("roles", []))
        missing_roles = set(rubric["required_human_roles_for_approval"]) - human_roles
        if missing_roles:
            errors.append(f"approved record lacks accountable human roles: {sorted(missing_roles)}")
        decider = reviewer_index.get(decision.get("decided_by"), {})
        if (
            decider.get("reviewer_type") != "human"
            or "final_approver" not in decider.get("roles", [])
        ):
            errors.append("approved decision must be made by a human final_approver")

        if unit_kind in rubric["official_reference_unit_kinds"]:
            if not any(
                item.get("type") == "official_reference" for item in evidence if isinstance(item, dict)
            ):
                errors.append("approved pedagogical unit requires official-reference evidence")
        if unit_kind in rubric["execution_evidence_unit_kinds"]:
            executable_types = {"code_execution", "notebook_execution", "test_result"}
            if not any(
                item.get("type") in executable_types and item.get("result") == "pass"
                for item in evidence
                if isinstance(item, dict)
            ):
                errors.append("approved executable unit requires passing execution evidence")

    return errors


def discover_review_records(directory: Path) -> list[Path]:
    """Return review record files in deterministic order."""

    return sorted(directory.glob("*.json")) if directory.is_dir() else []


def main() -> None:
    """Validate contract documents and zero or more review records."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", nargs="*", type=Path, help="Review record JSON files")
    parser.add_argument("--rubric", type=Path, default=DEFAULT_RUBRIC)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--reviews-directory", type=Path, default=DEFAULT_REVIEWS_DIRECTORY)
    parser.add_argument(
        "--require-records",
        action="store_true",
        help="Fail when no review records are supplied or discovered",
    )
    args = parser.parse_args()

    rubric = _read_json(args.rubric)
    inventory = _read_json(args.inventory)
    schema = _read_json(args.schema)
    errors = validate_contract_documents(rubric, inventory, schema)

    record_paths = args.records or discover_review_records(args.reviews_directory)
    if args.require_records and not record_paths:
        errors.append("no review records were supplied or discovered")
    for path in record_paths:
        record = _read_json(path)
        for error in validate_review_record(record, rubric, inventory):
            errors.append(f"{path}: {error}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)

    print(
        f"PASS: review contract valid; records={len(record_paths)}; "
        f"inventory_units={inventory['counts']['total_review_units']}"
    )


if __name__ == "__main__":
    main()
