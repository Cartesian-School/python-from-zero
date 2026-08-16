checks = [
    {"name": "age_ok — age >= 18 отдельно от eligible", "passed": age_ok is True},
    {"name": "eligible — age_ok and has_ticket, has_ticket=False", "passed": eligible is False},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
