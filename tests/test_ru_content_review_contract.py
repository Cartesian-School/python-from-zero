"""Tests for the binding M01 professorial review contract."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_ru_content_review.py"
RUBRIC_PATH = ROOT / "manifest" / "ru_content_review_rubric.json"
INVENTORY_PATH = ROOT / "manifest" / "ru_content_audit_inventory.json"
SCHEMA_PATH = ROOT / "manifest" / "schemas" / "ru_content_review_record.schema.json"


def _load_validator() -> ModuleType:
    """Load the validator without requiring scripts to be a Python package."""

    spec = importlib.util.spec_from_file_location("validate_ru_content_review", VALIDATOR_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _documents() -> tuple[dict, dict, dict]:
    """Load the three binding machine-readable contract documents."""

    return tuple(
        json.loads(path.read_text(encoding="utf-8"))
        for path in (RUBRIC_PATH, INVENTORY_PATH, SCHEMA_PATH)
    )


def _approved_record() -> dict:
    """Build a complete valid approval record for one canonical notebook."""

    validator = _load_validator()
    rubric, inventory, _schema = _documents()
    unit = validator.build_inventory_index(inventory)["chapter:03:practice:03-01"]
    evidence = [
        {
            "evidence_id": "E-001",
            "type": "official_reference",
            "summary": "Python 3.14 language documentation supports the reviewed syntax and semantics.",
            "locator": "https://docs.python.org/3.14/",
            "result": "pass",
            "sha256": None,
        },
        {
            "evidence_id": "E-002",
            "type": "notebook_execution",
            "summary": "The complete canonical notebook executed from top to bottom without an unexpected failure.",
            "locator": "notebooks/chapter-03/03-01-first-program.ipynb",
            "result": "pass",
            "sha256": unit["baseline_source_sha256"],
        },
        {
            "evidence_id": "E-003",
            "type": "test_result",
            "summary": "The independent learner task produced the declared result under the Python 3.14 environment.",
            "locator": "python scripts/run_notebook.py notebooks/chapter-03/03-01-first-program.ipynb",
            "result": "pass",
            "sha256": None,
        },
        {
            "evidence_id": "E-004",
            "type": "review_note",
            "summary": "The lesson sequence, cognitive load, terminology, and prerequisite boundary were reviewed in context.",
            "locator": "review-note://M01-RU-CH03-PRACTICE-03-01-R001",
            "result": "informational",
            "sha256": None,
        },
    ]
    criteria = [
        {
            "criterion_id": criterion_id,
            "score": 3,
            "rationale": f"Criterion {criterion_id} meets the publication-quality threshold with linked evidence.",
            "evidence_refs": ["E-001", "E-002", "E-004"],
        }
        for criterion_id in sorted(validator.applicable_criterion_ids(rubric, "notebook"))
    ]
    return {
        "schema_version": "1.0.0",
        "rubric_id": rubric["rubric_id"],
        "record_id": "M01-RU-CH03:PRACTICE:03-01-R001",
        "curriculum_id": "python-from-zero",
        "language": "ru",
        "unit": {
            "inventory_ref": "chapter:03:practice:03-01",
            "kind": unit["kind"],
            "title": unit["title"],
            "canonical_source_path": unit["canonical_source_path"],
            "baseline_source_sha256": unit["baseline_source_sha256"],
            "reviewed_source_sha256": unit["baseline_source_sha256"],
            "review_surface_path": unit["review_surface_path"],
            "review_surface_sha256": unit["review_surface_sha256"],
        },
        "review_context": {
            "baseline_commit": inventory["baseline"]["commit_sha"],
            "review_commit": "a" * 40,
            "started_at": "2026-08-28T10:00:00+00:00",
            "completed_at": "2026-08-28T12:00:00+00:00",
            "python_version": "3.14.2",
        },
        "learning_outcomes": [
            {
                "id": "LO-01",
                "statement": "The learner can run a minimal Python program and explain the observed output.",
                "assessment_evidence_refs": ["E-003"],
            }
        ],
        "reviewers": [
            {
                "reviewer_id": "human-reviewer-1",
                "display_name": "Accountable human reviewer",
                "reviewer_type": "human",
                "roles": [
                    "subject_matter_reviewer",
                    "methodology_reviewer",
                    "technical_verifier",
                    "final_approver",
                ],
                "attestation": "I reviewed the source, evidence, learning design, and final approval gates.",
                "reviewed_at": "2026-08-28T12:00:00+00:00",
            },
            {
                "reviewer_id": "assistant-analyst-1",
                "display_name": "Assistant analyst",
                "reviewer_type": "ai_assistant",
                "roles": ["assistant_analyst"],
                "attestation": "I assisted with source inspection and evidence preparation but did not approve the unit.",
                "reviewed_at": "2026-08-28T11:30:00+00:00",
            },
        ],
        "criteria": criteria,
        "findings": [],
        "evidence": evidence,
        "decision": {
            "status": "approved",
            "rationale": "All applicable criteria, evidence, execution, and accountable human gates passed.",
            "decided_by": "human-reviewer-1",
            "decided_at": "2026-08-28T12:00:00+00:00",
        },
        "status_history": [
            {
                "from": "not_started",
                "to": "in_review",
                "changed_by": "human-reviewer-1",
                "changed_at": "2026-08-28T10:00:00+00:00",
                "reason": "The unit entered the binding professorial content review process.",
            },
            {
                "from": "in_review",
                "to": "reviewed",
                "changed_by": "human-reviewer-1",
                "changed_at": "2026-08-28T11:50:00+00:00",
                "reason": "All criterion assessments and required evidence were completed.",
            },
            {
                "from": "reviewed",
                "to": "approved",
                "changed_by": "human-reviewer-1",
                "changed_at": "2026-08-28T12:00:00+00:00",
                "reason": "The explicit approval gate passed without an unresolved binding finding.",
            },
        ],
    }


def _errors(record: dict) -> list[str]:
    """Validate a record with repository contract documents."""

    validator = _load_validator()
    rubric, inventory, _schema = _documents()
    return validator.validate_review_record(record, rubric, inventory, repository_root=ROOT)


def test_contract_documents_cover_all_frozen_inventory_units() -> None:
    """The rubric and schema must bind cleanly to every M01-I01 unit."""

    validator = _load_validator()
    rubric, inventory, schema = _documents()
    assert validator.validate_contract_documents(rubric, inventory, schema) == []
    assert len(validator.build_inventory_index(inventory)) == 1_158


def test_complete_human_approved_record_passes() -> None:
    """A fully evidenced, accountable approval must pass."""

    assert _errors(_approved_record()) == []


def test_ai_only_approval_is_rejected() -> None:
    """AI assistance cannot replace accountable human approval."""

    record = _approved_record()
    record["reviewers"][0]["reviewer_type"] = "ai_assistant"
    errors = _errors(record)
    assert any("accountable human roles" in error for error in errors)
    assert any("human final_approver" in error for error in errors)


def test_approval_with_one_low_criterion_is_rejected() -> None:
    """Averages cannot hide one criterion below publication quality."""

    record = _approved_record()
    record["criteria"][0]["score"] = 2
    assert any("criteria below 3" in error for error in _errors(record))


def test_approval_with_unresolved_major_finding_is_rejected() -> None:
    """A major finding must be resolved, not accepted or ignored."""

    record = _approved_record()
    record["findings"] = [
        {
            "finding_id": "F-001",
            "severity": "major",
            "domain": "subject_matter",
            "criterion_ids": ["SM01"],
            "description": "The explanatory claim would create a materially incorrect beginner mental model.",
            "evidence_refs": ["E-001"],
            "required_action": "Correct the canonical explanation and repeat the subject-matter review.",
            "status": "accepted_risk",
            "resolution": "The risk was documented but the source was not corrected.",
        }
    ]
    assert any("unresolved blocking findings" in error for error in _errors(record))


def test_missing_applicable_criterion_is_rejected() -> None:
    """Reviewers cannot silently omit a difficult criterion."""

    record = _approved_record()
    record["criteria"].pop()
    assert any("criterion coverage mismatch" in error for error in _errors(record))


def test_direct_not_started_to_approved_transition_is_rejected() -> None:
    """Approval must follow review and explicit gate stages."""

    record = _approved_record()
    record["status_history"] = [
        {
            "from": "not_started",
            "to": "approved",
            "changed_by": "human-reviewer-1",
            "changed_at": "2026-08-28T12:00:00+00:00",
            "reason": "This intentionally invalid transition attempts to bypass required review stages.",
        }
    ]
    assert any("forbidden status transition" in error for error in _errors(record))


def test_reviewed_source_checksum_drift_is_rejected() -> None:
    """A decision cannot claim review of source bytes that were not inspected."""

    record = _approved_record()
    record["unit"]["reviewed_source_sha256"] = "0" * 64
    assert any("current source file" in error for error in _errors(record))


def test_needs_rework_record_with_open_finding_passes() -> None:
    """The contract must truthfully represent unfinished review work."""

    record = _approved_record()
    record["criteria"][0]["score"] = 1
    record["findings"] = [
        {
            "finding_id": "F-001",
            "severity": "major",
            "domain": "subject_matter",
            "criterion_ids": [record["criteria"][0]["criterion_id"]],
            "description": "The current explanation is materially incomplete for the declared learning outcome.",
            "evidence_refs": ["E-004"],
            "required_action": "Rewrite the explanation and provide new execution and pedagogical evidence.",
            "status": "open",
            "resolution": None,
        }
    ]
    record["decision"] = {
        "status": "needs_rework",
        "rationale": "A major binding finding remains open and requires canonical-source correction.",
        "decided_by": "human-reviewer-1",
        "decided_at": "2026-08-28T12:00:00+00:00",
    }
    record["status_history"] = [
        {
            "from": "not_started",
            "to": "in_review",
            "changed_by": "human-reviewer-1",
            "changed_at": "2026-08-28T10:00:00+00:00",
            "reason": "The unit entered the binding professorial content review process.",
        },
        {
            "from": "in_review",
            "to": "needs_rework",
            "changed_by": "human-reviewer-1",
            "changed_at": "2026-08-28T12:00:00+00:00",
            "reason": "The review identified a major unresolved subject-matter deficiency.",
        },
    ]
    assert _errors(record) == []
