checks = [
    {"name": "document очищен", "passed": document == []},
    {"name": "undo_stack очищен вместе с документом", "passed": undo_stack == []},
    {"name": "redo_stack очищен вместе с документом", "passed": redo_stack == []},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
