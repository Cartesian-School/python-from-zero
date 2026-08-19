checks = [
    {"name": "s1.board[0] изменён", "passed": s1.board[0] == "X"},
    {"name": "s2.board не затронут (default_factory)", "passed": s2.board[0] == ""},
    {"name": "оба экземпляра начинают с current_player='X'", "passed": s1.current_player == "X" and s2.current_player == "X"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
