checks = [
    {"name": "a1, a2 — return-версия функции вычислена верно", "passed": a1 == 15 and a2 == 100},
    {"name": "plosch_pryamougolnika(6, 7) — работает на новых аргументах", "passed": plosch_pryamougolnika(6, 7) == 42},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
