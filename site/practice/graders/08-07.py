checks = [
    {"name": "name — получено через input()", "passed": isinstance(name, str) and len(name) > 0},
    {"name": "age_text — введено число возраста", "passed": age_text.strip().lstrip("-").isdigit()},
    {"name": "age == int(age_text)", "passed": age == int(age_text)},
    {"name": "message — приветствие построено из введённого имени", "passed": message == f"Привет, {name}!"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
