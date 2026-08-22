# Доверенный грейдер для практики 20-21 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("2c1b2f4a", {})  # "Проверка результата" -- AABB-пересечение
_zadanie = _cells.get("edb29970", {})   # "Задание ★★" -- уменьшенный хитбокс

checks = [
    {
        "name": "Проверка результата: пересечение прямоугольников находится верно",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Задание ★★: уменьшенный хитбокс реализован без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "20-21", "passed": passed, "score": score, "checks": checks}
