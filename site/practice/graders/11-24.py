checks = [
    {"name": "tovary — extend() вместо append() добавил элементы по отдельности", "passed": tovary == ["хлеб", "молоко", "яйца"]},
    {"name": "chisla — sort() не присвоен обратно в переменную", "passed": chisla == [1, 3, 4, 5]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
