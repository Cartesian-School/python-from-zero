# Доверенный грейдер для практики 03-04 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_zadanie = _cells.get("354be90d", {})  # "Задание ★" — sep=" · "
_samost = _cells.get("5e3714e2", {})   # "Самостоятельная практика ★★" — sep=" — "

_zadanie_lines = [s for s in _zadanie.get("stdout", "").splitlines() if s.strip()]
_samost_lines = [s for s in _samost.get("stdout", "").splitlines() if s.strip()]

checks = [
    {
        "name": "Задание ★: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
    {
        "name": "Задание ★: использован разделитель « · »",
        "passed": any(" · " in line for line in _zadanie_lines),
    },
    {
        "name": "Самостоятельная практика ★★: ячейка выполнена без ошибок",
        "passed": bool(_samost) and _samost.get("ok", False),
    },
    {
        "name": "Самостоятельная практика ★★: минимум 2 строки с « — »",
        "passed": sum(1 for line in _samost_lines if " — " in line) >= 2,
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "03-04", "passed": passed, "score": score, "checks": checks}
