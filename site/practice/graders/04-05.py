# Доверенный грейдер для практики 04-05 (не редактируется учеником).
#
# Задание ★★★ этого ноутбука прямо просит продемонстрировать ОБЕ версии —
# сломанную (которая обязана завершиться ошибкой) и исправленную. Поэтому
# для ячейки a8533ee4 корректный результат — ok=False (ошибка ожидаема и
# является частью верного выполнения задания), а не признак поломки.

_cells = __cartesian__["cells"]

_proverka1 = _cells.get("3404111d", {})  # assert-цепочка про типы
_zadanie2 = _cells.get("9628052c", {})   # print(str(7) + str(9))
_broken = _cells.get("a8533ee4", {})     # "Итого: " + 100 — должна упасть
_fixed = _cells.get("d351feb0", {})      # "Итого: " + str(100) — должна пройти

checks = [
    {
        "name": "Задание ★: проверка пяти типов пройдена",
        "passed": bool(_proverka1) and _proverka1.get("ok", False)
        and "Все пять ответов верны" in _proverka1.get("stdout", ""),
    },
    {
        "name": "Задание ★★: str(7) + str(9) равно '79'",
        "passed": bool(_zadanie2) and _zadanie2.get("ok", False)
        and _zadanie2.get("stdout", "").strip() == "79",
    },
    {
        "name": "Задание ★★★: сломанная версия действительно вызывает ошибку",
        "passed": bool(_broken) and not _broken.get("ok", True),
    },
    {
        "name": "Задание ★★★: исправленная версия выводит «Итого: 100»",
        "passed": bool(_fixed) and _fixed.get("ok", False)
        and _fixed.get("stdout", "").strip() == "Итого: 100",
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "04-05", "passed": passed, "score": score, "checks": checks}
