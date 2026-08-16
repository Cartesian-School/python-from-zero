# Доверенный грейдер для практики 05-17 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_zadanie = _cells.get("a1db517f", {})  # Задание — log2(1024)

checks = [
    {
        "name": "Задание: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get('ok', False),
    },
    {
        "name": "Задание: выведено 10.0",
        "passed": _zadanie.get('stdout','').strip() == "10.0",
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "05-17", "passed": passed, "score": score, "checks": checks}
