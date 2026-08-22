# Доверенный грейдер для практики 20-18 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("4f55549c", {})  # "Проверка результата" -- границы Rect и ось Y

checks = [
    {
        "name": "Проверка результата: границы прямоугольника посчитаны верно",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "20-18", "passed": passed, "score": score, "checks": checks}
