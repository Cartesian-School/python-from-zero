# Доверенный грейдер для практики 05-02 (не редактируется учеником).
#
# Ноутбук уже содержит собственную ячейку самопроверки (id 2c4eb887,
# assert 2 + 3 * 4 ** 2 == 50) — используем её как основной сигнал,
# как и в графике для 03-03.

_cells = __cartesian__["cells"]

_zadanie = _cells.get("b96f7fb7", {})   # print(2 + 3 * 4 ** 2)
_proverka = _cells.get("2c4eb887", {})  # assert ... == 50

checks = [
    {
        "name": "Задание ★: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
    {
        "name": "Задание ★: результат равен 50",
        "passed": _zadanie.get("stdout", "").strip() == "50",
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

{"lesson_id": "05-02", "passed": passed, "score": score, "checks": checks}
