checks = [
    {"name": "history — все команды записаны в порядке ввода", "passed": history == ["help", "hello", "status", "exit"]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
