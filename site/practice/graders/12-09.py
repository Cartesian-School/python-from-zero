checks = [
    {"name": "guess — совпадает с secret в конце игры", "passed": guess == secret},
    {"name": "attempts — верное число попыток", "passed": attempts == 3},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
