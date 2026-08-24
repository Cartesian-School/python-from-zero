# Доверенный грейдер для практики 23-22 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("6c29b672", {})  # "Проверка результата" -- три файла с одинаковым содержимым образуют одну группу из трёх
_zadanie = _cells.get("9551246f", {})  # "Задание ★★" -- три группы размеров, дубликаты найдены только в одной из них

checks = [
    {
        "name": "Проверка результата: три файла с одинаковым содержимым образуют одну группу из трёх, а не полтора дубликата",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Задание: из трёх групп размеров дубликаты найдены только в одной",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "23-22", "passed": passed, "score": score, "checks": checks}
