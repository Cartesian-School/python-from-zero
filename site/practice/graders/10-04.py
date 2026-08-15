checks = [
    {"name": "number — первое число, делящееся на 3 и на 7 (найдено через break)", "passed": number == 21},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
