checks = [
    {"name": "ok1 — пустая строка не является числом", "passed": ok1 is False},
    {"name": "ok2 — нечисловой текст не является числом", "passed": ok2 is False},
    {"name": "ok3/val3 — отрицательное число ЧИСЛОМ является (parse_number не отвергает его)", "passed": ok3 is True and val3 == -5.0},
    {"name": "ok4/val4 — корректное положительное число разобрано верно", "passed": ok4 is True and val4 == 100.0 and msg4 == ""},
    {"name": "amount_negative_ok — validate_positive_amount отвергает отрицательную сумму", "passed": amount_negative_ok is False},
    {"name": "amount_valid_ok — validate_positive_amount принимает положительную сумму", "passed": amount_valid_ok is True},
    {"name": "people_float_ok — validate_positive_int отвергает дробное количество человек", "passed": people_float_ok is False},
    {"name": "people_valid_ok — validate_positive_int принимает положительное целое", "passed": people_valid_ok is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
