checks = [
    {"name": "z1.spisok — содержит только свою запись", "passed": z1.spisok == ["Купить хлеб"]},
    {"name": "z2.spisok — не смешался с z1", "passed": z2.spisok == ["Позвонить маме"]},
    {"name": "Zametki — свежий объект начинается с пустого списка", "passed": Zametki().spisok == []},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
