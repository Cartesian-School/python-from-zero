checks = [
    {"name": "summa — сумма списка через накопитель", "passed": summa == sum(chisla)},
    {"name": "chetnye_chisla — фильтрация чётных чисел", "passed": chetnye_chisla == [n for n in chisla if n % 2 == 0]},
    {"name": "maksimum — поиск максимума вручную", "passed": maksimum == max(chisla)},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
