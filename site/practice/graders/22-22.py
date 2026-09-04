# Доверенный грейдер для практики 22-22 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("6ae5b261", {})  # "Проверка результата" -- Create и Read через модуль sqlite3
_update_delete = _cells.get("e1f1a1e9", {})  # "Эксперимент — Update" -- Update и Delete через модуль sqlite3

checks = [
    {
        "name": "Проверка результата: Create и Read через модуль sqlite3",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Проверка результата: Update и Delete через модуль sqlite3",
        "passed": bool(_update_delete) and _update_delete.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "22-22", "passed": passed, "score": score, "checks": checks}
