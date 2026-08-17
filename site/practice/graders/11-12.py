checks = [
    {"name": "temperatures[2] исправлен на 23", "passed": temperatures[2] == 23},
    {"name": "остальные значения не тронуты", "passed": temperatures == [18, 21, 23, 25, 17]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
