checks = [
    {"name": "is_sunny — True типа bool", "passed": is_sunny is True and isinstance(is_sunny, bool)},
    {"name": "цикл проверки истинности дошёл до конца (value == \"0\")", "passed": value == "0"},
    {"name": "bool(\"0\") — неочевидный случай: непустая строка это True", "passed": bool(value) is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
