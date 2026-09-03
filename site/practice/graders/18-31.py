# Два бага истории из справочника Debug Labs (раздел 18.31):
# Lab 11 — очистка холста обязана обнулить историю вместе с документом;
# Lab 10 — новое действие обязано обнулить ветку redo.
checks = [
    {"name": "Lab 11: document очищен", "passed": document == []},
    {"name": "Lab 11: undo_stack очищен вместе с документом", "passed": undo_stack == []},
    {"name": "Lab 11: redo_stack очищен вместе с документом", "passed": redo_stack == []},
    {"name": "Lab 10: документ после A, undo(B), C", "passed": doc2 == ["A", "C"]},
    {"name": "Lab 10: новое действие обнулило redo", "passed": redo2 == []},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
