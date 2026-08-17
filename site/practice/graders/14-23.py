checks = [
    {"name": "k1.tovary — содержит только свой товар", "passed": k1.tovary == ["Хлеб"]},
    {"name": "k2.tovary — не затронут добавлением в k1", "passed": k2.tovary == []},
    {"name": "k3.tovary — тоже независим", "passed": k3.tovary == ["Молоко"]},
    {"name": "Korzina — свежий объект всегда начинается с пустого списка", "passed": Korzina().tovary == []},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
