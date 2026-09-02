#!/usr/bin/env python3
"""Generate structural M01 review-record skeletons from the RU content inventory.

This tool populates only facts the inventory and rubric already know: unit
identity, source paths, checksums, the applicable criterion-id list for the
unit's kind, and an empty judgment shell. It never invents scores, rationale,
findings, or evidence text — those must come from an actual review (see
``scripts/compose_ru_content_review_records.py``, which merges a human/AI
review dossier into a skeleton produced here to build the final record).

Usage:
    python scripts/scaffold_ru_content_review_records.py \
        --chapters 2 3 4 --kinds theory_lesson notebook \
        --review-commit <40-hex-sha> --reviewed-at 2026-09-02T00:00:00+00:00 \
        --python-version 3.14.6 [--out-dir DIR]

With --out-dir, one skeleton JSON is written per unit. Without it, skeletons
are printed as a single JSON array to stdout. The module also exposes
``iter_units`` and ``build_skeleton`` for direct reuse by composition tooling.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterator

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INVENTORY = REPOSITORY_ROOT / "manifest" / "ru_content_audit_inventory.json"
DEFAULT_RUBRIC = REPOSITORY_ROOT / "manifest" / "ru_content_review_rubric.json"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def applicable_criterion_ids(rubric: dict[str, Any], unit_kind: str) -> list[str]:
    """Return the ordered criterion-id list a unit kind must score."""

    return [c["id"] for c in rubric["criteria"] if unit_kind in c["applies_to"]]


def iter_units(
    inventory: dict[str, Any],
    chapters: set[int] | None = None,
    kinds: set[str] | None = None,
) -> Iterator[dict[str, Any]]:
    """Yield every inventory unit matching the requested chapters/kinds filter.

    Each yielded dict carries ``inventory_ref``, ``kind``, ``title``,
    ``canonical_source_path``, ``baseline_source_sha256``,
    ``review_surface_path``, and ``review_surface_sha256`` — the same shape
    ``validate_ru_content_review.py`` expects on ``unit``.
    """

    for unit in inventory["supplementary_units"]:
        if kinds and unit["kind"] not in kinds:
            continue
        yield {
            "inventory_ref": f"supplementary:{unit['id']}",
            "kind": unit["kind"],
            "title": unit.get("heading") or unit.get("title") or unit["id"],
            "canonical_source_path": unit["canonical_source"],
            "baseline_source_sha256": unit["canonical_source_sha256"],
            "review_surface_path": unit["review_surface"],
            "review_surface_sha256": unit["review_surface_sha256"],
        }

    for chapter in inventory["chapters"]:
        if chapters and chapter["number"] not in chapters:
            continue
        token = f"{chapter['number']:02d}"
        for unit in chapter["theory_units"]:
            if kinds and unit["kind"] not in kinds:
                continue
            yield {
                "inventory_ref": f"chapter:{token}:theory:{unit['id']}",
                "kind": unit["kind"],
                "title": unit.get("heading") or unit.get("title") or unit["id"],
                "canonical_source_path": chapter["canonical_theory_source"],
                "baseline_source_sha256": chapter["canonical_theory_source_sha256"],
                "review_surface_path": unit["review_surface"],
                "review_surface_sha256": unit["review_surface_sha256"],
            }
        for unit in chapter["practice_units"]:
            if kinds and unit["kind"] not in kinds:
                continue
            yield {
                "inventory_ref": f"chapter:{token}:practice:{unit['id']}",
                "kind": unit["kind"],
                "title": unit["title"],
                "canonical_source_path": unit["canonical_source"],
                "baseline_source_sha256": unit["canonical_source_sha256"],
                "review_surface_path": None,
                "review_surface_sha256": None,
            }
        for unit in chapter["projects"]:
            if kinds and unit["kind"] not in kinds:
                continue
            yield {
                "inventory_ref": f"chapter:{token}:project:{unit['id']}",
                "kind": unit["kind"],
                "title": unit["title"],
                "canonical_source_path": unit["source_path"],
                "baseline_source_sha256": unit["canonical_source_sha256"],
                "review_surface_path": None,
                "review_surface_sha256": None,
            }


def build_skeleton(
    unit: dict[str, Any],
    rubric: dict[str, Any],
    *,
    baseline_commit: str,
    review_commit: str,
    reviewed_at: str,
    python_version: str,
    repository_root: Path = REPOSITORY_ROOT,
) -> dict[str, Any]:
    """Build one unjudged review-record skeleton for a single inventory unit."""

    source_path = repository_root / unit["canonical_source_path"]
    reviewed_sha = _sha256(source_path)
    criterion_ids = applicable_criterion_ids(rubric, unit["kind"])

    return {
        "schema_version": "1.0.0",
        "rubric_id": rubric["rubric_id"],
        "record_id": None,  # filled by the composer once the unit id is known
        "curriculum_id": "python-from-zero",
        "language": "ru",
        "unit": {
            "inventory_ref": unit["inventory_ref"],
            "kind": unit["kind"],
            "title": unit["title"],
            "canonical_source_path": unit["canonical_source_path"],
            "baseline_source_sha256": unit["baseline_source_sha256"],
            "reviewed_source_sha256": reviewed_sha,
            "review_surface_path": unit["review_surface_path"],
            "review_surface_sha256": unit["review_surface_sha256"],
        },
        "review_context": {
            "baseline_commit": baseline_commit,
            "review_commit": review_commit,
            "started_at": reviewed_at,
            "completed_at": reviewed_at,
            "python_version": python_version,
        },
        "learning_outcomes": [],
        "reviewers": [],
        "criteria": [
            {"criterion_id": cid, "score": None, "rationale": "", "evidence_refs": []}
            for cid in criterion_ids
        ],
        "findings": [],
        "evidence": [],
        "decision": {"status": "not_started", "rationale": "", "decided_by": "", "decided_at": reviewed_at},
        "status_history": [],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapters", type=int, nargs="*", default=None)
    parser.add_argument(
        "--kinds",
        nargs="*",
        default=None,
        choices=["chapter_opener", "theory_lesson", "front_matter", "subject_index", "notebook", "standalone_project"],
    )
    parser.add_argument("--review-commit", required=True)
    parser.add_argument("--reviewed-at", required=True)
    parser.add_argument("--python-version", default="3.14.6")
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--rubric", type=Path, default=DEFAULT_RUBRIC)
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    inventory = _read_json(args.inventory)
    rubric = _read_json(args.rubric)
    chapters = set(args.chapters) if args.chapters else None
    kinds = set(args.kinds) if args.kinds else None
    baseline_commit = inventory["baseline"]["commit_sha"]

    skeletons = [
        build_skeleton(
            unit,
            rubric,
            baseline_commit=baseline_commit,
            review_commit=args.review_commit,
            reviewed_at=args.reviewed_at,
            python_version=args.python_version,
        )
        for unit in iter_units(inventory, chapters, kinds)
    ]

    if args.out_dir:
        args.out_dir.mkdir(parents=True, exist_ok=True)
        for skeleton in skeletons:
            safe_name = skeleton["unit"]["inventory_ref"].replace(":", "_") + ".skeleton.json"
            (args.out_dir / safe_name).write_text(
                json.dumps(skeleton, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        print(f"Wrote {len(skeletons)} skeleton(s) to {args.out_dir}", file=sys.stderr)
    else:
        print(json.dumps(skeletons, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
