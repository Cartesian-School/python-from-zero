checks = [
    {"name": "move_snake — чистая логика", "passed": is_pure_logic("move_snake") is True},
    {"name": "is_wall_collision — чистая логика", "passed": is_pure_logic("is_wall_collision") is True},
    {"name": "render требует экран", "passed": is_pure_logic("render") is False},
    {"name": "bind_keys требует экран", "passed": is_pure_logic("bind_keys") is False},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
