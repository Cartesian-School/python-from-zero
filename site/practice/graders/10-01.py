checks = [
    {"name": "total — сумма чисел от 1 до 100 через цикл", "passed": total == 5050},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
