_before = [(0, 0), (-20, 0)]
_after_paused, _status_paused = game_tick(list(_before), "paused", "right")
_after_running, _status_running = game_tick(list(_before), "running", "right")

checks = [
    {"name": "тик во время PAUSED не двигает змейку", "passed": _after_paused == _before},
    {"name": "статус PAUSED сохраняется", "passed": _status_paused == "paused"},
    {"name": "тик во время RUNNING двигает змейку", "passed": _after_running != _before},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
