_score1, _delay1 = eat_food(40, 140)
_score2, _delay2 = eat_food(999_990, 60)

checks = [
    {"name": "score увеличивается на food_score", "passed": _score1 == 50},
    {"name": "delay пересчитан после еды", "passed": _delay1 == 130},
    {"name": "delay не опускается ниже минимума", "passed": _delay2 == 60},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
