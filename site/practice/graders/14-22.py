checks = [
    {"name": "rasstoyanie_do — верное евклидово расстояние (0,0)→(3,4)", "passed": abs(rasstoyanie - 5.0) < 0.001},
    {"name": "__str__ — форматирует точку верно", "passed": str(Tochka(1, 2)) == "(1, 2)"},
    {"name": "__eq__ — сравнивает по координатам", "passed": Tochka(1, 2) == Tochka(1, 2) and Tochka(1, 2) != Tochka(5, 5)},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
