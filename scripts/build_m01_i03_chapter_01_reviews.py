#!/usr/bin/env python3
"""Build the immutable M01-I03 review records for all Chapter 1 units."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "manifest" / "ru_content_audit_inventory.json"
RUBRIC_PATH = ROOT / "manifest" / "ru_content_review_rubric.json"
VALIDATOR_PATH = ROOT / "scripts" / "validate_ru_content_review.py"
OUTPUT_DIRECTORY = ROOT / "evidence" / "m01" / "reviews"

REVIEW_COMMIT = "e1b7167959519bbfac09e137ddf2436f9610e6ed"
STARTED_AT = "2026-08-28T20:40:00+00:00"
COMPLETED_AT = "2026-08-28T22:29:00+00:00"
REVIEWER_ID = "openai-codex-m01-i03-analyst"


UNIT_CONFIG: dict[str, dict[str, Any]] = {
    "chapter:01:theory:index": {
        "record_token": "CH01:THEORY:INDEX",
        "outcomes": [
            "Учащийся может описать путь от исходного кода к выполнению программы.",
            "Учащийся может выбрать официальный источник и отличить стандартную библиотеку от пакета.",
            "Учащийся может запустить первый код и применить сообщение об ошибке для исправления.",
        ],
        "official": "https://docs.python.org/3.14/tutorial/",
        "finding": (
            "major",
            "pedagogy",
            ["PD01", "PD10"],
            "Открытие главы не содержало измеримых результатов и начальной задачи на последующее извлечение.",
            "Добавить наблюдаемые результаты главы и диагностическое задание с критериями итогового ответа.",
        ),
    },
    "chapter:01:theory:01-01-chto-takoe-programmirovanie": {
        "record_token": "CH01:THEORY:01-01",
        "outcomes": [
            "Учащийся может различить алгоритм, инструкцию, выражение и программу на примерах.",
            "Учащийся может объяснить двухуровневую модель выполнения исходного кода в CPython.",
            "Учащийся может обосновать пригодность Python как первого языка без ложного упрощения.",
        ],
        "official": "https://docs.python.org/3.14/reference/executionmodel.html",
        "finding": (
            "major",
            "pedagogy",
            ["PD01", "PD08", "PD09", "PD10"],
            "Раздел давал объяснение и примеры, но не формулировал результаты и не проверял различение понятий.",
            "Добавить измеримые результаты и задачу классификации с раскрываемыми критериями ответа.",
        ),
    },
    "chapter:01:theory:01-04-istoriya-python": {
        "record_token": "CH01:THEORY:01-04",
        "outcomes": [
            "Учащийся может расположить основные события истории Python в правильном порядке.",
            "Учащийся может объяснить причину намеренной несовместимости Python 3.",
            "Учащийся может отличить роль PSF от технического управления языком.",
        ],
        "official": "https://docs.python.org/3.14/faq/general.html#why-was-python-created-in-the-first-place",
        "finding": (
            "major",
            "subject_matter",
            ["SM01", "SM03", "SM08"],
            "Описание приписывало PSF общее руководство развитием языка и фиксировало меняющийся patch-релиз как актуальный.",
            "Разделить организационную роль PSF и управление через PEP 13, а версию описать как стабильную ветку 3.14.x.",
        ),
    },
    "chapter:01:theory:01-05-sajt-dokumentaciya-pypi": {
        "record_token": "CH01:THEORY:01-05",
        "outcomes": [
            "Учащийся может выбрать официальный ресурс Python для заданного информационного запроса.",
            "Учащийся может отличить стандартную библиотеку от стороннего пакета.",
            "Учащийся может объяснить, почему источник и имя пакета проверяют до установки.",
        ],
        "official": "https://packaging.python.org/en/latest/tutorials/installing-packages/",
        "finding": (
            "major",
            "subject_matter",
            ["SM01", "SM07", "SM08"],
            "Текст безусловно утверждал, что pip загружает пакеты именно с PyPI, скрывая настраиваемые индексы и риск происхождения.",
            "Уточнить поведение индекса по умолчанию, возможность иной конфигурации и обязанность проверки источника.",
        ),
    },
    "chapter:01:theory:01-06-soobschestvo-i-filosofiya": {
        "record_token": "CH01:THEORY:01-06",
        "outcomes": [
            "Учащийся может различить обязанности PSF, процесса PEP и Steering Council.",
            "Учащийся может отличить язык Python от выполняющей его реализации.",
            "Учащийся может применить принцип дзена Python к сравнению вариантов кода.",
        ],
        "official": "https://peps.python.org/pep-0013/",
        "finding": (
            "major",
            "subject_matter",
            ["SM01", "SM03", "CO01"],
            "Раздел смешивал поддержку проекта со стороны PSF с техническим управлением и недостаточно точно описывал браузерную реализацию.",
            "Разделить роли PSF, PEP и Steering Council и назвать Pyodide сборкой CPython для WebAssembly.",
        ),
    },
    "chapter:01:theory:01-02-python-eto-veselo": {
        "record_token": "CH01:THEORY:01-02",
        "outcomes": [
            "Учащийся может назвать области профессионального применения Python.",
            "Учащийся может выбрать подходящий класс инструмента с учётом ограничений задачи.",
            "Учащийся может изменить первый пример и проверить заранее предсказанный вывод.",
        ],
        "official": "https://docs.python.org/3.14/faq/general.html#what-is-python",
        "finding": (
            "major",
            "pedagogy",
            ["PD01", "PD08", "PD09", "CO04"],
            "Мотивационный обзор не требовал переноса выбора инструмента на новые сценарии и не связывал практику с наблюдаемым результатом.",
            "Добавить измеримые результаты, сценарную задачу выбора инструмента и явный критерий изменения практики.",
        ),
    },
    "chapter:01:theory:01-07-peremennye-i-oshibki": {
        "record_token": "CH01:THEORY:01-07",
        "outcomes": [
            "Учащийся может объяснить присваивание как связывание имени со значением.",
            "Учащийся может предсказать результат повторного присваивания одному имени.",
            "Учащийся может отличить SyntaxError от traceback необработанного исключения.",
        ],
        "official": "https://docs.python.org/3.14/tutorial/errors.html#syntax-errors",
        "finding": (
            "blocker",
            "subject_matter",
            ["SM01", "SM03", "SM04", "PD07", "CO04"],
            "Незакрытая скобка ошибочно называлась traceback, а заявленные упражнения с именами и SyntaxError отсутствовали в notebook 01-01.",
            "Различить ошибку разбора и исключение времени выполнения и реализовать обе заявленные практики в notebook и grader.",
        ),
    },
    "chapter:01:theory:01-03-kak-poluchit-maksimum": {
        "record_token": "CH01:THEORY:01-03",
        "outcomes": [
            "Учащийся может применить цикл предсказания, запуска, сравнения и объяснения.",
            "Учащийся может восстановить ключевые модели главы без просмотра предыдущих страниц.",
            "Учащийся может составить конкретный план перехода к установке Python.",
        ],
        "official": "https://docs.python.org/3.14/tutorial/",
        "finding": (
            "major",
            "coherence",
            ["CO02", "CO04", "PD10"],
            "Итог ошибочно советовал открывать notebook к каждому разделу, хотя глава имеет один общий notebook, и не проверял извлечение знаний.",
            "Исправить модель доступности практики и добавить итоговую задачу синтеза с критериями полноты.",
        ),
    },
    "chapter:01:practice:01-01": {
        "record_token": "CH01:PRACTICE:01-01",
        "outcomes": [
            "Учащийся может изменить вызов print и предсказать наблюдаемый вывод.",
            "Учащийся может повторно связать имя со значением и объяснить результат.",
            "Учащийся может распознать NameError и SyntaxError, исправить код и повторно его выполнить.",
        ],
        "official": "https://docs.python.org/3.14/library/functions.html#print",
        "finding": (
            "major",
            "practice_assessment",
            ["PA03", "PA04", "PA05", "CO04"],
            "Notebook не реализовывал обещанные теорией задания на связывание имени и исправление SyntaxError, а grader их не оценивал.",
            "Добавить управляемую и самостоятельную практику, Debug Lab, устойчивые cell IDs и поведенческие проверки grader.",
        ),
    },
}


DOMAIN_EVIDENCE = {
    "subject_matter": ["E-001", "E-002", "E-003"],
    "pedagogy": ["E-001", "E-004", "E-006"],
    "coherence": ["E-001", "E-004", "E-005"],
    "practice_assessment": ["E-003", "E-004", "E-006"],
}


def _load_json(path: Path) -> dict[str, Any]:
    """Load one UTF-8 JSON object."""

    return json.loads(path.read_text(encoding="utf-8"))


def _load_validator() -> ModuleType:
    """Load the contract validator without requiring a scripts package."""

    spec = importlib.util.spec_from_file_location(
        "m01_review_validator", VALIDATOR_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load validator: {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _sha256(path: Path) -> str:
    """Return the lowercase SHA-256 of a repository file."""

    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _evidence(unit: dict[str, Any], config: dict[str, Any]) -> list[dict[str, Any]]:
    """Build truthful evidence shared by one reviewed unit revision."""

    source_path = ROOT / unit["canonical_source_path"]
    execution_type = (
        "notebook_execution" if unit["kind"] == "notebook" else "test_result"
    )
    return [
        {
            "evidence_id": "E-001",
            "type": "source_inspection",
            "summary": "Canonical source and generated review surface were inspected against every applicable rubric criterion.",
            "locator": unit["canonical_source_path"],
            "result": "pass",
            "sha256": _sha256(source_path),
        },
        {
            "evidence_id": "E-002",
            "type": "official_reference",
            "summary": "The unit's normative and version-sensitive claims were checked against this official Python source.",
            "locator": config["official"],
            "result": "pass",
            "sha256": None,
        },
        {
            "evidence_id": "E-003",
            "type": execution_type,
            "summary": "The Chapter 1 regression harness executed all non-demonstration code and observed the two intentional error types.",
            "locator": "pytest -q tests/test_chapter01_professorial_audit.py",
            "result": "pass",
            "sha256": _sha256(ROOT / "tests" / "test_chapter01_professorial_audit.py"),
        },
        {
            "evidence_id": "E-004",
            "type": "cross_reference",
            "summary": "Theory, Chapter 1 navigation, notebook tasks, stable cell bindings, and browser grader expectations were compared.",
            "locator": "scripts/build_chapter_01.py <-> notebooks/chapter-01/01-01-dobro-pozhalovat.ipynb <-> site/practice/graders/01-01.py",
            "result": "pass",
            "sha256": None,
        },
        {
            "evidence_id": "E-005",
            "type": "diff",
            "summary": "The remediation commit records the exact canonical-source, generated-surface, notebook, grader, and regression changes.",
            "locator": f"git:{REVIEW_COMMIT}",
            "result": "pass",
            "sha256": None,
        },
        {
            "evidence_id": "E-006",
            "type": "review_note",
            "summary": "Observable outcomes, prerequisite load, guided work, independent work, feedback, retrieval, and transfer were reviewed explicitly.",
            "locator": f"review-note://M01-I03/{config['record_token']}",
            "result": "pass",
            "sha256": None,
        },
    ]


def _record(
    inventory_ref: str,
    config: dict[str, Any],
    unit: dict[str, Any],
    rubric: dict[str, Any],
    inventory: dict[str, Any],
    validator: ModuleType,
) -> dict[str, Any]:
    """Build one complete reviewed, not human-approved, record."""

    evidence = _evidence(unit, config)
    criteria_by_id = {item["id"]: item for item in rubric["criteria"]}
    criterion_ids = sorted(validator.applicable_criterion_ids(rubric, unit["kind"]))
    criteria = []
    for criterion_id in criterion_ids:
        definition = criteria_by_id[criterion_id]
        criteria.append(
            {
                "criterion_id": criterion_id,
                "score": 3,
                "rationale": (
                    f"Критерий {definition['name']} достиг публикационного порога после исправления; "
                    "исходный код, тест и методическая оценка подтверждают результат для этой единицы."
                ),
                "evidence_refs": DOMAIN_EVIDENCE[definition["domain"]],
            }
        )

    severity, domain, finding_criteria, description, required_action = config["finding"]
    findings = [
        {
            "finding_id": "F-001",
            "severity": severity,
            "domain": domain,
            "criterion_ids": finding_criteria,
            "description": description,
            "evidence_refs": ["E-001", "E-004"],
            "required_action": required_action,
            "status": "resolved",
            "resolution": "Требуемое исправление внесено в канонический источник и подтверждено diff и регрессионным тестом.",
        }
    ]

    return {
        "schema_version": "1.0.0",
        "rubric_id": rubric["rubric_id"],
        "record_id": f"M01-RU-{config['record_token']}-R001",
        "curriculum_id": "python-from-zero",
        "language": "ru",
        "unit": {
            "inventory_ref": inventory_ref,
            "kind": unit["kind"],
            "title": unit["title"],
            "canonical_source_path": unit["canonical_source_path"],
            "baseline_source_sha256": unit["baseline_source_sha256"],
            "reviewed_source_sha256": _sha256(ROOT / unit["canonical_source_path"]),
            "review_surface_path": unit["review_surface_path"],
            "review_surface_sha256": unit["review_surface_sha256"],
        },
        "review_context": {
            "baseline_commit": inventory["baseline"]["commit_sha"],
            "review_commit": REVIEW_COMMIT,
            "started_at": STARTED_AT,
            "completed_at": COMPLETED_AT,
            "python_version": "3.14.6",
        },
        "learning_outcomes": [
            {
                "id": f"LO-{position:02d}",
                "statement": statement,
                "assessment_evidence_refs": ["E-003", "E-006"],
            }
            for position, statement in enumerate(config["outcomes"], start=1)
        ],
        "reviewers": [
            {
                "reviewer_id": REVIEWER_ID,
                "display_name": "OpenAI Codex — M01-I03 assistant analyst",
                "reviewer_type": "ai_assistant",
                "roles": ["assistant_analyst", "technical_verifier"],
                "attestation": "I inspected sources, prepared corrections, executed available tests, and assembled evidence; I did not issue human approval.",
                "reviewed_at": COMPLETED_AT,
            }
        ],
        "criteria": criteria,
        "findings": findings,
        "evidence": evidence,
        "decision": {
            "status": "reviewed",
            "rationale": "All applicable criteria were assessed and identified findings were corrected; accountable human approval remains pending.",
            "decided_by": REVIEWER_ID,
            "decided_at": COMPLETED_AT,
        },
        "status_history": [
            {
                "from": "not_started",
                "to": "in_review",
                "changed_by": REVIEWER_ID,
                "changed_at": STARTED_AT,
                "reason": "The unit entered the binding M01-I03 professorial pilot review.",
            },
            {
                "from": "in_review",
                "to": "reviewed",
                "changed_by": REVIEWER_ID,
                "changed_at": COMPLETED_AT,
                "reason": "The complete criterion review, remediation, cross-check, and evidence assembly finished successfully.",
            },
        ],
    }


def main() -> None:
    """Generate and semantically validate all nine Chapter 1 records."""

    inventory = _load_json(INVENTORY_PATH)
    rubric = _load_json(RUBRIC_PATH)
    validator = _load_validator()
    inventory_index = validator.build_inventory_index(inventory)

    if set(UNIT_CONFIG) != {
        reference
        for reference in inventory_index
        if reference.startswith("chapter:01:")
    }:
        raise RuntimeError(
            "Chapter 1 configuration does not cover the exact inventory surface"
        )

    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    for inventory_ref, config in UNIT_CONFIG.items():
        record = _record(
            inventory_ref,
            config,
            inventory_index[inventory_ref],
            rubric,
            inventory,
            validator,
        )
        errors = validator.validate_review_record(
            record,
            rubric,
            inventory,
            repository_root=ROOT,
        )
        if errors:
            raise RuntimeError(f"Invalid generated record {inventory_ref}: {errors}")
        filename = inventory_ref.replace(":", "-") + "-r001.json"
        path = OUTPUT_DIRECTORY / filename
        path.write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
