checks = [
    {"name": "сломанная версия ошибочно объявляет ничью", "passed": status_broken(poslednij_hod) == "Ничья!"},
    {"name": "исправленная версия находит победителя", "passed": "Победил" in status_fixed(poslednij_hod)},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
