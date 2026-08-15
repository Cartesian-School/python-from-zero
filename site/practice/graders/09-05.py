checks = [
    {"name": "zagadannoe — случайное число в диапазоне 1..20", "passed": 1 <= zagadannoe <= 20},
    {"name": "popytka — введено через input() и преобразовано в int", "passed": isinstance(popytka, int)},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
