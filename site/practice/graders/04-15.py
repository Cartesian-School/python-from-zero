# Доверенный грейдер для практики 04-15 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_exp1 = _cells.get("f42fdebf", {})  # Эксперимент 1 — округление до чётного
_zadanie = _cells.get("d7f181fb", {})  # Задание — округление до 2 знаков

checks = [
    {
        "name": "Эксперимент 1: ячейка выполнена без ошибок",
        "passed": bool(_exp1) and _exp1.get('ok', False),
    },
    {
        "name": "Эксперимент 1: выведено 2 и 4",
        "passed": '2' in _exp1.get('stdout','') and '4' in _exp1.get('stdout',''),
    },
    {
        "name": "Задание: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get('ok', False),
    },
    {
        "name": "Задание: выведено 7.46",
        "passed": '7.46' in _zadanie.get('stdout',''),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "04-15", "passed": passed, "score": score, "checks": checks}
