# Доверенный грейдер для практики 23-08 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("ebab97b2", {})  # "Проверка результата" -- оператор / и атрибуты name/suffix/parent работают верно
_zadanie = _cells.get("4adcf839", {})  # "Задание ★" -- FileInfo для photo.JPG: расширение приведено к нижнему регистру

checks = [
    {
        "name": "Проверка результата: оператор / и атрибуты name/suffix/parent работают верно",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Проверка результата: FileInfo для photo.JPG — расширение приведено к нижнему регистру",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "23-08", "passed": passed, "score": score, "checks": checks}
