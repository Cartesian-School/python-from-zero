# Доверенный грейдер для практики 23-15 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("95562664", {})  # "Проверка результата" -- манифест пережил json.dumps()/json.loads() без потерь
_zadanie = _cells.get("1185438d", {})  # "Задание ★" -- количество успешных перемещений посчитано верно

checks = [
    {
        "name": "Проверка результата: манифест пережил json.dumps()/json.loads() без потерь",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Проверка результата: количество успешных перемещений (completed=True) посчитано верно",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "23-15", "passed": passed, "score": score, "checks": checks}
