# Доверенный грейдер для практики 04-22 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_lab1 = _cells.get("a4132423", {})  # Лаборатория 1 — ожидаемый ValueError
_fix1 = _cells.get("2a8d1303", {})  # Исправление 1
_zadanie = _cells.get("2e0c4660", {})  # Задание — Decimal сумма

checks = [
    {
        "name": "Лаборатория 1: ячейка действительно завершилась ошибкой",
        "passed": bool(_lab1) and not _lab1.get('ok', True),
    },
    {
        "name": "Исправление 1: ячейка выполнена без ошибок",
        "passed": bool(_fix1) and _fix1.get('ok', False),
    },
    {
        "name": "Исправление 1: выведено 255",
        "passed": '255' in _fix1.get('stdout',''),
    },
    {
        "name": "Задание: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get('ok', False),
    },
    {
        "name": "Задание: выведено 25.49",
        "passed": '25.49' in _zadanie.get('stdout',''),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "04-22", "passed": passed, "score": score, "checks": checks}
