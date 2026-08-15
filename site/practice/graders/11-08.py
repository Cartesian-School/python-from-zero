checks = [
    {"name": "films — словарь фильмов и годов создан верно", "passed": films == {"Матрица": 1999, "Начало": 2010, "Интерстеллар": 2014}},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
