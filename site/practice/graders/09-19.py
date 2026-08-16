checks = [
    {"name": "is_none_check — value is None", "passed": is_none_check is True},
    {"name": "equals_check — value2 == 5", "passed": equals_check is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
