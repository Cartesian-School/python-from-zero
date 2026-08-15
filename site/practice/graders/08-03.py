checks = [
    {"name": "word[:3] — первые три символа «Cartesian»", "passed": word[:3] == "Car"},
    {"name": "word[-3:] — последние три символа «Cartesian»", "passed": word[-3:] == "ian"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
