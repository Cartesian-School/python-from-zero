checks = [
    {"name": "cart — правильный итоговый список", "passed": cart == ["вода", "хлеб", "молоко", "яйца", "сыр", "масло"]},
    {"name": "insert() поставил 'вода' в начало", "passed": cart[0] == "вода"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
