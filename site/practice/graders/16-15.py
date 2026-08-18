checks = [
    {"name": "result_equal — равные веса делят место поровну", "passed": result_equal == [100.0, 100.0]},
    {"name": "result_weighted — вес 2 получает вдвое больше веса 1", "passed": result_weighted == [100.0, 200.0]},
    {"name": "result_three — распределение для трёх колонок с весами [1,1,2]", "passed": result_three == [100.0, 100.0, 200.0]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
