# Доверенный грейдер для практики 05-06 (не редактируется учеником).
#
# Ноутбук уже содержит собственную ячейку самопроверки (id 950688f8).
# Для Задания ★★ проверяем сам результат (числа, кратные 7 от 1 до 100),
# не завязываясь на точный текст, чтобы проверка оставалась осмысленной,
# даже если ученик слегка изменит форматирование вывода.

_cells = __cartesian__["cells"]

_zadanie = _cells.get("aebbe920", {})   # kratnoe_chemu = 7, диапазон 1..100
_proverka = _cells.get("950688f8", {})  # assert count == 10 (кратные 5 от 1 до 50)

_zadanie_lines = [s for s in _zadanie.get("stdout", "").splitlines() if s.strip()]
_expected_multiples = [n for n in range(1, 101) if n % 7 == 0]
_zadanie_correct = False
try:
    _zadanie_correct = [int(s) for s in _zadanie_lines] == _expected_multiples
except ValueError:
    _zadanie_correct = False

checks = [
    {
        "name": "Задание ★★: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
    {
        "name": "Задание ★★: выведены все числа, кратные 7, от 1 до 100",
        "passed": _zadanie_correct,
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

{"lesson_id": "05-06", "passed": passed, "score": score, "checks": checks}
