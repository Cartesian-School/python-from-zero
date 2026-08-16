# Доверенный грейдер для практики 03-10 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_exp1 = _cells.get("0596f469", {})     # "Эксперимент 1" — визитка через input()
_zadanie = _cells.get("d0f40013", {})  # "Задание ★ Базовая практика" — 4-я строка

_exp1_out = _exp1.get("stdout", "")
_zadanie_out = _zadanie.get("stdout", "")

checks = [
    {
        "name": "Эксперимент 1: ячейка выполнена без ошибок",
        "passed": bool(_exp1) and _exp1.get("ok", False),
    },
    {
        "name": "Эксперимент 1: визитка содержит рамку и «Имя:»",
        "passed": "====" in _exp1_out and "Имя:" in _exp1_out,
    },
    {
        "name": "Задание ★: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
    {
        "name": "Задание ★: добавлена четвёртая строка визитки",
        "passed": len([s for s in _zadanie_out.splitlines() if s.strip()]) >= 6,
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "03-10", "passed": passed, "score": score, "checks": checks}
