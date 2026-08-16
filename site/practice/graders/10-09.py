checks = [
    {"name": "otschet — числа от 100 до 50 с шагом -5", "passed": otschet == list(range(100, 45, -5))},
    {"name": "otschet — начинается со 100 и заканчивается 50", "passed": len(otschet) > 0 and otschet[0] == 100 and otschet[-1] == 50},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
