checks = [
    {"name": "spisok_s_nomerami — нумерация с 1 через enumerate()", "passed": spisok_s_nomerami == ["1: хлеб", "2: молоко", "3: яйца", "4: сыр"]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
