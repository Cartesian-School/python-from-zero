checks = [
    {"name": "последний ход находит победителя X", "passed": winner == "X"},
    {"name": "выигрышная линия — диагональ 0-4-8", "passed": set(line) == {0, 4, 8}},
    {"name": "победа НЕ считается ничьей", "passed": is_draw(poslednij_hod_pobeda) is False},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
