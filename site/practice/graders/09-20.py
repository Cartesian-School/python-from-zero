checks = [
    {"name": "result — password_ok=False выбирает вложенную ветку «Неверный пароль»", "passed": result == "Неверный пароль"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
