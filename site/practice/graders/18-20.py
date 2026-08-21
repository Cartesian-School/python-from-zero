checks = [
    {"name": "podnyat переносит элемент в конец", "passed": poryadok == [13, 14, 12]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
