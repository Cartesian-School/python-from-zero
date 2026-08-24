# Доверенный грейдер для практики 23-12 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("6344c2ac", {})  # "Проверка результата" -- каждый файл получил путь Sorted/<категория>/<имя>
_zadanie = _cells.get("dcc85ad0", {})  # "Задание ★" -- файл с неизвестным расширением попал в Sorted/other/

checks = [
    {
        "name": "Проверка результата: каждый файл плана получил путь Sorted/<категория>/<имя>",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Проверка результата: файл с неизвестным расширением попал в Sorted/other/",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "23-12", "passed": passed, "score": score, "checks": checks}
