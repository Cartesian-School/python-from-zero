checks = [
    {"name": "numbers — append/sort/reverse применены верно", "passed": numbers == [4, 3, 2, 1]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
