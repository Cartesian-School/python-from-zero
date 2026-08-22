checks = [
    {"name": "up", "passed": next_head((0, 0), "up") == (0, 20)},
    {"name": "down", "passed": next_head((0, 0), "down") == (0, -20)},
    {"name": "left", "passed": next_head((0, 0), "left") == (-20, 0)},
    {"name": "right со смещённой головой", "passed": next_head((100, 100), "right") == (120, 100)},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
