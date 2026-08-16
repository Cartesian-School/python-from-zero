checks = [
    {"name": "is_adult — age == 20", "passed": is_adult is True},
    {"name": "apple_before_banana — \"apple\" < \"banana\"", "passed": apple_before_banana is True},
    {"name": "same_case_insensitive — сравнение без учёта регистра", "passed": same_case_insensitive is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
