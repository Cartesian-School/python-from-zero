# Доверенный грейдер для практики 04-17 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_exp1 = _cells.get("4d4884f3", {})  # Эксперимент 1 — сложение дробей

checks = [
    {
        "name": "Эксперимент 1: ячейка выполнена без ошибок",
        "passed": bool(_exp1) and _exp1.get('ok', False),
    },
    {
        "name": "Эксперимент 1: выведено 1/2",
        "passed": '1/2' in _exp1.get('stdout',''),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "04-17", "passed": passed, "score": score, "checks": checks}
