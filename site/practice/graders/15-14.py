checks = [
    {"name": "first_line — первая строка a", "passed": first_line == "a"},
    {"name": "second_line — вторая строка b", "passed": second_line == "b"},
    {"name": "all_lines — readlines() вернул все 3 строки", "passed": len(all_lines) == 3},
    {"name": "counted — цикл for посчитал те же 3 строки", "passed": counted == 3},
    {"name": "sovpadaet — подсчёт циклом совпадает с readlines()", "passed": sovpadaet is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
