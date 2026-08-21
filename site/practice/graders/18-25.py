checks = [
    {"name": "документ после A, C (redo B не применялся)", "passed": document == ["A", "C"]},
    {"name": "новое действие очищает redo_stack", "passed": redo_stack == []},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
