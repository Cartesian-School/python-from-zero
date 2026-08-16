# Доверенный грейдер для практики 05-08 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_zadanie = _cells.get("69d62bf1", {})  # Задание — -17 // 5 и -17 % 5

checks = [
    {
        "name": "Задание: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get('ok', False),
    },
    {
        "name": "Задание: выведено -4 3",
        "passed": _zadanie.get('stdout','').strip() == "-4 3",
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "05-08", "passed": passed, "score": score, "checks": checks}
