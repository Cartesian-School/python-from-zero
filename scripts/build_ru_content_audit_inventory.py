"""Build the deterministic M01 inventory for the Russian curriculum audit.

The inventory deliberately distinguishes canonical editable sources from generated
delivery artifacts.  Theory is edited in the chapter build scripts, practical
lessons are edited in notebooks, and standalone projects are edited in their
project source trees.  Generated HTML is indexed because it is the review surface,
but it is never described as the canonical source.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPOSITORY_ROOT / "manifest" / "ru_content_audit_inventory.json"
BASELINE_BRANCH = "main"
BASELINE_COMMIT = "929a69d13acc0e22a47eeb46c6a2146f33c7e732"
REVIEW_STATUS = "not_started"


class _PageMetadataParser(HTMLParser):
    """Extract the first non-empty title and H1 from a generated HTML page."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._capture: str | None = None
        self._buffer: list[str] = []
        self.title: str | None = None
        self.h1: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        if tag in {"title", "h1"} and self._capture is None:
            self._capture = tag
            self._buffer = []

    def handle_data(self, data: str) -> None:
        if self._capture is not None:
            self._buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != self._capture:
            return
        value = " ".join("".join(self._buffer).split()) or None
        if tag == "title" and self.title is None:
            self.title = value
        elif tag == "h1" and self.h1 is None:
            self.h1 = value
        self._capture = None
        self._buffer = []


def _relative(path: Path) -> str:
    """Return a stable POSIX path relative to the repository root."""

    return path.relative_to(REPOSITORY_ROOT).as_posix()


def _sha256(path: Path) -> str:
    """Calculate a content checksum without normalizing the source file."""

    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_json(path: Path) -> Any:
    """Read a UTF-8 JSON document."""

    return json.loads(path.read_text(encoding="utf-8"))


def _page_metadata(path: Path) -> dict[str, str | None]:
    """Read human-facing metadata from a generated HTML review surface."""

    parser = _PageMetadataParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return {"title": parser.title, "heading": parser.h1}


def _notebook_title(notebook: dict[str, Any], fallback: str) -> str:
    """Use the first Markdown heading as the practical lesson title."""

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        source = cell.get("source", "")
        text = "".join(source) if isinstance(source, list) else str(source)
        for line in text.splitlines():
            match = re.match(r"^\s*#{1,6}\s+(.+?)\s*$", line)
            if match:
                return match.group(1)
    return fallback


def _theory_unit(path: Path, source_path: Path, kind: str) -> dict[str, Any]:
    """Describe one generated theory page and its editable canonical source."""

    metadata = _page_metadata(path)
    return {
        "id": path.stem,
        "kind": kind,
        "review_surface": _relative(path),
        "canonical_source": _relative(source_path),
        "review_surface_sha256": _sha256(path),
        "title": metadata["title"],
        "heading": metadata["heading"],
        "review_status": REVIEW_STATUS,
    }


def _practice_unit(
    path: Path,
    practice_manifest: dict[str, Any],
) -> dict[str, Any]:
    """Describe one canonical notebook and its delivery configuration."""

    notebook = _read_json(path)
    lesson_id = path.name[:5]
    cell_counts = {"total": 0, "markdown": 0, "code": 0, "raw": 0}
    for cell in notebook.get("cells", []):
        cell_type = str(cell.get("cell_type", "raw"))
        cell_counts["total"] += 1
        if cell_type in cell_counts:
            cell_counts[cell_type] += 1
        else:
            cell_counts["raw"] += 1

    delivery = practice_manifest.get(lesson_id)
    return {
        "id": lesson_id,
        "kind": "notebook",
        "canonical_source": _relative(path),
        "canonical_source_sha256": _sha256(path),
        "title": _notebook_title(notebook, path.stem),
        "kernel": notebook.get("metadata", {}).get("kernelspec", {}),
        "cells": cell_counts,
        "delivery": delivery,
        "registered_in_practice_manifest": delivery is not None,
        "review_status": REVIEW_STATUS,
    }


def _project_unit(project: dict[str, Any]) -> dict[str, Any]:
    """Describe one standalone project referenced by the curriculum."""

    source_path = REPOSITORY_ROOT / project["source_path"]
    if not source_path.is_file():
        raise FileNotFoundError(f"Project source does not exist: {source_path}")
    return {
        **project,
        "kind": "standalone_project",
        "canonical_source_sha256": _sha256(source_path),
        "review_status": REVIEW_STATUS,
    }


def _chapter_record(
    chapter: dict[str, Any],
    practice_manifest: dict[str, Any],
    projects: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build one complete chapter record from theory, practice, and projects."""

    number = int(chapter["number"])
    chapter_token = f"{number:02d}"
    theory_source = REPOSITORY_ROOT / "scripts" / f"build_chapter_{chapter_token}.py"
    theory_directory = REPOSITORY_ROOT / "site" / "chapters" / f"glava-{chapter_token}"
    notebook_directory = REPOSITORY_ROOT / "notebooks" / f"chapter-{chapter_token}"

    if not theory_source.is_file():
        raise FileNotFoundError(f"Missing canonical theory source: {theory_source}")
    if not theory_directory.is_dir():
        raise FileNotFoundError(f"Missing generated theory directory: {theory_directory}")

    theory_paths = sorted(theory_directory.glob("*.html"))
    theory_units = [
        _theory_unit(
            path,
            theory_source,
            "chapter_opener" if path.name == "index.html" else "theory_lesson",
        )
        for path in theory_paths
    ]
    notebook_paths = (
        sorted(notebook_directory.glob("*.ipynb")) if notebook_directory.is_dir() else []
    )
    practice_units = [_practice_unit(path, practice_manifest) for path in notebook_paths]
    chapter_projects = [project for project in projects if project["chapter"] == number]

    unregistered_notebooks = [
        unit["id"] for unit in practice_units if not unit["registered_in_practice_manifest"]
    ]
    return {
        "number": number,
        "title": chapter["title"],
        "canonical_theory_source": _relative(theory_source),
        "canonical_theory_source_sha256": _sha256(theory_source),
        "theory_units": theory_units,
        "practice_units": practice_units,
        "projects": chapter_projects,
        "counts": {
            "chapter_openers": sum(unit["kind"] == "chapter_opener" for unit in theory_units),
            "theory_lessons": sum(unit["kind"] == "theory_lesson" for unit in theory_units),
            "practice_notebooks": len(practice_units),
            "standalone_projects": len(chapter_projects),
        },
        "coverage_observations": {
            "has_practice_notebooks": bool(practice_units),
            "theory_and_practice_counts_match": (
                sum(unit["kind"] == "theory_lesson" for unit in theory_units)
                == len(practice_units)
            ),
            "unregistered_notebook_ids": unregistered_notebooks,
            "requires_professorial_review": True,
        },
        "review_status": REVIEW_STATUS,
    }


def build_inventory() -> dict[str, Any]:
    """Build the complete deterministic Russian curriculum audit inventory."""

    chapters_document = _read_json(REPOSITORY_ROOT / "data" / "chapters.json")
    practice_manifest = _read_json(REPOSITORY_ROOT / "manifest" / "practice_manifest.json")
    projects_document = _read_json(REPOSITORY_ROOT / "manifest" / "projects_manifest.json")
    projects = [_project_unit(project) for project in projects_document["projects"]]

    chapter_records = [
        _chapter_record(chapter, practice_manifest, projects)
        for chapter in chapters_document["chapters"]
    ]

    supplementary_mapping = [
        (
            REPOSITORY_ROOT / "site" / "front-matter" / "ob-avtore.html",
            REPOSITORY_ROOT / "scripts" / "build_front_matter.py",
            "front_matter",
        ),
        (
            REPOSITORY_ROOT / "site" / "front-matter" / "o-tehnicheskom-recenzente.html",
            REPOSITORY_ROOT / "scripts" / "build_front_matter.py",
            "front_matter",
        ),
        (
            REPOSITORY_ROOT / "site" / "front-matter" / "vvedenie.html",
            REPOSITORY_ROOT / "scripts" / "build_front_matter.py",
            "front_matter",
        ),
        (
            REPOSITORY_ROOT / "site" / "predmetnyj-ukazatel.html",
            REPOSITORY_ROOT / "scripts" / "build_subject_index.py",
            "subject_index",
        ),
    ]
    supplementary_units = [
        _theory_unit(review_surface, source, kind)
        for review_surface, source, kind in supplementary_mapping
    ]

    all_theory_units = [
        unit for chapter in chapter_records for unit in chapter["theory_units"]
    ]
    all_practice_units = [
        unit for chapter in chapter_records for unit in chapter["practice_units"]
    ]
    registered_ids = set(practice_manifest)
    inventoried_ids = {unit["id"] for unit in all_practice_units}

    return {
        "schema_version": "1.0.0",
        "milestone": "M01 — RU CONTENT AUDIT",
        "work_item": "M01-I01 — Baseline and complete curriculum inventory",
        "language": "ru",
        "curriculum": "Python from Zero",
        "baseline": {
            "branch": BASELINE_BRANCH,
            "commit_sha": BASELINE_COMMIT,
        },
        "source_of_truth_policy": {
            "theory": "scripts/build_chapter_XX.py and supplementary page builders",
            "practice": "notebooks/chapter-XX/*.ipynb",
            "projects": "manifest/projects_manifest.json plus referenced project sources",
            "generated_review_surface": "site/**/*.html",
            "excluded_from_m01": [
                "book/pdf/*",
                "book/epub/*",
                "visual redesign",
                "Polish localization",
                "English localization",
            ],
        },
        "review_status_vocabulary": [
            "not_started",
            "in_review",
            "needs_rework",
            "reviewed",
            "approved",
        ],
        "counts": {
            "chapters": len(chapter_records),
            "chapter_openers": sum(
                unit["kind"] == "chapter_opener" for unit in all_theory_units
            ),
            "theory_lessons": sum(
                unit["kind"] == "theory_lesson" for unit in all_theory_units
            ),
            "supplementary_units": len(supplementary_units),
            "practice_notebooks": len(all_practice_units),
            "standalone_projects": len(projects),
            "total_review_units": (
                len(all_theory_units)
                + len(supplementary_units)
                + len(all_practice_units)
                + len(projects)
            ),
            "notebook_cells": sum(
                unit["cells"]["total"] for unit in all_practice_units
            ),
        },
        "integrity": {
            "practice_manifest_entries": len(practice_manifest),
            "notebooks_missing_from_practice_manifest": sorted(
                inventoried_ids - registered_ids
            ),
            "practice_manifest_entries_missing_notebooks": sorted(
                registered_ids - inventoried_ids
            ),
        },
        "supplementary_units": supplementary_units,
        "chapters": chapter_records,
    }


def write_inventory(output: Path) -> None:
    """Write the generated inventory using stable UTF-8 JSON formatting."""

    output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(build_inventory(), ensure_ascii=False, indent=2) + "\n"
    output.write_text(payload, encoding="utf-8")


def main() -> None:
    """Run the command-line inventory generator."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Destination JSON path (defaults to manifest/ru_content_audit_inventory.json)",
    )
    args = parser.parse_args()
    write_inventory(args.output.resolve())


if __name__ == "__main__":
    main()
