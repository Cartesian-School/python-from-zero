checks = [
    {"name": "club_access — age>=18 and has_ticket, введено «20»/«да»", "passed": club_access is True},
    {"name": "advice — холодно и дождь -> «тёплая куртка и зонт»", "passed": advice == "тёплая куртка и зонт"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
