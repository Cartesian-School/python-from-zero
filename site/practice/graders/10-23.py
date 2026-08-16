_norm = lambda s: str(s).strip().lower()
checks = [
    {"name": "otvet_1 — 4 стороны квадрата: число повторов известно заранее", "passed": _norm(otvet_1) == "for"},
    {"name": "otvet_2 — пока не угадает: число повторов заранее неизвестно", "passed": _norm(otvet_2) == "while"},
    {"name": "otvet_3 — перебор букв слова", "passed": _norm(otvet_3) == "for"},
    {"name": "otvet_4 — условие остановки в середине тела", "passed": _norm(otvet_4) == "while true"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
