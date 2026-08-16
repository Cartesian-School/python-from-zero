checks = [
    {"name": "r1 — s1.isalpha() is True", "passed": r1 is True},
    {"name": "r2 — s2.isdigit() is True", "passed": r2 is True},
    {"name": "r3 — s3.isspace() is True", "passed": r3 is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
