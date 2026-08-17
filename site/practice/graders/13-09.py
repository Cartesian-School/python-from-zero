checks = [
    {"name": "summa_kvadratov — верна на новых аргументах", "passed": summa_kvadratov(1, 2) == 5},
    {"name": "kvadrat_summy — верна на новых аргументах", "passed": kvadrat_summy(1, 2) == 9},
    {"name": "raznost — разница между kvadrat_summy(3,4) и summa_kvadratov(3,4)", "passed": raznost == 24},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
