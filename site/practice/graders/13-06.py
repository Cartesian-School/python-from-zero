checks = [
    {"name": "is_even — лямбда верно определяет чётность", "passed": is_even(4) is True and is_even(3) is False},
    {"name": "chetnye — filter() с лямбдой дал верный результат", "passed": chetnye == [2, 4, 6, 8]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
