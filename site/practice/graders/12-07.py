checks = [
    {"name": "chisla — список из трёх введённых чисел", "passed": chisla == [10.0, 20.0, 30.0]},
    {"name": "minimum", "passed": minimum == 10.0},
    {"name": "maksimum", "passed": maksimum == 30.0},
    {"name": "summa", "passed": summa == 60.0},
    {"name": "average", "passed": average == 20.0},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
