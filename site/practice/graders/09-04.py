checks = [
    {"name": "age — задан для проверки диапазона", "passed": age == 30},
    {"name": "условие 18 <= age <= 65 верно для заданного возраста", "passed": 18 <= age <= 65},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
