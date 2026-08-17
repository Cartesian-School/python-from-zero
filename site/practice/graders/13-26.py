checks = [
    {"name": "f1 — celsius_to_fahrenheit(0)", "passed": f1 == 32},
    {"name": "f2 — celsius_to_fahrenheit(100)", "passed": f2 == 212},
    {"name": "c1 — fahrenheit_to_celsius(32)", "passed": c1 == 0},
    {"name": "miles — km_to_miles(10), округлено", "passed": miles == 6.21},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
