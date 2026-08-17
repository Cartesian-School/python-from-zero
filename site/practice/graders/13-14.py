checks = [
    {"name": "r1 — значение color по умолчанию", "passed": r1 == "10x20 blue"},
    {"name": "r2 — color передан по имени", "passed": r2 == "10x20 red"},
    {"name": "keyword_only_enforced — позиционная передача color вызывает TypeError", "passed": keyword_only_enforced is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
