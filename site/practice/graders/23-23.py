# Доверенный грейдер для практики 23-23 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("f96ab544", {})  # "Проверка результата" -- apply разобран с правильным путём
_zadanie = _cells.get("2105edff", {})  # "Задание ★" -- неизвестная подкоманда завершает разбор с ненулевым кодом

checks = [
    {
        "name": "Проверка результата: apply разобран с правильным путём",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Задание: неизвестная подкоманда 'zip' тоже завершает разбор с ненулевым кодом",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "23-23", "passed": passed, "score": score, "checks": checks}
