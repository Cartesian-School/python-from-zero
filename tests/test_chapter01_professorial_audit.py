"""Regression tests for the M01-I03 Chapter 1 professorial audit."""

from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "notebooks" / "chapter-01" / "01-01-dobro-pozhalovat.ipynb"
GRADER_PATH = ROOT / "site" / "practice" / "graders" / "01-01.py"
CHAPTER_DIR = ROOT / "site" / "chapters" / "glava-01"
REVIEW_DIRECTORY = ROOT / "evidence" / "m01" / "reviews"

THEORY_PAGES = (
    "01-01-chto-takoe-programmirovanie.html",
    "01-02-python-eto-veselo.html",
    "01-03-kak-poluchit-maksimum.html",
    "01-04-istoriya-python.html",
    "01-05-sajt-dokumentaciya-pypi.html",
    "01-06-soobschestvo-i-filosofiya.html",
    "01-07-peremennye-i-oshibki.html",
)

GRADED_CELL_IDS = {
    "3ca309a1",
    "e1a23aa4",
    "ea50acd2",
    "chapter01-variable-task",
    "chapter01-syntax-fix",
}

EXPECTED_REVIEW_REFS = {
    "chapter:01:theory:index",
    "chapter:01:theory:01-01-chto-takoe-programmirovanie",
    "chapter:01:theory:01-02-python-eto-veselo",
    "chapter:01:theory:01-03-kak-poluchit-maksimum",
    "chapter:01:theory:01-04-istoriya-python",
    "chapter:01:theory:01-05-sajt-dokumentaciya-pypi",
    "chapter:01:theory:01-06-soobschestvo-i-filosofiya",
    "chapter:01:theory:01-07-peremennye-i-oshibki",
    "chapter:01:practice:01-01",
}


def _load_notebook() -> dict:
    """Load the canonical notebook without requiring the nbformat package."""

    return json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))


def _execute_cells(notebook: dict) -> tuple[dict[str, dict], list[type[BaseException]]]:
    """Execute code cells in one namespace and preserve browser-grader observations."""

    namespace: dict = {}
    observations: dict[str, dict] = {}
    expected_errors: list[type[BaseException]] = []

    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        source = "".join(cell["source"])
        output = io.StringIO()
        tags = set(cell.get("metadata", {}).get("tags", []))
        try:
            with contextlib.redirect_stdout(output):
                exec(compile(source, f"cell:{cell['id']}", "exec"), namespace)  # noqa: S102
        except (
            BaseException
        ) as error:  # The lesson intentionally demonstrates two failures.
            if "raises-exception" not in tags:
                raise
            expected_errors.append(type(error))
            observations[cell["id"]] = {
                "ok": False,
                "stdout": output.getvalue(),
                "error": type(error).__name__,
            }
        else:
            observations[cell["id"]] = {"ok": True, "stdout": output.getvalue()}

    return observations, expected_errors


def test_every_chapter01_page_exposes_outcomes_and_retrieval_practice() -> None:
    """Every audited theory unit must state outcomes and require active retrieval."""

    opener = (CHAPTER_DIR / "index.html").read_text(encoding="utf-8")
    assert "После этого раздела вы сможете" in opener
    assert "Проверьте себя" in opener

    for filename in THEORY_PAGES:
        page = (CHAPTER_DIR / filename).read_text(encoding="utf-8")
        assert "После этого раздела вы сможете" in page, filename
        assert "Проверьте себя" in page, filename
        assert "Показать ответ и критерии" in page, filename


def test_syntax_error_is_not_mislabelled_as_a_runtime_traceback() -> None:
    """The reviewed page must distinguish parse failure from runtime traceback."""

    page = (CHAPTER_DIR / "01-07-peremennye-i-oshibki.html").read_text(encoding="utf-8")
    assert "синтаксическая ошибка до начала выполнения" in page
    assert "обычной строки" in page
    assert "Traceback (most recent call last)" in page


def test_notebook_executes_all_non_demo_cells_and_passes_behavior_grader() -> None:
    """Canonical solutions must execute and satisfy the expanded behavior grader."""

    notebook = _load_notebook()
    observations, expected_errors = _execute_cells(notebook)
    assert expected_errors == [NameError, SyntaxError]
    assert GRADED_CELL_IDS <= set(observations)

    grader_namespace = {"__cartesian__": {"cells": observations}}
    grader_source = GRADER_PATH.read_text(encoding="utf-8")
    exec(compile(grader_source, str(GRADER_PATH), "exec"), grader_namespace)  # noqa: S102

    assert grader_namespace["passed"] is True
    assert grader_namespace["score"] == 100
    assert len(grader_namespace["checks"]) == 10


def test_notebook_declares_measurable_outcomes_and_stable_graded_cells() -> None:
    """Assessment bindings must survive notebook regeneration and remain learner-visible."""

    notebook = _load_notebook()
    ids = [cell["id"] for cell in notebook["cells"]]
    assert len(ids) == len(set(ids))
    assert GRADED_CELL_IDS <= set(ids)

    markdown = "\n".join(
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "markdown"
    )
    assert "После практики вы сможете" in markdown
    assert "Самостоятельное задание: повторное присваивание" in markdown
    assert "Debug Lab: синтаксическая ошибка" in markdown
    assert "Итог без подсказки" in markdown


def test_pilot_evidence_covers_every_unit_without_fabricated_human_approval() -> None:
    """The pilot must stop at reviewed until an accountable human attests."""

    records = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in REVIEW_DIRECTORY.glob("*.json")
    ]
    assert {
        record["unit"]["inventory_ref"] for record in records
    } == EXPECTED_REVIEW_REFS

    for record in records:
        assert record["decision"]["status"] == "reviewed"
        assert record["status_history"][-1]["to"] == "reviewed"
        assert {reviewer["reviewer_type"] for reviewer in record["reviewers"]} == {
            "ai_assistant"
        }
        assert all(assessment["score"] >= 3 for assessment in record["criteria"])
        assert all(finding["status"] == "resolved" for finding in record["findings"])
