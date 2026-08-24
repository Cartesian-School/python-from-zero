# Доверенный грейдер для практики 23-14 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("70c51825", {})  # "Проверка результата" -- свободное имя находится по схеме name (n).ext
_zadanie = _cells.get("ad57ebf7", {})  # "Задание ★" -- та же схема отработала для photo.jpg

checks = [
    {
        "name": "Проверка результата: свободное имя находится по схеме name (n).ext (otchet.pdf)",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Проверка результата: та же схема name (n).ext отработала для photo.jpg",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "23-14", "passed": passed, "score": score, "checks": checks}
