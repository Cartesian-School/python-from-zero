checks = [
    {"name": "itogi — словарь из zip(names, scores)", "passed": itogi == {"Anna": 95, "Bob": 82, "Maria": 91}},
    {"name": "stroki — отформатированные строки в порядке словаря", "passed": stroki == ["Anna: 95", "Bob: 82", "Maria: 91"]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
