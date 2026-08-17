checks = [
    {"name": "d1 — calculate_discount(100, 10)", "passed": d1 == 90.0},
    {"name": "d2 — calculate_discount(200, 50)", "passed": d2 == 100.0},
    {"name": "calculate_discount — верна на новых аргументах", "passed": calculate_discount(50, 0) == 50},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
