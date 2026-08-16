checks = [
    {"name": "can_rest — is_weekend or is_holiday", "passed": can_rest is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
