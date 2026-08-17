checks = [
    {"name": "result — a() → b() → c() вернули верную сумму", "passed": result == 5},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
