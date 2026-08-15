# Доверенный грейдер для практики 05-01 (не редактируется учеником).
#
# price/paid — фиксированные значения в самом задании, поэтому ожидаемый
# результат детерминирован (не зависит от личных данных ученика).

_cells = __cartesian__["cells"]

_zadanie = _cells.get("d15260d5", {})  # change = paid - price

checks = [
    {
        "name": "Задание ★: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
    {
        "name": "Задание ★: сдача равна 150",
        "passed": _zadanie.get("stdout", "").strip() == "150",
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "05-01", "passed": passed, "score": score, "checks": checks}
