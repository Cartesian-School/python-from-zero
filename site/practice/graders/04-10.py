# Доверенный грейдер для практики 04-10 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_exp2 = _cells.get("3064cc17", {})  # Эксперимент 2 — отрицательное floor-деление
_zadanie = _cells.get("a6f14b85", {})  # Задание — яблоки и корзины

checks = [
    {
        "name": "Эксперимент 2: ячейка выполнена без ошибок",
        "passed": bool(_exp2) and _exp2.get('ok', False),
    },
    {
        "name": "Эксперимент 2: выведено -3 и 2",
        "passed": '-3' in _exp2.get('stdout','') and '2' in _exp2.get('stdout',''),
    },
    {
        "name": "Задание: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get('ok', False),
    },
    {
        "name": "Задание: выведено 5 и 3",
        "passed": '5' in _zadanie.get('stdout','') and '3' in _zadanie.get('stdout',''),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "04-10", "passed": passed, "score": score, "checks": checks}
