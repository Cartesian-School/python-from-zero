checks = [
    {"name": "ход по клетке — command", "passed": vybor_hod_po_kletke == "command"},
    {"name": "hover-эффект — bind", "passed": vybor_hover_effekt == "bind"},
    {"name": "клавиши 1-9 — bind", "passed": vybor_klavishi_1_9 == "bind"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
