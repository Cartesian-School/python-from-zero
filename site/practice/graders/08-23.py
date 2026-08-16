checks = [
    {"name": "total — количество слов == 5", "passed": total == 5},
    {"name": "schetchik — правильный подсчёт повторов слов", "passed": schetchik == {"кот": 2, "и": 2, "пёс": 1}},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
