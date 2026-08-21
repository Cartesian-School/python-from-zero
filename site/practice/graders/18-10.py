checks = [
    {"name": "shapes_by_id[3] == 'rectangle'", "passed": shapes_by_id.get(3) == "rectangle"},
    {"name": "shapes_by_id[7] == 'oval'", "passed": shapes_by_id.get(7) == "oval"},
    {"name": "5 не зарегистрирован", "passed": 5 not in shapes_by_id},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
