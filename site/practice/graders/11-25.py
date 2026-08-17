checks = [
    {"name": "counts — правильная частота каждого слова", "passed": counts == {"python": 2, "is": 2, "great": 1, "and": 2, "fun": 1, "simple": 1}},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
