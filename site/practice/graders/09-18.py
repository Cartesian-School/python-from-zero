checks = [
    {"name": "has_py — \"py\" in text", "passed": has_py is True},
    {"name": "is_yes — answer in группе допустимых значений", "passed": is_yes is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
