# Доверенный грейдер для практики 23-18 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("91a44f4e", {})  # "Проверка результата" -- ровно две группы дубликатов найдены, уникальные файлы не попали ни в одну
_zadanie = _cells.get("039d8c09", {})  # "Задание ★★" -- два файла нулевого размера образовали отдельную группу дубликатов

checks = [
    {
        "name": "Проверка результата: найдены ровно две группы дубликатов, уникальные файлы не попали ни в одну",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Задание: два файла нулевого размера образовали отдельную группу дубликатов",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "23-18", "passed": passed, "score": score, "checks": checks}
