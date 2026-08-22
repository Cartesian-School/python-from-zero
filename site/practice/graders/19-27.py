_a = GameState(snake=[(0, 0)], score=10)
_b = GameState(snake=[(0, 0)], score=10)
_c = replace(_a, status="running")

checks = [
    {"name": "два одинаковых GameState равны", "passed": _a == _b},
    {"name": "replace() меняет только указанное поле", "passed": _c.status == "running" and _c.score == 10},
    {"name": "replace() не мутирует исходный объект", "passed": _a.status == "ready"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
