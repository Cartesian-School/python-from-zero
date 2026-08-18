checks = [
    {"name": "result — calculate_tip() верно делит чаевые между людьми", "passed": result == 75.0},
    {"name": "values — lambda i=i зафиксировала каждое значение i отдельно", "passed": values == [0, 1, 2]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
