# Доверенный грейдер для практики 22-31 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("364498b1", {})  # "Проверка результата" -- clean_title() отклоняет пустой и слишком длинный ввод

checks = [
    {
        "name": "Проверка результата: clean_title() отклоняет пустой и слишком длинный ввод",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "22-31", "passed": passed, "score": score, "checks": checks}
