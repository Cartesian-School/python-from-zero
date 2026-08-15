checks = [
    {"name": "name, age — заданы для сравнения трёх способов", "passed": name == "Ада" and age == 28},
    {"name": "все три способа форматирования дали одинаковый текст", "passed": len({"%s — %d" % (name, age), "{} — {}".format(name, age), f"{name} — {age}"}) == 1},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
