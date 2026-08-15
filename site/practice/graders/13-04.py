checks = [
    {"name": "srednee(*chisla) — верно на новых аргументах", "passed": srednee(2, 4, 6) == 4.0},
    {"name": "srednee — работает с одним аргументом", "passed": srednee(10) == 10.0},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
