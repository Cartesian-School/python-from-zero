checks = [
    {"name": "pravilnyj_otvet — сгенерирован в разумном диапазоне (2..9 x 2..9)", "passed": 4 <= pravilnyj_otvet <= 81},
    {"name": "otvet — введён через input() и преобразован в int", "passed": isinstance(otvet, int)},
    {"name": "pravilnyh — счётчик правильных ответов за 5 попыток", "passed": isinstance(pravilnyh, int) and 0 <= pravilnyh <= 5},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
