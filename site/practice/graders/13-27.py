checks = [
    {"name": "avg — average([70, 80, 90])", "passed": avg == 80.0},
    {"name": "above — count_above([70, 80, 90], 75)", "passed": above == 2},
    {"name": "uniq — unique_words нормализует регистр и убирает повторы", "passed": uniq == {"python", "code"}},
    {"name": "top — find_top_score выбрал ученика с максимальным баллом", "passed": top == {"name": "Anna", "score": 95}},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
