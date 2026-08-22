checks = [
    {"name": "(40, 60) -> (2, 3)", "passed": pixel_to_cell(40, 60) == (2, 3)},
    {"name": "(-10, 0) -> (-1, 0)", "passed": pixel_to_cell(-10, 0) == (-1, 0)},
    {"name": "(-20, 0) -> (-1, 0)", "passed": pixel_to_cell(-20, 0) == (-1, 0)},
    {"name": "(-21, 0) -> (-2, 0)", "passed": pixel_to_cell(-21, 0) == (-2, 0)},
    {"name": "(0, 0) -> (0, 0)", "passed": pixel_to_cell(0, 0) == (0, 0)},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
