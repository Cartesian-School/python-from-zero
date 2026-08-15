checks = [
    {"name": "r, g, b — кортеж RGB распакован верно", "passed": r == 255 and g == 0 and b == 128},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
