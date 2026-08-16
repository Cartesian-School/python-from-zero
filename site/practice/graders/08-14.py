checks = [
    {"name": "first3 — word[:3] == \"Car\"", "passed": first3 == "Car"},
    {"name": "last3 — word[-3:] == \"ian\"", "passed": last3 == "ian"},
    {"name": "every_second — word[::2] == \"Crein\"", "passed": every_second == "Crein"},
    {"name": "reversed_word — word[::-1] == \"naisetraC\"", "passed": reversed_word == "naisetraC"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
