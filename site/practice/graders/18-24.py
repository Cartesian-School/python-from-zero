checks = [
    {"name": "Undo убирает ВЕСЬ штрих (3 отрезка), а не один", "passed": document == ["rect"]},
    {"name": "undo_stack содержит одно оставшееся действие", "passed": len(undo_stack) == 1},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
