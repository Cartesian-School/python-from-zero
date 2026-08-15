checks = [
    {"name": "zagadannoe — случайное число в диапазоне 1..20", "passed": 1 <= zagadannoe <= 20},
    {"name": "popytka — цикл завершился, когда угадали (popytka == zagadannoe)", "passed": popytka == zagadannoe},
    {"name": "popytki — счётчик попыток отработал", "passed": isinstance(popytki, int) and popytki >= 1},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
