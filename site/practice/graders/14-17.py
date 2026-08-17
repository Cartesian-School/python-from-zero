checks = [
    {"name": "Koshka.zvuk() — расширяет родительский метод через super()", "passed": Koshka().zvuk() == "Животное подаёт голос: Мяу!"},
    {"name": "Sobaka.zvuk() — родительское поведение не потеряно", "passed": Sobaka().zvuk() == "Животное подаёт голос: Гав!"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
