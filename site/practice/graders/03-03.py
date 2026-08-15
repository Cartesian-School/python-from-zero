# Доверенный грейдер для практики 03-03 (не редактируется учеником).
#
# Выполняется в ТОЙ ЖЕ Python-сессии, что и ячейки ноутбука, поэтому видит
# реальный результат работы кода ученика через __cartesian__["cells"][cell_id]
# (заполняется раннером в site/assets/js/python-worker.mjs при каждом запуске ячейки).
#
# У этого ноутбука есть собственная ячейка самопроверки "Проверка результата"
# (id 00aad64d, assert 3.5 * 60 == 210.0) — используем её как основной сигнал:
# если assert не упал, ячейка выполнилась без ошибок и напечатала подтверждение.

_cells = __cartesian__["cells"]

_zadanie = _cells.get("42f4b88d", {})   # "Задание ★ Базовая практика"
_proverka = _cells.get("00aad64d", {})  # "Проверка результата" (со своим assert)

checks = [
    {
        "name": "Задание ★: ячейка выполнена без ошибок",
        "passed": bool(_zadanie) and _zadanie.get("ok", False),
    },
    {
        "name": "Задание ★: выведен числовой результат",
        "passed": bool(_zadanie.get("stdout", "").strip()),
    },
    {
        "name": "Проверка результата: assert пройден (210.0 минут)",
        "passed": bool(_proverka)
        and _proverka.get("ok", False)
        and "Проверка пройдена" in _proverka.get("stdout", ""),
    },
]

_passed_count = sum(1 for c in checks if c["passed"])
passed = _passed_count == len(checks)
score = round(100 * _passed_count / len(checks))

{"lesson_id": "03-03", "passed": passed, "score": score, "checks": checks}
