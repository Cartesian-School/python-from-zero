#!/usr/bin/env python3
"""Валидирует manifest/practice_manifest.json перед сборкой.

Отклоняет запись, если:
- notebook не существует в notebooks/;
- return_url отсутствует или не начинается с "/";
- next_url задан, но не начинается с "/" (сам next_url может быть null —
  для последнего урока главы это ожидаемо, а не ошибка);
- backend не входит в допустимый набор;
- assessment не входит в допустимый набор;
- assessment == "automatic", но grader не указан;
- grader указан, но файл не существует в site/;
- lesson_id из ключа не совпадает с { "lesson_id": ... } внутри записи,
  если оно там присутствует.

Дубликаты lesson_id исключены самой структурой JSON-объекта (ключи
уникальны), поэтому отдельно не проверяются.

Использование: python3 scripts/validate_practice_manifest.py
Возвращает ненулевой код выхода и печатает все найденные ошибки, если
манифест невалиден — предназначен для вызова из build-конвейера.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "manifest" / "practice_manifest.json"
NOTEBOOKS_DIR = ROOT / "notebooks"
SITE_DIR = ROOT / "site"

VALID_BACKENDS = {"browser-pyodide", "browser-adapted", "local-required"}
VALID_ASSESSMENTS = {"automatic", "manual-observation", "execution-only", "local-required"}


def validate() -> list[str]:
    errors = []

    if not MANIFEST_PATH.exists():
        return [f"Манифест не найден: {MANIFEST_PATH}"]

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    for lesson_id, entry in manifest.items():
        prefix = f"[{lesson_id}]"

        if "lesson_id" in entry and entry["lesson_id"] != lesson_id:
            errors.append(f"{prefix} entry['lesson_id']={entry['lesson_id']!r} не совпадает с ключом {lesson_id!r}")

        notebook = entry.get("notebook")
        if not notebook:
            errors.append(f"{prefix} отсутствует поле 'notebook'")
        elif not (NOTEBOOKS_DIR / notebook).exists():
            errors.append(f"{prefix} notebook не найден: notebooks/{notebook}")

        return_url = entry.get("return_url")
        if not return_url:
            errors.append(f"{prefix} отсутствует 'return_url'")
        elif not return_url.startswith("/"):
            errors.append(f"{prefix} return_url должен быть абсолютным путём от корня сайта: {return_url!r}")

        next_url = entry.get("next_url")
        if next_url is not None and not next_url.startswith("/"):
            errors.append(f"{prefix} next_url должен быть абсолютным путём от корня сайта или null: {next_url!r}")

        backend = entry.get("backend")
        if backend not in VALID_BACKENDS:
            errors.append(f"{prefix} недопустимый backend: {backend!r} (ожидается один из {sorted(VALID_BACKENDS)})")

        assessment = entry.get("assessment")
        if assessment not in VALID_ASSESSMENTS:
            errors.append(f"{prefix} недопустимый assessment: {assessment!r} (ожидается один из {sorted(VALID_ASSESSMENTS)})")

        grader = entry.get("grader")
        if assessment == "automatic" and not grader:
            errors.append(f"{prefix} assessment='automatic' требует поле 'grader'")
        if grader:
            grader_path = SITE_DIR / grader.lstrip("/")
            if not grader_path.exists():
                errors.append(f"{prefix} grader не найден: {grader}")

    return errors


def main() -> None:
    errors = validate()
    if errors:
        print(f"Манифест невалиден — найдено ошибок: {len(errors)}\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    print(f"Манифест валиден: {len(manifest)} урок(ов) проверено.")


if __name__ == "__main__":
    main()
