checks = [
    {"name": "otlichniki — только оценки >= 90", "passed": otlichniki == [95, 91]},
    {"name": "otlichniki_s_indeksami — пары (индекс, оценка)", "passed": otlichniki_s_indeksami == [(0, 95), (2, 91)]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
