checks = [
    {"name": "ok1 — пустая строка не проходит валидацию", "passed": ok1 is False},
    {"name": "ok2 — нечисловой текст не проходит валидацию", "passed": ok2 is False},
    {"name": "ok3 — отрицательное число не проходит валидацию", "passed": ok3 is False},
    {"name": "ok4/msg4 — корректное число проходит без сообщения об ошибке", "passed": ok4 is True and msg4 == ""},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
