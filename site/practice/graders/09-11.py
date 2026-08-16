checks = [
    {"name": "is_none — value is None", "passed": is_none is True},
    {"name": "truthy_check — bool(\"False\") is True", "passed": truthy_check is True},
    {"name": "falsy_check — bool(0) is False", "passed": falsy_check is False},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
