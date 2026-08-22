checks = [
    {"name": "(280, 280) безопасна — граница включена", "passed": is_wall_collision((280, 280)) is False},
    {"name": "(-280, -280) безопасна", "passed": is_wall_collision((-280, -280)) is False},
    {"name": "(300, 0) — столкновение", "passed": is_wall_collision((300, 0)) is True},
    {"name": "(0, -281) — столкновение", "passed": is_wall_collision((0, -281)) is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
