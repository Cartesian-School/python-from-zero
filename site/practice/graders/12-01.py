checks = [
    {"name": "number — введено и преобразовано в int", "passed": isinstance(number, int)},
    {"name": "chetnye — все значения действительно чётные", "passed": all(n % 2 == 0 for n in chetnye)},
    {"name": "nechetnye — нечётные числа от 1 до 20", "passed": nechetnye == [n for n in range(1, 21) if n % 2 != 0]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
