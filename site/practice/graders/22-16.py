# Доверенный грейдер для практики 22-16 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("5b4924cf", {})  # "Проверка результата" -- zadacha_dlya_api() формирует словарь с bool-полем done
_zadanie = _cells.get("e9fecf3d", {})  # "Задание ★★" -- spisok_dlya_api() применяет форматирование к списку записей

checks = [
    {
        "name": "Проверка результата: zadacha_dlya_api() формирует словарь с bool-полем done",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Проверка результата: spisok_dlya_api() применяет форматирование к списку записей",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "22-16", "passed": passed, "score": score, "checks": checks}
