checks = [
    {"name": "zhurnal — цикл команд отработал верно (help/list не добавляются, stop завершает)", "passed": zhurnal == ["привет"]},
    {"name": "naideno_100 — loop-else сработал верно (100 нет в списке)", "passed": naideno_100 is False},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
