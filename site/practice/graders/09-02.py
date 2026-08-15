checks = [
    {"name": "age — присвоено верно после исправления == вместо =", "passed": age == 20},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
