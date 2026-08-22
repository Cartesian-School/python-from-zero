# Доверенный грейдер для практики 20-16 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("cb6f07bd", {})  # "Проверка результата" -- FPS-независимость через dt
_zadanie = _cells.get("ee7d5a6f", {})   # "Задание ★★" -- наивная версия БЕЗ dt

checks = [
    {
        "name": "Проверка результата: движение через delta time не зависит от FPS",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Задание ★★: наивная версия без dt воспроизведена и зависит от FPS",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "20-16", "passed": passed, "score": score, "checks": checks}
