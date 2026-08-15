checks = [
    {"name": "q1 — кавычки вокруг «Привет!» одинарные", "passed": q1 == 'Она сказала: \'Привет!\''},
    {"name": "q2 (другой тип кавычек снаружи) и q3 (экранирование) дают одну и ту же строку", "passed": q2 == q3},
    {"name": "q2/q3 — кавычки вокруг «Привет!» двойные", "passed": '"Привет!"' in q2},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
