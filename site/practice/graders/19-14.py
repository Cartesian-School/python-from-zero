checks = [
    {"name": "score=0 -> 140", "passed": calculate_delay(0) == 140},
    {"name": "score=50 -> 130", "passed": calculate_delay(50) == 130},
    {"name": "score=100 -> 120", "passed": calculate_delay(100) == 120},
    {"name": "очень большой счёт не опускается ниже 60", "passed": calculate_delay(100_000) == 60},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
