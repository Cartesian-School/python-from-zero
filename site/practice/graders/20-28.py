# Доверенный грейдер для практики 20-28 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("ec26d685", {})  # "Проверка результата" -- диагностика по симптому
_zadanie = _cells.get("45c700e6", {})   # "Задание ★" -- расширение справочника новым симптомом

checks = [
    {
        "name": "Проверка результата: симптомы сопоставлены правильным причинам",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Задание ★: справочник расширен новой парой симптом/причина",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "20-28", "passed": passed, "score": score, "checks": checks}
