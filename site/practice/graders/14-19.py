checks = [
    {"name": "poznakomit(Chelovek(...)) — вызывает предствавление человека", "passed": rezultat_chelovek == "Привет, я Боря!"},
    {"name": "poznakomit(Robot(...)) — вызывает представление робота", "passed": rezultat_robot == "БИП. Я робот номер 42."},
    {"name": "Chelovek и Robot не имеют общего родителя, кроме object", "passed": Chelovek.__bases__ == (object,) and Robot.__bases__ == (object,)},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
