checks = [
    {"name": "b — a + 3 == 8", "passed": b == 8},
    {"name": "c — b * 2 == 16", "passed": c == 16},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
