#!/usr/bin/env python3
"""Валидирует задокументированную связь учебного SafeSort с upstream.

Большинство файлов совпадает с зафиксированным тегом upstream; небольшой
учебный correction layer перечислен явно. Проверка остаётся полностью
офлайн: она фиксирует итоговые хеши и не выдаёт локальный lock за проверку
текущего состояния GitHub.

Источник истины для ожидаемых хешей — projects/python/safesort/
.upstream-sync.json (поле "locked_files": {относительный путь: sha256}).
Поле ``course_corrections`` обязано перечислять upstream-хеш и причину для
каждого намеренно изменённого файла. Обновление lock остаётся отдельным
сознательным шагом после реальной сверки по процедуре из UPSTREAM.md.

Отклоняет, если:
- .upstream-sync.json отсутствует или не парсится;
- зафиксированный файл отсутствует на диске;
- содержимое файла на диске не совпадает с зафиксированным хешем;
- на диске появился *.py файл под src/ или tests/, которого нет в
  locked_files (файл добавлен без обновления замка — тоже расхождение,
  а не "новая фича, ничего страшного").

Использование: python3 scripts/validate_safesort_upstream_sync.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAFESORT_DIR = ROOT / "projects" / "python" / "safesort"
LOCK_PATH = SAFESORT_DIR / ".upstream-sync.json"


def validate() -> list[str]:
    errors: list[str] = []

    if not LOCK_PATH.exists():
        return [f"Файл замка не найден: {LOCK_PATH.relative_to(ROOT)}"]

    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    locked_files: dict[str, str] = lock.get("locked_files", {})
    corrections: dict[str, dict[str, str]] = lock.get("course_corrections", {})
    if not locked_files:
        return ["Поле 'locked_files' пустое или отсутствует в .upstream-sync.json"]

    if lock.get("relationship") != "course-corrected-snapshot":
        errors.append("Поле 'relationship' должно быть 'course-corrected-snapshot'")

    for rel_path, correction in sorted(corrections.items()):
        if rel_path not in locked_files:
            errors.append(f"{rel_path}: course_corrections не имеет соответствующего locked_files")
        upstream_hash = correction.get("upstream_sha256", "")
        reason = correction.get("reason", "").strip()
        if len(upstream_hash) != 64:
            errors.append(f"{rel_path}: отсутствует корректный upstream_sha256")
        if not reason:
            errors.append(f"{rel_path}: отсутствует причина учебной коррекции")
        if locked_files.get(rel_path) == upstream_hash:
            errors.append(f"{rel_path}: коррекция заявлена, но итоговый хеш равен upstream")

    for rel_path, expected_hash in sorted(locked_files.items()):
        path = SAFESORT_DIR / rel_path
        if not path.exists():
            errors.append(f"{rel_path}: файл зафиксирован в замке, но отсутствует на диске")
            continue
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            errors.append(
                f"{rel_path}: содержимое разошлось с lock учебного снимка "
                f"(ожидался sha256 {expected_hash}, получен {actual_hash}); "
                f"проверьте upstream и correction layer по процедуре из UPSTREAM.md"
            )

    actual_py_files = set()
    for sub in ("src", "tests"):
        for f in sorted((SAFESORT_DIR / sub).rglob("*.py")):
            actual_py_files.add(str(f.relative_to(SAFESORT_DIR)))

    unlocked = actual_py_files - locked_files.keys()
    for rel_path in sorted(unlocked):
        errors.append(
            f"{rel_path}: файл есть на диске под src/ или tests/, но не "
            f"зафиксирован в .upstream-sync.json — добавьте его в locked_files "
            f"после сверки с реальным репозиторием"
        )

    return errors


def main() -> None:
    errors = validate()
    if errors:
        print(f"Синхронизация со snapshot'ом safesort невалидна — найдено ошибок: {len(errors)}\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    print(
        f"Связь SafeSort с upstream валидна: {len(lock['locked_files'])} файл(ов) "
        f"зафиксированы, учебных коррекций: {len(lock['course_corrections'])}; "
        f"база {lock['canonical_tag']} @ {lock['canonical_commit'][:12]}."
    )


if __name__ == "__main__":
    main()
