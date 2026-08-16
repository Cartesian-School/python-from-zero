checks = [
    {"name": "is_equal_before — password с пробелом не равен \"секрет\"", "passed": is_equal_before is False},
    {"name": "cleaned — password.strip() убрал пробел", "passed": cleaned == "секрет"},
    {"name": "is_equal_after — после strip() строки равны", "passed": is_equal_after is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
