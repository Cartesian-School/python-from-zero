# Доверенный грейдер для практики 03-08 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_rabochij = _cells.get("f81ad8a2", {})   # "Рабочий пример" — ожидаемый NameError
_reshenie = _cells.get("2fc825ef", {})   # "Решение задания" — исправленная опечатка

checks = [
    {
        "name": "Рабочий пример: ячейка действительно завершилась ошибкой",
        "passed": bool(_rabochij) and not _rabochij.get("ok", True),
    },
    {
        "name": "Решение задания: ячейка выполнена без ошибок",
        "passed": bool(_reshenie) and _reshenie.get("ok", False),
    },
    {
        "name": "Решение задания: выведено число 100",
        "passed": "100" in _reshenie.get("stdout", ""),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "03-08", "passed": passed, "score": score, "checks": checks}
