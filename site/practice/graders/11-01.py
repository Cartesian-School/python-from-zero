checks = [
    {"name": "numbers[0] — первое число", "passed": numbers[0] == 7},
    {"name": "numbers[-1] — последнее число", "passed": numbers[-1] == 100},
    {"name": "numbers[-3] — третье с конца", "passed": numbers[-3] == 21},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
