checks = [
    {"name": "can_enter — age >= 18 and has_ticket", "passed": can_enter is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
