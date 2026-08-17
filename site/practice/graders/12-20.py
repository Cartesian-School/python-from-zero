checks = [
    {"name": "ugol_1 — угол для 5 сторон", "passed": ugol_1 == 72.0},
    {"name": "ugol_2 — угол для 8 сторон", "passed": ugol_2 == 45.0},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
