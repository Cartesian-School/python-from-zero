"""Contract tests for the M01 Russian curriculum audit inventory."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "scripts" / "build_ru_content_audit_inventory.py"
INVENTORY_PATH = ROOT / "manifest" / "ru_content_audit_inventory.json"


def _load_generator() -> ModuleType:
    """Load the generator directly without making scripts a Python package."""

    spec = importlib.util.spec_from_file_location("ru_content_audit_inventory", GENERATOR_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _inventory() -> dict:
    """Read the committed generated inventory."""

    return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))


def _canonical_projection(value):
    """Compare stable inventory structure without rewriting the frozen baseline.

    M01-I01 records source hashes, delivery hashes, and notebook cell counts at the
    baseline commit. Later audited corrections intentionally change those current
    values; review records bind both the frozen hash and reviewed source hash.
    Regenerating Chapters 23 and 24 in CI can also change delivery bytes. The
    deterministic comparison therefore guards identities, paths, titles, delivery
    bindings, and counts while leaving baseline observations immutable.
    """

    if isinstance(value, dict):
        return {
            key: _canonical_projection(item)
            for key, item in value.items()
            if key
            not in {
                "canonical_source_sha256",
                "canonical_theory_source_sha256",
                "review_surface_sha256",
                "cells",
                "notebook_cells",
            }
        }
    if isinstance(value, list):
        return [_canonical_projection(item) for item in value]
    return value


def test_committed_inventory_structure_matches_deterministic_generator() -> None:
    """Prevent structural inventory drift without rebasing frozen observations."""

    generator = _load_generator()
    committed = _canonical_projection(_inventory())
    generated = _canonical_projection(generator.build_inventory())
    assert committed == generated


def test_inventory_covers_the_complete_frozen_baseline() -> None:
    """Lock the observed M01-I01 baseline counts until a deliberate re-baseline."""

    inventory = _inventory()
    assert inventory["baseline"] == {
        "branch": "main",
        "commit_sha": "929a69d13acc0e22a47eeb46c6a2146f33c7e732",
    }
    assert inventory["counts"]["chapters"] == 24
    assert inventory["counts"]["chapter_openers"] == 24
    assert inventory["counts"]["theory_lessons"] == 624
    assert inventory["counts"]["supplementary_units"] == 4
    assert inventory["counts"]["practice_notebooks"] == 493
    assert inventory["counts"]["standalone_projects"] == 13
    assert inventory["counts"]["total_review_units"] == 1_158


def test_every_review_unit_starts_unapproved() -> None:
    """M01-I01 inventories work; it must not claim professorial approval."""

    inventory = _inventory()
    units = list(inventory["supplementary_units"])
    for chapter in inventory["chapters"]:
        assert chapter["review_status"] == "not_started"
        units.extend(chapter["theory_units"])
        units.extend(chapter["practice_units"])
        units.extend(chapter["projects"])

    assert len(units) == inventory["counts"]["total_review_units"]
    assert {unit["review_status"] for unit in units} == {"not_started"}


def test_every_notebook_is_registered_for_delivery() -> None:
    """A canonical notebook must not silently disappear from the practice system."""

    integrity = _inventory()["integrity"]
    assert integrity["practice_manifest_entries"] == 493
    assert integrity["notebooks_missing_from_practice_manifest"] == []
    assert integrity["practice_manifest_entries_missing_notebooks"] == []
