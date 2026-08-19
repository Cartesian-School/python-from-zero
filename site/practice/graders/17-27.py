checks = [
    {"name": "New Round сохраняет счёт", "passed": after_round["score_x"] == 3 and after_round["score_o"] == 1},
    {"name": "New Match обнуляет счёт", "passed": after_match["score_x"] == 0 and after_match["score_o"] == 0},
    {"name": "счёт сохранён и прочитан из JSON", "passed": loaded == {"x": 3, "o": 1, "draws": 0}},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
