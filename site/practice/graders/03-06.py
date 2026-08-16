# Доверенный грейдер для практики 03-06 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]

_exp1 = _cells.get("8023e03b", {})    # "Эксперимент 1" — input() + print(name)
_zadanie = _cells.get("ac9b3f31", {})  # "Задание ★ Базовая практика"

_exp1_out = _exp1.get("stdout", "")
_zadanie_out = _zadanie.get("stdout", "")

checks = [
    {
        "name": "Эксперимент 1: ячейка выполнена без ошибок",
        "passed": bool(_exp1) and _exp1.get("ok", False),
    },
    {
        "name": "Эксперимент 1: в выводе есть слово «Привет»",
        "passed": "Привет" in _exp1_out,
    },
    {
        "name": "Задание ★: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
    {
        "name": "Задание ★: приветствие содержит «Рады знакомству»",
        "passed": "Рады знакомству" in _zadanie_out,
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "03-06", "passed": passed, "score": score, "checks": checks}
