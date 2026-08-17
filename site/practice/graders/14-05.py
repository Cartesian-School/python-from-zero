checks = [
    {"name": "kot.myaukat() — верная строка", "passed": kot.myaukat() == "Барсик: Мяу!"},
    {"name": "Kot.myaukat(kot) — то же самое, что и kot.myaukat()", "passed": Kot.myaukat(kot) == kot.myaukat()},
    {"name": "Kot — работает и со свежим объектом", "passed": Kot("Мурзик").myaukat() == "Мурзик: Мяу!"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
