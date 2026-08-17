checks = [
    {"name": "w1.company — переопределён напрямую у экземпляра", "passed": w1.company == "Другая компания"},
    {"name": "w2.company — не затронут переопределением w1", "passed": w2.company == "Cartesian School"},
    {"name": "Rabotnik.company — атрибут класса не изменился", "passed": Rabotnik.company == "Cartesian School"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
