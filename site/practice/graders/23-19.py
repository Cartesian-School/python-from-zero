# Доверенный грейдер для практики 23-19 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("b2b7fee4", {})  # "Проверка результата -- TOML разобран" -- tomllib.loads() вернул словарь ожидаемой структуры
_zadanie = _cells.get("26079b97", {})  # "Задание ★" -- без явных настроек используются значения по умолчанию

checks = [
    {
        "name": "Проверка результата: tomllib.loads() вернул словарь ожидаемой структуры",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Проверка результата: без секции [extensions] используются значения по умолчанию",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "23-19", "passed": passed, "score": score, "checks": checks}
