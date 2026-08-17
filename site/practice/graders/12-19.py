checks = [
    {"name": "has_digit — обнаружена цифра", "passed": has_digit is True},
    {"name": "has_letter — обнаружена буква", "passed": has_letter is True},
    {"name": "has_space — пробелов нет", "passed": has_space is False},
    {"name": "podhodit — пароль соответствует учебным правилам", "passed": podhodit is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
