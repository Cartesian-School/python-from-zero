checks = [
    {"name": "s1 — sign(-5) покрывает отрицательный путь", "passed": s1 == "negative"},
    {"name": "s2 — sign(0) покрывает нулевой путь", "passed": s2 == "zero"},
    {"name": "c1 — contains_even находит чётное в списке", "passed": c1 is True},
    {"name": "c2 — contains_even верно возвращает False, если чётных нет", "passed": c2 is False},
    {"name": "sign — верна на новом положительном входе", "passed": sign(7) == "positive"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
