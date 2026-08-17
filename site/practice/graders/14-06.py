checks = [
    {"name": "s1.kurs — использовано значение по умолчанию", "passed": s1.kurs == 1},
    {"name": "s2.kurs — передано явно", "passed": s2.kurs == 3},
    {"name": "Student — свежий объект тоже использует умолчание", "passed": Student("Т").kurs == 1},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
