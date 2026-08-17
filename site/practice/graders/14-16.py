checks = [
    {"name": "murka.klichka — настроено через super().__init__()", "passed": murka.klichka == "Мурка"},
    {"name": "murka.okras — настроено собственным __init__", "passed": murka.okras == "рыжий"},
    {"name": "Koshka — работает на новом объекте", "passed": Koshka("Соня", "чёрный").klichka == "Соня"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
