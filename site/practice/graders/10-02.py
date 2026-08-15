checks = [
    {"name": "row — треугольник из звёздочек выполнен до конца (1..5)", "passed": row == 5},
    {"name": "a, b — вложенная таблица умножения выполнена до конца (5x5)", "passed": a == 5 and b == 5},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
