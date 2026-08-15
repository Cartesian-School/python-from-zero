# Доверенный грейдер для практики 05-05 (не редактируется учеником).
#
# random.randint даёт разные числа при каждом запуске, поэтому точный вывод
# проверить нельзя — вместо этого проверяем реальные СВОЙСТВА результата
# напрямую по переменным (dice1/dice2 — те же глобальные имена, что и в
# ячейке ученика, поскольку грейдер выполняется в той же сессии): каждое
# значение действительно в диапазоне кубика, а напечатанная сумма ему
# соответствует. Это настоящая детерминированная проверка инварианта,
# а не просто «ячейка не упала».

_cells = __cartesian__["cells"]

_primer = _cells.get("959c006a", {})   # random.randint(1, 6) — рабочий пример
_zadanie = _cells.get("2d7e41af", {})  # dice1, dice2 = ...; print(...)

_dice_valid = False
_sum_matches = False
try:
    _dice_valid = 1 <= dice1 <= 6 and 1 <= dice2 <= 6  # noqa: F821
    _zadanie_stdout = _zadanie.get("stdout", "")
    _sum_matches = str(dice1 + dice2) in _zadanie_stdout  # noqa: F821
except NameError:
    _dice_valid = False
    _sum_matches = False

checks = [
    {
        "name": "Рабочий пример: random.randint выполнен без ошибок",
        "passed": bool(_primer) and _primer.get("ok", False),
    },
    {
        "name": "Задание ★: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
    {
        "name": "Задание ★: оба броска в диапазоне 1–6",
        "passed": _dice_valid,
    },
    {
        "name": "Задание ★: напечатанная сумма совпадает с dice1 + dice2",
        "passed": _sum_matches,
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "05-05", "passed": passed, "score": score, "checks": checks}
