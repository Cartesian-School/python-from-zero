checks = [
    {"name": "full_name — «Ада Лавлейс», приведено к аккуратному виду", "passed": full_name == "Ада Лавлейс"},
    {"name": "initials — «А. Л.»", "passed": initials == "А. Л."},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
