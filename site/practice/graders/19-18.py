import random as _random

_rng = _random.Random(3)
_snake = [(0, 0), (-20, 0), (-40, 0), (-60, 0)]
_food_ok = True
for _ in range(50):
    _food = choose_food(_snake, _rng, half=100)
    if _food in _snake:
        _food_ok = False
        break

_grown = move_snake(_snake, (20, 0), grow=True)
_shifted = move_snake(_snake, (20, 0), grow=False)

checks = [
    {"name": "еда никогда не попадает на змейку (50 попыток)", "passed": _food_ok},
    {"name": "move_snake с ростом увеличивает длину", "passed": len(_grown) == len(_snake) + 1},
    {"name": "move_snake без роста сохраняет длину", "passed": len(_shifted) == len(_snake)},
    {"name": "новая голова первая в списке", "passed": _shifted[0] == (20, 0)},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
