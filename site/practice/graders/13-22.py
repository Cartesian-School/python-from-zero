checks = [
    {"name": "final_score — run_quiz посчитал верные ответы", "passed": final_score == 2},
    {"name": "check_answer — верна на новых аргументах (регистр/пробелы)", "passed": check_answer("  PARIS  ", "paris") is True},
    {"name": "check_answer — верно отклоняет неверный ответ", "passed": check_answer("london", "paris") is False},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
