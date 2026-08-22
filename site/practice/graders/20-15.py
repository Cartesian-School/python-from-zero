# Доверенный грейдер для практики 20-15 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_proverka = _cells.get("a79f6adc", {})  # "Проверка результата"
_zadanie = _cells.get("b136f08b", {})   # "Задание ★ Базовая практика"

checks = [
    {
        "name": "Проверка результата: время кадра и FPS посчитаны верно",
        "passed": bool(_proverka) and _proverka.get("ok", False),
    },
    {
        "name": "Задание ★: skolko_kadrov_za_sekundy() реализована без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "20-15", "passed": passed, "score": score, "checks": checks}
