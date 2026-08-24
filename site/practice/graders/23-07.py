# Доверенный грейдер для практики 23-07 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("b595e48c", {})  # "Проверка результата" -- пять подкоманд разобраны, undo получает root по умолчанию
_zadanie = _cells.get("66d790d7", {})  # "Задание ★" -- duplicates разобрана с правильным путём

checks = [
    {
        "name": "Проверка результата: пять подкоманд разобраны, undo получает root по умолчанию, если он не передан",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Проверка результата: duplicates разобрана с правильным путём",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "23-07", "passed": passed, "score": score, "checks": checks}
