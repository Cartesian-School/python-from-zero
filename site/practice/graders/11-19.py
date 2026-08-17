checks = [
    {"name": "missing — required - available", "passed": missing == {"sql"}},
    {"name": "common — required & available", "passed": common == {"python", "git"}},
    {"name": "vse — required | available", "passed": vse == {"python", "git", "sql", "docker"}},
    {"name": "podmnozhestvo — {python, git} является подмножеством available", "passed": podmnozhestvo is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
