checks = [
    {"name": "diapazon — числа от 5 до 15 включительно", "passed": diapazon == list(range(5, 16))},
    {"name": "ubyvanie — чётные числа от 20 до 2 включительно, по убыванию", "passed": ubyvanie == list(range(20, 1, -2))},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
