# Доверенный грейдер для практики 20-22 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("7239ee68", {})  # "Проверка результата" -- гравитация и отскок с затуханием
_zadanie = _cells.get("db4ff408", {})   # "Задание ★" -- отскоки до почти полной остановки

checks = [
    {
        "name": "Проверка результата: гравитация и затухание при отскоке посчитаны верно",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Задание ★: число отскоков до остановки посчитано без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "20-22", "passed": passed, "score": score, "checks": checks}
