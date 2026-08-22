checks = [
    {"name": "столкновение со стеной -> game_over", "passed": resolve_tick((0, 0), "running", wall_hit=True, self_hit=False) == "game_over"},
    {"name": "самостолкновение -> game_over", "passed": resolve_tick((0, 0), "running", wall_hit=False, self_hit=True) == "game_over"},
    {"name": "без столкновений статус не меняется", "passed": resolve_tick((0, 0), "running", wall_hit=False, self_hit=False) == "running"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
