checks = [
    {"name": "in_range_correct — 1 <= 1 <= 10 (граница включена)", "passed": in_range_correct is True},
    {"name": "in_range_buggy — 1 < 1 < 10 (off-by-one отвергает границу)", "passed": in_range_buggy is False},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
