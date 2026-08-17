checks = [
    {"name": "total — итоговая сумма чека", "passed": abs(total - 21.10) < 1e-9},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
