checks = [
    {"name": "Avtomobil.opisanie() — обращается к вложенному Motor", "passed": mashina.opisanie() == "Автомобиль с двигателем 150 л.с."},
    {"name": "Avtomobil.start() — делегирует Motor.start()", "passed": mashina.start() == "Двигатель мощностью 150 л.с. запущен"},
    {"name": "композиция работает на новом объекте", "passed": Avtomobil(90).opisanie() == "Автомобиль с двигателем 90 л.с."},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
