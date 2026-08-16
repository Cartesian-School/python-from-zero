# Доверенный грейдер для практики 04-09 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_zadanie = _cells.get("f5171db2", {})  # Задание — приоритет **
_samost = _cells.get("a379278e", {})  # Самостоятельная практика — скобки

checks = [
    {
        "name": "Задание: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get('ok', False),
    },
    {
        "name": "Задание: выведено 6",
        "passed": _zadanie.get('stdout','').strip() == '6',
    },
    {
        "name": "Самостоятельная практика: ячейка выполнена без ошибок",
        "passed": bool(_samost) and _samost.get('ok', False),
    },
    {
        "name": "Самостоятельная практика: выведено 19",
        "passed": _samost.get('stdout','').strip() == '19',
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "04-09", "passed": passed, "score": score, "checks": checks}
