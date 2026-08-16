checks = [
    {"name": "summa — сентинел-цикл суммировал числа до 'stop'", "passed": summa == 15},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
