checks = [
    {"name": "poluchit_balans() — 100 + 50 - 30", "passed": schet.poluchit_balans() == 120},
    {"name": "snyat(30) — успешно, средств достаточно", "passed": uspeshno is True},
    {"name": "snyat(9999) — отклонено, средств не хватает", "passed": neuspeshno is False},
    {"name": "Konto — свежий счёт не даёт снять больше баланса", "passed": Konto(10).snyat(20) is False},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
