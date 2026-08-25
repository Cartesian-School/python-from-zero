#!/usr/bin/env python3
"""Валидирует, что projects/python/safesort/{src,tests} не разошлись
с зафиксированным снимком реального репозитория Cartesian-School/safesort —
без обращений к сети.

projects/python/safesort/ — учебный снимок реального репозитория (см.
UPSTREAM.md). Код в src/ и tests/ обязан оставаться побайтово идентичным
тому, что было в реальном репозитории на момент последней сверки: любое
случайное редактирование снимка без соответствующего изменения в реальном
репозитории — это расхождение, которое должно провалить сборку, а не
остаться незамеченным.

Источник истины для ожидаемых хешей — projects/python/safesort/
.upstream-sync.json (поле "locked_files": {относительный путь: sha256}).
Сам скрипт сеть не трогает: сверка идёт с уже зафиксированными хешами,
обновлять которые — отдельный сознательный шаг после реальной синхронизации
с апстримом (см. процедуру в UPSTREAM.md).

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
    if not locked_files:
        return ["Поле 'locked_files' пустое или отсутствует в .upstream-sync.json"]

    for rel_path, expected_hash in sorted(locked_files.items()):
        path = SAFESORT_DIR / rel_path
        if not path.exists():
            errors.append(f"{rel_path}: файл зафиксирован в замке, но отсутствует на диске")
            continue
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            errors.append(
                f"{rel_path}: содержимое разошлось с зафиксированным снимком "
                f"апстрима (ожидался sha256 {expected_hash}, получен {actual_hash}) — "
                f"либо это случайная правка снимка (откатите её), либо реальная "
                f"синхронизация с апстримом (обновите .upstream-sync.json по "
                f"процедуре из UPSTREAM.md)"
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
        f"Snapshot safesort синхронизирован: {len(lock['locked_files'])} файл(ов) src/tests "
        f"совпадают с зафиксированным состоянием апстрима "
        f"({lock['canonical_tag']} @ {lock['canonical_commit'][:12]})."
    )


if __name__ == "__main__":
    main()
