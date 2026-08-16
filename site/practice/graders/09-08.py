checks = [
    {"name": "action — верная ветка для is_raining=True", "passed": action == "взять зонт"},
    {"name": "has_branch — программа содержит ветвление", "passed": has_branch is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
