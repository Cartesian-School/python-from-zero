# Доверенный грейдер для практики 03-02 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_zadanie = _cells.get("2da67db8", {})  # "Задание ★ Базовая практика"

_zadanie_lines = [s for s in _zadanie.get("stdout", "").splitlines() if s.strip()]


def _looks_numeric(s):
    try:
        float(s.strip())
        return True
    except ValueError:
        return False


_numeric_lines = [s for s in _zadanie_lines if _looks_numeric(s)]

checks = [
    {
        "name": "Задание ★: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
    {
        "name": "Задание ★: выведено минимум 3 строки",
        "passed": len(_zadanie_lines) >= 3,
    },
    {
        "name": "Задание ★: каждая строка — числовой результат",
        "passed": len(_numeric_lines) >= 3,
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "03-02", "passed": passed, "score": score, "checks": checks}
