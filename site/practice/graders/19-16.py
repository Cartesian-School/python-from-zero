_snake = [(0, 0), (-20, 0), (-40, 0)]
checks = [
    {"name": "head_of возвращает snake[0]", "passed": head_of(_snake) == (0, 0)},
    {"name": "body_of возвращает snake[1:]", "passed": body_of(_snake) == [(-20, 0), (-40, 0)]},
    {"name": "body_of на змейке из одного сегмента пуст", "passed": body_of([(0, 0)]) == []},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
