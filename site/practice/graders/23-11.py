# Доверенный грейдер для практики 23-11 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("972fa623", {})  # "Проверка результата" -- classify() регистронезависима, неизвестное расширение -> other
_zadanie = _cells.get("a3c0687a", {})  # "Задание ★" -- собственная категория presentations работает наравне со встроенными

checks = [
    {
        "name": "Проверка результата: classify() регистронезависима, неизвестное расширение попадает в other",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Проверка результата: собственная категория presentations работает наравне со встроенными",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "23-11", "passed": passed, "score": score, "checks": checks}
