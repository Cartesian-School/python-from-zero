checks = [
    {"name": "result — temperature=10 попадает в «прохладно»", "passed": result == "прохладно"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
