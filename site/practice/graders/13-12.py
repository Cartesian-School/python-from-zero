checks = [
    {"name": "p1 — позиционный вызов с умолчанием city", "passed": p1 == "Anna, 25, Unknown"},
    {"name": "p2 — именованные аргументы в другом порядке", "passed": p2 == "Bob, 30, Warsaw"},
    {"name": "build_profile — верна на новых аргументах", "passed": build_profile("Li", 40) == "Li, 40, Unknown"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
