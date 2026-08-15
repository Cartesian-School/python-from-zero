checks = [
    {"name": "age — исправленная версия (без IndentationError) выполнена", "passed": age == 20},
    {"name": "number — задание на чётность выполнено", "passed": number == 17},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
