#!/usr/bin/env python3
"""Validate Chapter 23 notebook pedagogy and behavior-based graders."""

from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import types

import nbformat

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_DIR = ROOT / "notebooks" / "chapter-23"
GRADER_DIR = ROOT / "site" / "practice" / "graders"
MANIFEST_PATH = ROOT / "manifest" / "practice_manifest.json"

HOMEWORK_IDS = {f"23-{number:02d}" for number in range(1, 7)}
SAFESORT_IDS = {f"23-{number:02d}" for number in range(7, 25)}
LOCAL_SAFESORT_IDS = {"23-09", "23-13", "23-16", "23-20", "23-21", "23-24"}
LOCAL_HOMEWORK_IDS = {"23-01", "23-04", "23-05", "23-06"}
LOCAL_IDS = LOCAL_SAFESORT_IDS | LOCAL_HOMEWORK_IDS
BROWSER_IDS = (HOMEWORK_IDS | SAFESORT_IDS) - LOCAL_IDS
HEADINGS = ("## Example", "## Starter", "## Task", "## Tests", "## Hint", "## Solution")
EXECUTION_IMPORT_PATHS = (
    ROOT / "projects" / "python" / "safesort" / "src",
    ROOT / "projects" / "tkinter" / "calculator",
    ROOT / "projects" / "console" / "story-generator",
    ROOT / "projects" / "console" / "rock-paper-scissors",
    ROOT / "projects" / "pygame" / "bouncing-balls-oop",
    ROOT / "projects" / "tkinter" / "temperature-converter",
    ROOT / "projects" / "tkinter" / "notes-app",
)


def practice_id(path: Path) -> str:
    return "-".join(path.stem.split("-")[:2])


def python_solution(notebook) -> str:
    cell = next(
        cell
        for cell in notebook.cells
        if cell.cell_type == "markdown" and cell.source.startswith("## Solution")
    )
    blocks = re.findall(r"```python\n(.*?)\n```", cell.source, flags=re.DOTALL)
    if len(blocks) != 1:
        raise ValueError(f"ожидался один Python-блок решения, найдено {len(blocks)}")
    return blocks[0]


def validate_structure(path: Path, notebook) -> list[str]:
    lesson_id = practice_id(path)
    errors = []
    heading_positions = []
    for heading in HEADINGS:
        positions = [
            index
            for index, cell in enumerate(notebook.cells)
            if cell.cell_type == "markdown" and cell.source.startswith(heading)
        ]
        if len(positions) != 1:
            errors.append(f"[{lesson_id}] heading {heading!r}: найдено {len(positions)}, ожидалось 1")
        else:
            heading_positions.append(positions[0])
    if len(heading_positions) == len(HEADINGS) and heading_positions != sorted(heading_positions):
        errors.append(f"[{lesson_id}] нарушен порядок Example -> Starter -> Task -> Tests -> Hint -> Solution")

    task_cells = [cell for cell in notebook.cells if cell.get("id") == f"task-{lesson_id}"]
    test_cells = [cell for cell in notebook.cells if cell.get("id") == f"tests-{lesson_id}"]
    if len(task_cells) != 1:
        errors.append(f"[{lesson_id}] task cell: найдено {len(task_cells)}, ожидалось 1")
    else:
        starter = task_cells[0].source
        if "TODO" not in starter:
            errors.append(f"[{lesson_id}] starter не содержит содержательный TODO")
        if "exercise" not in task_cells[0].metadata.get("tags", []):
            errors.append(f"[{lesson_id}] task cell не помечена тегом exercise")

    if len(test_cells) != 1:
        errors.append(f"[{lesson_id}] tests cell: найдено {len(test_cells)}, ожидалось 1")
    elif test_cells[0].source.count("assert ") < 2:
        errors.append(f"[{lesson_id}] tests не содержат основной и крайний случаи")

    solution_cells = [
        cell
        for cell in notebook.cells
        if cell.cell_type == "markdown" and cell.source.startswith("## Solution")
    ]
    if len(solution_cells) == 1:
        source = solution_cells[0].source
        if "<details>" not in source or "</details>" not in source:
            errors.append(f"[{lesson_id}] решение не помещено в раскрываемый details-блок")
        try:
            solution = python_solution(notebook)
        except ValueError as exc:
            errors.append(f"[{lesson_id}] {exc}")
        else:
            if task_cells and task_cells[0].source.strip() == solution.strip():
                errors.append(f"[{lesson_id}] starter совпадает с полным решением")

    for index, cell in enumerate(notebook.cells):
        if cell.cell_type == "code":
            try:
                compile(cell.source, f"{path}:cell-{index}", "exec")
            except SyntaxError as exc:
                errors.append(f"[{lesson_id}] syntax error в code cell {index}: {exc}")

    if lesson_id in LOCAL_SAFESORT_IDS:
        joined = "\n".join(cell.source for cell in notebook.cells)
        required = (
            "git clone https://github.com/Cartesian-School/safesort.git",
            "python3.14 -m venv .venv",
            'python -m pip install -e ".[dev]"',
            "python -m ipykernel install --user --name safesort-py314",
            "print(sys.executable)",
            "print(safesort.__file__)",
        )
        for text in required:
            if text not in joined:
                errors.append(f"[{lesson_id}] локальная инструкция SafeSort не содержит {text!r}")
    elif lesson_id in LOCAL_HOMEWORK_IDS:
        joined = "\n".join(cell.source for cell in notebook.cells)
        required = (
            "git clone https://github.com/Cartesian-School/python-from-zero.git",
            "python3.14 -m venv .venv",
            "python -m ipykernel install --user --name course-py314",
            "print(sys.executable)",
            "print(Path.cwd())",
        )
        for text in required:
            if text not in joined:
                errors.append(f"[{lesson_id}] локальная инструкция курса не содержит {text!r}")
    return errors


def execute_attempt(path: Path, notebook, *, use_solution: bool) -> tuple[bool, str]:
    """Run the pre-task material, one attempt, tests, and optional grader."""
    lesson_id = practice_id(path)
    module_name = f"_chapter23_check_{lesson_id.replace('-', '_')}_{int(use_solution)}"
    module = types.ModuleType(module_name)
    module.__dict__.update(
        __name__=module_name,
        __cartesian__={"cells": {f"task-{lesson_id}": {"ok": True}}},
    )
    sys.modules[module_name] = module
    namespace = module.__dict__
    task_index = next(index for index, cell in enumerate(notebook.cells) if cell.get("id") == f"task-{lesson_id}")
    tests_index = next(index for index, cell in enumerate(notebook.cells) if cell.get("id") == f"tests-{lesson_id}")
    try:
        with (
            tempfile.TemporaryDirectory(prefix=f"chapter23-{lesson_id}-") as temp_dir,
            contextlib.chdir(temp_dir),
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            for index, cell in enumerate(notebook.cells[:task_index]):
                if cell.cell_type != "code" or "raises-exception" in cell.metadata.get("tags", []):
                    continue
                exec(compile(cell.source, f"{path}:cell-{index}", "exec"), namespace)

            attempt_source = python_solution(notebook) if use_solution else notebook.cells[task_index].source
            exec(compile(attempt_source, f"{path}:attempt", "exec"), namespace)
            exec(compile(notebook.cells[tests_index].source, f"{path}:tests", "exec"), namespace)

            grader_path = GRADER_DIR / f"{lesson_id}.py"
            if use_solution and grader_path.exists():
                grader_source = grader_path.read_text(encoding="utf-8")
                exec(compile(grader_source, str(grader_path), "exec"), namespace)
                if not namespace.get("passed"):
                    raise AssertionError(f"grader failed: {namespace.get('checks')}")
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"
    finally:
        sys.modules.pop(module_name, None)
    return True, "ok"


def validate() -> list[str]:
    errors = []
    paths = sorted(NOTEBOOK_DIR.glob("*.ipynb"))
    ids = {practice_id(path) for path in paths}
    expected_ids = HOMEWORK_IDS | SAFESORT_IDS
    if len(paths) != 24 or ids != expected_ids:
        errors.append(
            f"Состав практик: notebooks={len(paths)}, missing={sorted(expected_ids - ids)}, "
            f"extra={sorted(ids - expected_ids)}"
        )

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest_ids = {lesson_id for lesson_id in manifest if lesson_id.startswith("23-")}
    if manifest_ids != expected_ids:
        errors.append(
            f"Manifest Главы 23: missing={sorted(expected_ids - manifest_ids)}, "
            f"extra={sorted(manifest_ids - expected_ids)}"
        )

    grader_ids = {path.stem for path in GRADER_DIR.glob("23-*.py")}
    if grader_ids != BROWSER_IDS:
        errors.append(
            f"Browser graders: missing={sorted(BROWSER_IDS - grader_ids)}, "
            f"extra={sorted(grader_ids - BROWSER_IDS)}"
        )

    old_cwd = Path.cwd()
    for import_path in reversed(EXECUTION_IMPORT_PATHS):
        sys.path.insert(0, str(import_path))
    os.chdir(NOTEBOOK_DIR)
    try:
        for path in paths:
            lesson_id = practice_id(path)
            notebook = nbformat.read(path, as_version=4)
            errors.extend(validate_structure(path, notebook))

            starter_passed, starter_detail = execute_attempt(path, notebook, use_solution=False)
            if starter_passed:
                errors.append(f"[{lesson_id}] untouched starter unexpectedly passes tests")

            solution_passed, solution_detail = execute_attempt(path, notebook, use_solution=True)
            if not solution_passed:
                errors.append(f"[{lesson_id}] solution/grader failed: {solution_detail}")

            grader_path = GRADER_DIR / f"{lesson_id}.py"
            if grader_path.exists():
                grader_source = grader_path.read_text(encoding="utf-8")
                if f'task-{lesson_id}' not in grader_source:
                    errors.append(f"[{lesson_id}] grader не связан со стабильным task cell ID")
                if grader_source.count("_record(") < 3:
                    errors.append(f"[{lesson_id}] grader не проверяет основной и крайний случаи")
    finally:
        os.chdir(old_cwd)
        for import_path in EXECUTION_IMPORT_PATHS:
            try:
                sys.path.remove(str(import_path))
            except ValueError:
                pass
    return errors


def main() -> None:
    errors = validate()
    if errors:
        print(f"Практики Главы 23 невалидны: {len(errors)} ошибок", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        raise SystemExit(1)
    print(
        "Практики Главы 23 валидны: 24 notebooks (18 SafeSort + 6 homework), "
        "14 browser graders, 10 local-required, 0 prefilled solutions; "
        "untouched starters fail and all published solutions pass."
    )


if __name__ == "__main__":
    main()
