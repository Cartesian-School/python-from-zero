# Доверенный грейдер для практики 23-17 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("ad5ebcde", {})  # "Проверка результата" -- sha256_file совпадает с hashlib.sha256() при любом размере блока
_zadanie = _cells.get("7360d7e7", {})  # "Задание ★" -- один изменённый байт дал совсем другой дайджест

checks = [
    {
        "name": "Проверка результата: sha256_file() совпадает с hashlib.sha256() напрямую при любом размере блока",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Проверка результата: один изменённый байт содержимого даёт совсем другой дайджест",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "23-17", "passed": passed, "score": score, "checks": checks}
