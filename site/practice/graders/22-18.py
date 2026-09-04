# Доверенный грейдер для практики 22-18 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("5967f748", {})  # "Проверка результата" -- выбор фреймворка соответствует таблице сравнения
_zadanie = _cells.get("60029475", {})  # "Задание ★★" -- добавлен верный выбор для низкоуровневого контроля над ASGI

checks = [
    {
        "name": "Проверка результата: выбор фреймворка соответствует таблице сравнения",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Проверка результата: добавлен верный выбор для низкоуровневого контроля над ASGI",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "22-18", "passed": passed, "score": score, "checks": checks}
