checks = [
    {"name": "chetnye_count — счётчик чётных чисел исправлен (инициализация вынесена из цикла)", "passed": chetnye_count == sum(1 for n in chisla if n % 2 == 0)},
    {"name": "chisla_1_do_10 — off-by-one исправлен, диапазон включает 10", "passed": chisla_1_do_10 == list(range(1, 11))},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
