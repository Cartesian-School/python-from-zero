checks = [
    {"name": "in_range — 18 <= 30 <= 65", "passed": in_range is True},
    {"name": "valid_score — 0 <= 105 <= 100 (за пределами диапазона)", "passed": valid_score is False},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
