checks = [
    {"name": "bounds_from_center(50, 50, 20)", "passed": bounds_from_center(50, 50, 20) == (30, 30, 70, 70)},
    {"name": "center_from_bounds — обратное преобразование", "passed": center_from_bounds(30, 30, 70, 70) == (50.0, 50.0)},
    {"name": "bounds_from_center(0, 0, 10)", "passed": bounds_from_center(0, 0, 10) == (-10, -10, 10, 10)},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
