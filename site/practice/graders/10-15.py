checks = [
    {"name": "vozrast — цикл переспрашивал, пока ввод не стал числом", "passed": vozrast == 15},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
