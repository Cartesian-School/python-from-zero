checks = [
    {"name": "x не изменился — y была настоящей копией", "passed": x == [10, 20]},
    {"name": "y содержит добавленное значение", "passed": y == [10, 20, 30]},
    {"name": "z == y — одинаковое содержимое", "passed": ravny is True},
    {"name": "z is y — но это РАЗНЫЕ объекты", "passed": odin_i_tot_zhe is False},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
