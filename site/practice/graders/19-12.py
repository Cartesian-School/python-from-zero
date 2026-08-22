_no_food = tick_order((20, 0), (100, 100), [(0, 0), (-20, 0)])
_with_food = tick_order((20, 0), (20, 0), [(0, 0), (-20, 0)])
checks = [
    {"name": "без еды: grow=False", "passed": _no_food[1] is False},
    {"name": "без еды: длина не растёт", "passed": len(_no_food[0]) == 2},
    {"name": "с едой: grow=True", "passed": _with_food[1] is True},
    {"name": "с едой: длина растёт", "passed": len(_with_food[0]) == 3},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
