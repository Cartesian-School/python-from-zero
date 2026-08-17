checks = [
    {"name": "x — не изменился после add_one(x)", "passed": x == 10},
    {"name": "y — новое значение, возвращённое функцией", "passed": y == 11},
    {"name": "skills — мутирован через add_item(skills)", "passed": skills == ["Git", "Python"]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
