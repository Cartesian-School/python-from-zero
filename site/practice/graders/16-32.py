checks = [
    {"name": "check_sleep — time.sleep признан небезопасным для callback", "passed": check_sleep is False},
    {"name": "check_after — root.after признан безопасным для callback", "passed": check_after is True},
    {"name": "check_while — цикл-опрос while True признан небезопасным", "passed": check_while is False},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
