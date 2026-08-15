checks = [
    {"name": "numbers[2:5] — средние три числа", "passed": numbers[2:5] == [3, 4, 5]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
