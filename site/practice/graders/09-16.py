checks = [
    {"name": "can_walk — not is_raining", "passed": can_walk is True},
    {"name": "double_negative — not not True", "passed": double_negative is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
