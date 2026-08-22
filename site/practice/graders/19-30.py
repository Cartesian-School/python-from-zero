checks = [
    {"name": "правильная версия безопасна на границе", "passed": test_boundary_is_safe(is_wall_collision) is True},
    {"name": "тест ловит сломанную версию (>=)", "passed": test_boundary_is_safe(is_wall_collision_BROKEN) is False},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
