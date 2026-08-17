checks = [
    {"name": "average — средний балл", "passed": average == 81.5},
    {"name": "maksimum", "passed": maksimum == 95},
    {"name": "minimum", "passed": minimum == 58},
    {"name": "otlichniki — ученики с баллом >= 90", "passed": len(otlichniki) == 2},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
