checks = [
    {"name": "все восемь линий верны для X и O", "passed": vse_linii_ok is True},
    {"name": "пустое поле — победителя нет", "passed": find_winner([""] * 9) == (None, None)},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
