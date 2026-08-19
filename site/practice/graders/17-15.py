checks = [
    {"name": "занятая клетка — moved2 is False", "passed": moved2 is False},
    {"name": "невалидный ход не переключает игрока", "passed": player2 == "O"},
    {"name": "невалидный ход не меняет поле", "passed": board2 == board_occupied},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
