checks = [
    {"name": "tablica — таблица умножения 5x5 построена верно", "passed": tablica == [[a * b for b in range(1, 6)] for a in range(1, 6)]},
    {"name": "tablica[4][4] — последний элемент равен 25", "passed": tablica[4][4] == 25},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
