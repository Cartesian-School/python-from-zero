checks = [
    {"name": "itogo_iteracij — 3 строки × 7 столбцов = 21 итерация", "passed": itogo_iteracij == 21},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
