checks = [
    {"name": "summary['total_words'] — число слов", "passed": summary["total_words"] == 7},
    {"name": "summary['unique_words'] — число уникальных слов", "passed": summary["unique_words"] == 5},
    {"name": "summary['counts'] — частота каждого слова верна", "passed": summary["counts"] == {"python": 2, "is": 2, "great": 1, "and": 1, "fun": 1}},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
