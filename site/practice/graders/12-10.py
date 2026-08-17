checks = [
    {"name": "pobeda — игра выиграна в пределах лимита попыток", "passed": pobeda is True},
    {"name": "attempts — не превышает max_attempts", "passed": attempts == 3 and attempts <= max_attempts},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
