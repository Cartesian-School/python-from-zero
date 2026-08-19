checks = [
    {"name": "board — список из 9 пустых строк", "passed": len(state["board"]) == 9 and all(c == "" for c in state["board"])},
    {"name": "current_player — 'X' в начале", "passed": state["current_player"] == "X"},
    {"name": "game_over — False в начале", "passed": state["game_over"] is False},
    {"name": "winner — None в начале", "passed": state.get("winner") is None},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
