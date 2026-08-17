checks = [
    {"name": "score — все три ответа правильные", "passed": score == 3},
    {"name": "questions — список из трёх вопросов не тронут", "passed": len(questions) == 3},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
