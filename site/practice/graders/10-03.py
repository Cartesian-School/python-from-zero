checks = [
    {"name": "count — число гласных букв в слове посчитано верно", "passed": count == sum(1 for L in word if L in glasnye)},
    {"name": "count — правдоподобное значение (не ноль)", "passed": count > 0},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
