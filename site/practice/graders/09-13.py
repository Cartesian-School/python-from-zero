checks = [
    {"name": "warm_triggered — temperature > 20", "passed": warm_triggered is True},
    {"name": "hot_triggered — temperature > 25", "passed": hot_triggered is True},
    {"name": "both_triggered — оба независимых if сработали бы одновременно", "passed": both_triggered is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
