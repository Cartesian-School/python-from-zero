checks = [
    {"name": "tests_passed — все три assert прошли", "passed": tests_passed is True},
    {"name": "classify_score — верна на границе (90)", "passed": classify_score(90) == "отлично"},
    {"name": "classify_score — верна на границе (70)", "passed": classify_score(70) == "хорошо"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
