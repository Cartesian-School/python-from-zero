# Доверенный грейдер для практики 23-10 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("092ebde7", {})  # "Проверка результата" -- обязательные исключения пропускаются, обычные имена -- нет
_zadanie = _cells.get("c47288bd", {})  # "Задание ★" -- своё исключение добавлено, а Sorted/.safesort по-прежнему исключены всегда

checks = [
    {
        "name": "Проверка результата: обязательные исключения (.git, Sorted, .safesort) пропускаются, обычные имена -- нет",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Проверка результата: своё исключение добавлено, а Sorted/.safesort по-прежнему исключены всегда",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "23-10", "passed": passed, "score": score, "checks": checks}
