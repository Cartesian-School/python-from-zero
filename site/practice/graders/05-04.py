# Доверенный грейдер для практики 05-04 (не редактируется учеником).
#
# Ноутбук уже содержит собственную ячейку самопроверки (id e72167bb,
# assert math.sqrt(3**2 + 4**2) == 5.0).

_cells = __cartesian__["cells"]

_zadanie = _cells.get("9f38c429", {})   # hypotenuse = math.sqrt(3**2 + 4**2)
_proverka = _cells.get("e72167bb", {})  # assert ... == 5.0

checks = [
    {
        "name": "Задание ★: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
    {
        "name": "Задание ★: гипотенуза равна 5.0",
        "passed": _zadanie.get("stdout", "").strip() == "5.0",
    },
    {
        "name": "Проверка результата: assert пройден",
        "passed": bool(_proverka) and _proverka.get("ok", False)
        and "Верно" in _proverka.get("stdout", ""),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "05-04", "passed": passed, "score": score, "checks": checks}
