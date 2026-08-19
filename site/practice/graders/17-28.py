checks = [
    {"name": "все 8 линий верны для обоих игроков", "passed": all_lines_ok is True},
    {"name": "известная ничья определена верно", "passed": draw_ok is True},
    {"name": "последний ход побеждает, не заканчивается ничьей", "passed": last_move_ok is True},
    {"name": "пустое поле — без победителя", "passed": empty_ok is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
