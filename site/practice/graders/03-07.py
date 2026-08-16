# Доверенный грейдер для практики 03-07 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_ispravlenie = _cells.get("1841495a", {})  # "Исправление" — favourite_city после NameError
_zadanie = _cells.get("f97a5a34", {})      # "Задание ★ Базовая практика"

_zadanie_lines = [s for s in _zadanie.get("stdout", "").splitlines() if s.strip()]

checks = [
    {
        "name": "Исправление: ячейка выполнена без ошибок",
        "passed": bool(_ispravlenie) and _ispravlenie.get("ok", False),
    },
    {
        "name": "Задание ★: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
    {
        "name": "Задание ★: все три имени выведены в одной строке",
        "passed": len(_zadanie_lines) == 1 and len(_zadanie_lines[0].split()) >= 3,
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "03-07", "passed": passed, "score": score, "checks": checks}
