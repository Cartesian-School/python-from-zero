checks = [
    {"name": "Dengi(100) == Dengi(100) — равенство по значению", "passed": ravny is True},
    {"name": "Dengi(100) != Dengi(250) — разные суммы не равны", "passed": ne_ravny is False},
    {"name": "__hash__ определён — объекты работают в множестве", "passed": len(mnozhestvo) == 2},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
