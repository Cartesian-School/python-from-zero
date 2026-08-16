# Доверенный грейдер для практики 04-02 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_zadanie = _cells.get("1dbe52df", {})  # Задание — переименованные переменные
_samost = _cells.get("d68a39df", {})  # Самостоятельная практика — НДС

checks = [
    {
        "name": "Задание: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get('ok', False),
    },
    {
        "name": "Задание: выведено 2 строки",
        "passed": len([s for s in _zadanie.get('stdout','').splitlines() if s.strip()]) >= 2,
    },
    {
        "name": "Самостоятельная практика: ячейка выполнена без ошибок",
        "passed": bool(_samost) and _samost.get('ok', False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "04-02", "passed": passed, "score": score, "checks": checks}
