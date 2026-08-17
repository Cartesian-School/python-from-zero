checks = [
    {"name": "operations — словарь с функциями double и square", "passed": callable(operations.get("double")) and callable(operations.get("square"))},
    {"name": "result_double — вызов функции из словаря", "passed": result_double == 10},
    {"name": "result_square — вызов функции из словаря", "passed": result_square == 25},
    {"name": "result_action — вызов через второе имя той же функции", "passed": result_action == 14},
    {"name": "action — то же самое, что и double", "passed": action is double},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
