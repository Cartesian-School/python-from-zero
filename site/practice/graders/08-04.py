checks = [
    {"name": "word.startswith(\"Car\")", "passed": word.startswith("Car") is True},
    {"name": "word.endswith(\"an\")", "passed": word.endswith("an") is True},
    {"name": "count — слов длиннее 4 букв в предложении", "passed": count == 7},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
