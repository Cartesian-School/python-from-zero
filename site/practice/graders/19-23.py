_state = {"snake": [(0, 0), (-20, 0), (-40, 0)], "score": 40, "high_score": 40, "status": "game_over"}
_new_state, _new_generation = restart(_state, generation=3)

checks = [
    {"name": "snake сброшен к одной клетке", "passed": _new_state["snake"] == [(0, 0)]},
    {"name": "score обнулён", "passed": _new_state["score"] == 0},
    {"name": "high_score пережил рестарт", "passed": _new_state["high_score"] == 40},
    {"name": "generation увеличился", "passed": _new_generation == 4},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
