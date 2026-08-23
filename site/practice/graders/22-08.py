# Доверенный грейдер для практики 22-08 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("6aa7882b", {})  # "Проверка результата" -- URL разобран на схему, хост, порт, путь, query и фрагмент
_zadanie = _cells.get("fff739a1", {})  # "Задание ★" -- второй URL разобран верно: путь и параметр done

checks = [
    {
        "name": "Проверка результата: URL разобран на схему, хост, порт, путь, query и фрагмент",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Проверка результата: второй URL разобран верно: путь и параметр done",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "22-08", "passed": passed, "score": score, "checks": checks}
