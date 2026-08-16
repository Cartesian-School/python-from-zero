# Доверенный грейдер для практики 04-07 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_exp2 = _cells.get("b8c92560", {})  # Эксперимент 2 — обратное преобразование
_zadanie = _cells.get("1a9e0b84", {})  # Задание — год рождения

checks = [
    {
        "name": "Эксперимент 2: ячейка выполнена без ошибок",
        "passed": bool(_exp2) and _exp2.get('ok', False),
    },
    {
        "name": "Эксперимент 2: выведено 255 и 10",
        "passed": '255' in _exp2.get('stdout','') and '10' in _exp2.get('stdout',''),
    },
    {
        "name": "Задание: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get('ok', False),
    },
    {
        "name": "Задание: выведено 3 строки",
        "passed": len([s for s in _zadanie.get('stdout','').splitlines() if s.strip()]) >= 3,
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "04-07", "passed": passed, "score": score, "checks": checks}
