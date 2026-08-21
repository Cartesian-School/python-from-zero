checks = [
    {"name": "вниз-вправо", "passed": normalize_bounds(10, 10, 100, 80) == (10, 10, 100, 80)},
    {"name": "вверх-влево", "passed": normalize_bounds(100, 80, 10, 10) == (10, 10, 100, 80)},
    {"name": "вниз-влево", "passed": normalize_bounds(100, 10, 10, 80) == (10, 10, 100, 80)},
    {"name": "вверх-вправо", "passed": normalize_bounds(10, 80, 100, 10) == (10, 10, 100, 80)},
    {"name": "вырожденная точка", "passed": normalize_bounds(50, 50, 50, 50) == (50, 50, 50, 50)},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
