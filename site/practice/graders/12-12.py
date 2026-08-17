checks = [
    {"name": "counts — правильная частота каждого слова", "passed": counts == {"python": 2, "is": 2, "great": 1, "and": 1, "fun": 1}},
    {"name": "samoe_chastoe — слово с максимальной частотой", "passed": samoe_chastoe == "python"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
