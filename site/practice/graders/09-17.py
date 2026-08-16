checks = [
    {"name": "safe_check — falsy для пустой строки (short-circuit сработал, IndexError не возник)", "passed": bool(safe_check) is False},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
