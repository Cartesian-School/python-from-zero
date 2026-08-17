checks = [
    {"name": "result — nonlocal count накопил три вызова inner()", "passed": result == 3},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
