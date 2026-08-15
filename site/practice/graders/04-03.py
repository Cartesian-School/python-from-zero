# Доверенный грейдер для практики 04-03 (не редактируется учеником).
#
# type(значение) печатает одну и ту же строку независимо от конкретного
# числа (пока тип верный), поэтому ожидаемый вывод детерминирован даже
# при том, что значения i/f/c ученик придумывает сам.

_cells = __cartesian__["cells"]

_zadanie = _cells.get("c4dd68e9", {})  # print(type(i), type(f), type(c))

_expected = "<class 'int'> <class 'float'> <class 'complex'>"

checks = [
    {
        "name": "Задание ★: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
    {
        "name": "Задание ★: типы — int, float, complex",
        "passed": _zadanie.get("stdout", "").strip() == _expected,
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "04-03", "passed": passed, "score": score, "checks": checks}
