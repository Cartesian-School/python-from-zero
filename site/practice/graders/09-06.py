checks = [
    {"name": "bukva — соответствует последней оценке в цикле (40 -> D)", "passed": bukva == "D"},
    {"name": "has_license — задано для проверки вложенных условий", "passed": has_license is True},
    {"name": "has_fuel — третий уровень вложенности добавлен", "passed": has_fuel is False},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
