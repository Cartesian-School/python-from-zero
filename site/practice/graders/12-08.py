checks = [
    {"name": "score — счётчик инициализирован до цикла, а не внутри", "passed": score == 2},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
