# Доверенный грейдер для практики 01-01 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).

_cells = __cartesian__["cells"]  # noqa: F821 - injected by the trusted browser runner

_zadanie = _cells.get("3ca309a1", {})   # "Задание ★ Базовая практика" (имя, цвет, число)
_samost = _cells.get("e1a23aa4", {})    # "Самостоятельная практика" (рисунок из символов)
_dopolnitelnaya = _cells.get("ea50acd2", {})  # "Дополнительная задача ★★★" (один print(), три значения)
_variable_task = _cells.get("chapter01-variable-task", {})
_syntax_fix = _cells.get("chapter01-syntax-fix", {})

_zadanie_lines = [s for s in _zadanie.get("stdout", "").splitlines() if s.strip()]
_samost_lines = [s for s in _samost.get("stdout", "").splitlines() if s.strip()]
_dop_lines = [s for s in _dopolnitelnaya.get("stdout", "").splitlines() if s.strip()]
_variable_lines = [s for s in _variable_task.get("stdout", "").splitlines() if s.strip()]
_syntax_lines = [s for s in _syntax_fix.get("stdout", "").splitlines() if s.strip()]

checks = [
    {
        "name": "Задание ★: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
    {
        "name": "Задание ★: выведено минимум 3 строки (имя, цвет, число)",
        "passed": len(_zadanie_lines) >= 3,
    },
    {
        "name": "Самостоятельная практика: ячейка выполнена без ошибок",
        "passed": bool(_samost) and _samost.get("ok", False),
    },
    {
        "name": "Самостоятельная практика: что-то выведено на экран",
        "passed": len(_samost_lines) >= 1,
    },
    {
        "name": "Дополнительная задача ★★★: ячейка выполнена без ошибок",
        "passed": bool(_dopolnitelnaya) and _dopolnitelnaya.get("ok", False),
    },
    {
        "name": "Дополнительная задача ★★★: одна строка вывода с тремя значениями через print(a, b, c)",
        "passed": len(_dop_lines) == 1 and len(_dop_lines[0].split()) >= 3,
    },
    {
        "name": "Повторное присваивание: ячейка выполнена без ошибок",
        "passed": bool(_variable_task) and _variable_task.get("ok", False),
    },
    {
        "name": "Повторное присваивание: выведены два разных непустых значения",
        "passed": len(_variable_lines) == 2 and _variable_lines[0] != _variable_lines[1],
    },
    {
        "name": "Debug Lab: исправленная ячейка выполнена без ошибок",
        "passed": bool(_syntax_fix) and _syntax_fix.get("ok", False),
    },
    {
        "name": "Debug Lab: исправленная программа вывела ожидаемую строку",
        "passed": _syntax_lines == ["Python помогает читать ошибки"],
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "01-01", "passed": passed, "score": score, "checks": checks}
