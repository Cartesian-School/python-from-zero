checks = [
    {"name": "a — введено и преобразовано через float(input())", "passed": isinstance(a, float)},
    {"name": "b — введено и преобразовано через float(input())", "passed": isinstance(b, float)},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
