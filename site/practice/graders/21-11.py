# Доверенный грейдер для практики 21-11 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("b7549213", {})  # "Проверка результата" -- нормализация и clamp
_zadanie = _cells.get("ca65ce41", {})   # "Задание ★" -- равенство прямой и диагональной скорости

checks = [
    {
        "name": "Проверка результата: нормализация вектора и clamp позиции посчитаны верно",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Задание ★: диагональная скорость равна прямой после нормализации",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "21-11", "passed": passed, "score": score, "checks": checks}
