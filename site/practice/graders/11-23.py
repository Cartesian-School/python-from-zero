_norm = lambda s: str(s).strip().lower()
checks = [
    {"name": "otvet_1 — профиль «имя → email» это dict", "passed": _norm(otvet_1) == "dict"},
    {"name": "otvet_2 — уникальные ID без порядка это set", "passed": _norm(otvet_2) == "set"},
    {"name": "otvet_3 — неизменяемая координата это tuple", "passed": _norm(otvet_3) == "tuple"},
    {"name": "otvet_4 — список покупок, который меняем, это list", "passed": _norm(otvet_4) == "list"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
