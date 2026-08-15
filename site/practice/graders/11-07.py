checks = [
    {"name": "common — пересечение двух групп через множества", "passed": common == {"Вера", "Гриша"}},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
