# Доверенный грейдер для практики 03-09 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_rabochij = _cells.get("4a0010a3", {})    # "Рабочий пример" — ожидаемый SyntaxError
_ispravlenie = _cells.get("f680f058", {})  # "Исправление"
_reshenie = _cells.get("980acbcc", {})     # "Решение задания"

checks = [
    {
        "name": "Рабочий пример: ячейка действительно завершилась ошибкой",
        "passed": bool(_rabochij) and not _rabochij.get("ok", True),
    },
    {
        "name": "Исправление: ячейка выполнена без ошибок",
        "passed": bool(_ispravlenie) and _ispravlenie.get("ok", False),
    },
    {
        "name": "Решение задания: ячейка выполнена без ошибок",
        "passed": bool(_reshenie) and _reshenie.get("ok", False),
    },
    {
        "name": "Решение задания: выведено «Готово!»",
        "passed": "Готово!" in _reshenie.get("stdout", ""),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "03-09", "passed": passed, "score": score, "checks": checks}
