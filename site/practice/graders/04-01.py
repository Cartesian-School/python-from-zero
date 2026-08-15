# Доверенный грейдер для практики 04-01 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука — переменные
# верхнего уровня (например, age, days) видны напрямую как глобальные имена,
# поэтому можно проверить реальную математическую связь между ними, а не
# только текст, напечатанный в stdout.

_cells = __cartesian__["cells"]

_zadanie = _cells.get("f90e0202", {})   # print(name, age, city)
_samost = _cells.get("df8d2c3a", {})    # days = age * 365

_zadanie_lines = [s for s in _zadanie.get("stdout", "").splitlines() if s.strip()]

_days_correct = False
try:
    _days_correct = days == age * 365  # noqa: F821 (age/days defined by the learner's cell)
except NameError:
    _days_correct = False

checks = [
    {
        "name": "Задание ★: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
    {
        "name": "Задание ★: одна строка с именем, возрастом и городом",
        "passed": len(_zadanie_lines) == 1 and len(_zadanie_lines[0].split()) >= 3,
    },
    {
        "name": "Самостоятельная практика ★★: ячейка выполнена без ошибок",
        "passed": bool(_samost) and _samost.get("ok", False),
    },
    {
        "name": "Самостоятельная практика ★★: days равно age * 365",
        "passed": _days_correct,
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "04-01", "passed": passed, "score": score, "checks": checks}
