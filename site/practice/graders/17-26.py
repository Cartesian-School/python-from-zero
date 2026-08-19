checks = [
    {"name": "победа X учтена", "passed": scores2["x"] == 1},
    {"name": "победа O учтена", "passed": scores2["o"] == 1},
    {"name": "ничья учтена", "passed": scores2["draws"] == 1},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
