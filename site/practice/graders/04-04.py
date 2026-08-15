# Доверенный грейдер для практики 04-04 (не редактируется учеником).

_cells = __cartesian__["cells"]

_zadanie = _cells.get("8434ce30", {})  # str(total) и f-строка, total = 100

_zadanie_lines = [s for s in _zadanie.get("stdout", "").splitlines() if s.strip()]
_expected = "Итого: 100"

checks = [
    {
        "name": "Задание ★: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
    {
        "name": "Задание ★: обе строки — «Итого: 100»",
        "passed": len(_zadanie_lines) == 2 and all(line == _expected for line in _zadanie_lines),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "04-04", "passed": passed, "score": score, "checks": checks}
