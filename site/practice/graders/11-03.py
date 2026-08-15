checks = [
    {"name": "numbers — отсортированы и развёрнуты", "passed": numbers == [9, 8, 5, 2, 1]},
    {"name": "fruits, last — insert/remove/pop выполнены верно", "passed": fruits == ["манго", "яблоко"] and last == "вишня"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
