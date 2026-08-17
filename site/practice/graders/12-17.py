checks = [
    {"name": "score — два верных ответа из трёх", "passed": score == 2},
    {"name": "procent — доля правильных ответов", "passed": abs(procent - (2 / 3 * 100)) < 1e-6},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
