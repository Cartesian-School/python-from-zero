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

Также проверяет ГЛОБАЛЬНУЮ полноту учебного плана (Chapters 1-24):
- дубликаты lesson_id на верхнем уровне манифеста (JSON тихо схлопывает
  повторяющиеся ключи при обычном json.loads — здесь это ловится явно,
  через object_pairs_hook, а не полагается на структуру dict);
- дубликаты notebook — один и тот же .ipynb, сопоставленный двум разным
  lesson_id;
- каждый канонический ноутбук (notebooks/chapter-*/*.ipynb, за
  исключением одноразовых _test-*.ipynb) обязан быть РОВНО в одном из
  двух состояний: (A) сопоставлен записи в манифесте, или (B) явно
  задокументирован как исключение в manifest/practice_exclusions.json.
  Третье состояние — отсутствие в обоих файлах — необъяснённый пробел
  и провал валидации. Пересечение (ноутбук в обоих файлах сразу) —
  тоже провал, как противоречивая классификация;
- osiротевшие директории site/practice/<id>/ без соответствующей записи
  в манифесте.

Использование: python3 scripts/validate_practice_manifest.py
Возвращает ненулевой код выхода и печатает все найденные ошибки, если
манифест невалиден — предназначен для вызова из build-конвейера.
"""

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "manifest" / "practice_manifest.json"
EXCLUSIONS_PATH = ROOT / "manifest" / "practice_exclusions.json"
NOTEBOOKS_DIR = ROOT / "notebooks"
SITE_DIR = ROOT / "site"
PRACTICE_DIR = SITE_DIR / "practice"

VALID_BACKENDS = {"browser-pyodide", "browser-adapted", "local-required"}
VALID_ASSESSMENTS = {"automatic", "manual-observation", "execution-only", "local-required"}


def _load_top_level_pairs(path: Path) -> list[tuple[str, object]]:
    """Returns the raw (key, value) pairs of the OUTERMOST JSON object in
    `path`, including any duplicate keys that plain json.loads() would
    silently collapse into a dict (keeping only the last occurrence).
    json parses depth-first, so the outermost object's pairs are captured
    by the LAST call to object_pairs_hook.
    """
    captured: list[list[tuple[str, object]]] = []

    def hook(pairs: list[tuple[str, object]]) -> dict:
        captured.append(pairs)
        return dict(pairs)

    json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=hook)
    return captured[-1] if captured else []


def _canonical_notebooks() -> set[str]:
    """All real (non-throwaway) notebooks, as paths relative to notebooks/."""
    notebooks = set()
    for path in NOTEBOOKS_DIR.glob("chapter-*/*.ipynb"):
        if "_test-" in path.name:
            continue
        notebooks.add(f"{path.parent.name}/{path.name}")
    return notebooks


def validate_global_completeness(manifest: dict) -> list[str]:
    errors = []

    if not EXCLUSIONS_PATH.exists():
        return [f"Файл исключений не найден: {EXCLUSIONS_PATH}"]

    exclusions_doc = json.loads(EXCLUSIONS_PATH.read_text(encoding="utf-8"))
    exclusions = exclusions_doc.get("exclusions", {})

    # Duplicate lesson_id at the top level of the manifest.
    top_pairs = _load_top_level_pairs(MANIFEST_PATH)
    lesson_id_counts = Counter(k for k, _ in top_pairs)
    for lesson_id, count in lesson_id_counts.items():
        if count > 1:
            errors.append(f"Дубликат lesson_id в манифесте: {lesson_id!r} встречается {count} раз(а)")

    # Duplicate notebook mappings (same .ipynb claimed by >1 lesson_id).
    notebook_owners: dict[str, list[str]] = {}
    for lesson_id, entry in manifest.items():
        nb = entry.get("notebook")
        if nb:
            notebook_owners.setdefault(nb, []).append(lesson_id)
    for nb, owners in notebook_owners.items():
        if len(owners) > 1:
            errors.append(f"Ноутбук {nb!r} сопоставлен нескольким lesson_id: {owners}")

    # Every canonical notebook must be in exactly one of {manifest, exclusions}.
    canonical = _canonical_notebooks()
    mapped = set(notebook_owners.keys())
    excluded = set(exclusions.keys())

    unexplained_missing = canonical - mapped - excluded
    for nb in sorted(unexplained_missing):
        errors.append(f"Необъяснённый пробел: ноутбук {nb!r} не сопоставлен записи в манифесте и не задокументирован как исключение")

    in_both = mapped & excluded
    for nb in sorted(in_both):
        errors.append(f"Противоречивая классификация: ноутбук {nb!r} одновременно и в манифесте, и в исключениях")

    excluded_missing_file = excluded - canonical
    for nb in sorted(excluded_missing_file):
        errors.append(f"Исключение ссылается на несуществующий ноутбук: {nb!r}")

    for nb, info in exclusions.items():
        if not isinstance(info, dict) or not info.get("reason"):
            errors.append(f"Исключение {nb!r} не документировано (отсутствует непустое поле 'reason')")

    # Orphan practice routes: a generated site/practice/<id>/ with no manifest entry.
    if PRACTICE_DIR.exists():
        practice_dirs = {p.name for p in PRACTICE_DIR.iterdir() if p.is_dir() and p.name != "graders"}
        orphans = practice_dirs - set(manifest.keys())
        for lesson_id in sorted(orphans):
            errors.append(f"Осиротевшая директория практики без записи в манифесте: site/practice/{lesson_id}/")

    return errors


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

        if backend == "local-required" and assessment != "local-required":
            errors.append(
                f"{prefix} backend='local-required' требует assessment='local-required' "
                f"(получено {assessment!r}) — нет задокументированного исключения"
            )
        if backend == "local-required" and grader:
            errors.append(f"{prefix} backend='local-required' не должен ссылаться на grader (нет Pyodide-раннера)")

    errors += validate_global_completeness(manifest)

    return errors


def main() -> None:
    errors = validate()
    if errors:
        print(f"Манифест невалиден — найдено ошибок: {len(errors)}\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    exclusions = json.loads(EXCLUSIONS_PATH.read_text(encoding="utf-8")).get("exclusions", {})
    canonical = _canonical_notebooks()
    print(
        f"Манифест валиден: {len(manifest)} урок(ов) проверено. "
        f"Полнота учебного плана: {len(canonical)} канонических ноутбуков, "
        f"{len(manifest)} с практикой, {len(exclusions)} намеренно исключены, "
        f"0 необъяснённых пробелов."
    )


if __name__ == "__main__":
    main()
