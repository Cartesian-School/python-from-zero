# Доверенный грейдер для практики 22-32 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_uyazvimyj = _cells.get("d52a0b19", {})  # "Проверка результата — таблица пострадала" -- уязвимый вариант действительно повредил таблицу
_bezopasnyj = _cells.get("b3f19acb", {})  # "Эксперимент — параметризованный" -- параметризованный запрос защитил таблицу

checks = [
    {
        "name": "Проверка результата: уязвимый вариант действительно повредил таблицу",
        "passed": bool(_uyazvimyj) and _uyazvimyj.get("ok", False),
    },
    {
        "name": "Проверка результата: параметризованный запрос защитил таблицу",
        "passed": bool(_bezopasnyj) and _bezopasnyj.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "22-32", "passed": passed, "score": score, "checks": checks}
