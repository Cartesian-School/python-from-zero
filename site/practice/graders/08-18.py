checks = [
    {"name": "count — количество вхождений bukva в text, посчитанное вручную", "passed": count == text.count(bukva)},
    {"name": "count больше нуля (bukva реально встречается в text)", "passed": count > 0},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
