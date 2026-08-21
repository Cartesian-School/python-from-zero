checks = [
    {"name": "p1 == (40, 30)", "passed": p1 == (40, 30)},
    {"name": "p2 == (160, 120)", "passed": p2 == (160, 120)},
    {"name": "dvizhenie_vniz(30, 120) is True", "passed": dvizhenie_vniz(30, 120) is True},
    {"name": "dvizhenie_vniz(120, 30) is False", "passed": dvizhenie_vniz(120, 30) is False},
    {"name": "dvizhenie_vniz(50, 50) is False", "passed": dvizhenie_vniz(50, 50) is False},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
