checks = [
    {"name": "kuby_v1 — кубы через цикл с append()", "passed": kuby_v1 == [n ** 3 for n in range(1, 11)]},
    {"name": "kuby_v1 == kuby_v2 — оба способа дают одинаковый результат", "passed": kuby_v1 == kuby_v2},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
