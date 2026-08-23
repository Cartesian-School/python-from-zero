# Доверенный грейдер для практики 21-14 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("da834de9", {})  # "Проверка результата" -- while сохраняет overshoot
_zadanie = _cells.get("77622dc9", {})   # "Задание ★★" -- координата появления врага

checks = [
    {
        "name": "Проверка результата: таймер спавна сохраняет остаток времени",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Задание ★★: враг всегда появляется полностью внутри игрового поля",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "21-14", "passed": passed, "score": score, "checks": checks}
