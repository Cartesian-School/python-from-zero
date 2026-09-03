def _grader_mutant(head, half=280):
    """Сломанная версия, о которой ученик не знает: граница исключена."""
    x, y = head
    return abs(x) >= half or abs(y) >= half


def _grader_reference(head, half=280):
    x, y = head
    return abs(x) > half or abs(y) > half


checks = [
    {"name": "правильная версия безопасна на границе", "passed": test_boundary_is_safe(is_wall_collision) is True},
    {"name": "тест ловит сломанную версию (>=)", "passed": test_boundary_is_safe(is_wall_collision_BROKEN) is False},
    {"name": "тест принимает эталонную реализацию проверяющего",
     "passed": test_boundary_is_safe(_grader_reference) is True},
    {"name": "тест ловит скрытую сломанную версию проверяющего",
     "passed": test_boundary_is_safe(_grader_mutant) is False},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
