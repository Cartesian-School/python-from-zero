checks = [
    {"name": "schet, chaevye — введены и преобразованы в float", "passed": isinstance(schet, float) and isinstance(chaevye, float)},
    {"name": "procent — вычислен верно по введённым значениям", "passed": schet == 0 or abs(procent - (chaevye / schet) * 100) < 1e-9},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
