checks = [
    {"name": "ready -> running легален", "passed": can_transition("ready", "running") is True},
    {"name": "running -> paused легален", "passed": can_transition("running", "paused") is True},
    {"name": "paused -> running легален", "passed": can_transition("paused", "running") is True},
    {"name": "game_over -> ready легален", "passed": can_transition("game_over", "ready") is True},
    {"name": "paused -> game_over НЕ легален", "passed": can_transition("paused", "game_over") is False},
    {"name": "ready -> paused НЕ легален", "passed": can_transition("ready", "paused") is False},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
