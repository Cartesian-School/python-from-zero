# Доверенный грейдер для практики 03-05 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_zadanie = _cells.get("7828a1ac", {})  # "Задание ★ Базовая практика"
_samost = _cells.get("97a50218", {})   # "Самостоятельная практика ★★"

_zadanie_lines = [s for s in _zadanie.get("stdout", "").splitlines() if s.strip()]

checks = [
    {
        "name": "Задание ★: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
    {
        "name": "Задание ★: выведено минимум 3 строки (три типа)",
        "passed": len(_zadanie_lines) >= 3,
    },
    {
        "name": "Самостоятельная практика ★★: ячейка выполнена без ошибок",
        "passed": bool(_samost) and _samost.get("ok", False),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "03-05", "passed": passed, "score": score, "checks": checks}
