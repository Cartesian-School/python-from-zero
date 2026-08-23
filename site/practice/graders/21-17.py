# Доверенный грейдер для практики 21-17 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("24487d9d", {})  # "Проверка результата" -- формулы сложности ограничены

checks = [
    {
        "name": "Проверка результата: интервал появления врагов и их скорость растут со счётом, но ограничены",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "21-17", "passed": passed, "score": score, "checks": checks}
