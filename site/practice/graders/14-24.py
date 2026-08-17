checks = [
    {"name": "Zakaz.summa() — цена товара × количество", "passed": zakaz.summa() == 300},
    {"name": "Tovar — dataclass сравнивает по значению", "passed": Tovar("А", 10) == Tovar("А", 10)},
    {"name": "Tovar.so_skidkoj — верно применяет скидку", "passed": abs(knigi.so_skidkoj(10) - 531.0) < 0.01},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
