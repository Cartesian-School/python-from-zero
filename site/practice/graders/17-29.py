checks = [
    {"name": "сломанная версия ошибочно объявляет ничью", "passed": status_broken(posledny_hod) == "Ничья!"},
    {"name": "исправленная версия находит победителя", "passed": "Победил" in status_fixed(posledny_hod)},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
