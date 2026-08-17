checks = [
    {"name": "is_square — True для равных сторон", "passed": kvadrat.is_square is True},
    {"name": "is_square — False для разных сторон", "passed": ne_kvadrat.is_square is False},
    {"name": "Rectangle — area и perimeter верны на новом объекте", "passed": Rectangle(10, 4).area == 40 and Rectangle(10, 4).perimeter == 28},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
