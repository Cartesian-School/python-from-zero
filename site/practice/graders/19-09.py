checks = [
    {"name": "(0, 0) на сетке", "passed": is_on_grid(0, 0) is True},
    {"name": "(-280, 280) на сетке", "passed": is_on_grid(-280, 280) is True},
    {"name": "(21, 0) не на сетке", "passed": is_on_grid(21, 0) is False},
    {"name": "(0, -5) не на сетке", "passed": is_on_grid(0, -5) is False},
    {"name": "(40, -60) на сетке", "passed": is_on_grid(40, -60) is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
