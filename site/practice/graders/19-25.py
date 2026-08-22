checks = [
    {"name": "рекорд не понижается при меньшем счёте", "passed": update_high_score(30, 40) == 40},
    {"name": "рекорд обновляется при большем счёте", "passed": update_high_score(50, 40) == 50},
    {"name": "равные значения не меняют рекорд", "passed": update_high_score(0, 0) == 0},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
