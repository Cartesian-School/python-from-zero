# Доверенный грейдер для практики 04-06 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_exp2 = _cells.get("c28bb633", {})  # Эксперимент 2 — неизменяемость
_zadanie = _cells.get("badd992c", {})  # Задание — подчёркивания

checks = [
    {
        "name": "Эксперимент 2: ячейка выполнена без ошибок",
        "passed": bool(_exp2) and _exp2.get('ok', False),
    },
    {
        "name": "Эксперимент 2: b не изменился (10)",
        "passed": '10' in _exp2.get('stdout',''),
    },
    {
        "name": "Задание: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get('ok', False),
    },
    {
        "name": "Задание: выведено 38000000",
        "passed": '38000000' in _zadanie.get('stdout',''),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "04-06", "passed": passed, "score": score, "checks": checks}
