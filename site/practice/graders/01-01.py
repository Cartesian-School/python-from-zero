# Доверенный грейдер для практики 01-01 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_zadanie = _cells.get("3ca309a1", {})   # "Задание ★ Базовая практика" (имя, цвет, число)
_samost = _cells.get("e1a23aa4", {})    # "Самостоятельная практика" (рисунок из символов)
_dopolnitelnaya = _cells.get("ea50acd2", {})  # "Дополнительная задача ★★★" (один print(), три значения)

_zadanie_lines = [s for s in _zadanie.get("stdout", "").splitlines() if s.strip()]
_samost_lines = [s for s in _samost.get("stdout", "").splitlines() if s.strip()]
_dop_lines = [s for s in _dopolnitelnaya.get("stdout", "").splitlines() if s.strip()]

checks = [
    {
        "name": "Задание ★: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
    {
        "name": "Задание ★: структурная проверка участия — выведено минимум 3 непустые строки",
        "passed": len(_zadanie_lines) >= 3,
    },
    {
        "name": "Самостоятельная практика: ячейка выполнена без ошибок",
        "passed": bool(_samost) and _samost.get("ok", False),
    },
    {
        "name": "Самостоятельная практика: структурная проверка участия — есть непустой вывод",
        "passed": len(_samost_lines) >= 1,
    },
    {
        "name": "Дополнительная задача ★★★: ячейка выполнена без ошибок",
        "passed": bool(_dopolnitelnaya) and _dopolnitelnaya.get("ok", False),
    },
    {
        "name": "Дополнительная задача ★★★: структурная проверка — одна строка минимум с тремя полями",
        "passed": len(_dop_lines) == 1 and len(_dop_lines[0].split()) >= 3,
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "01-01", "passed": passed, "score": score, "checks": checks}
