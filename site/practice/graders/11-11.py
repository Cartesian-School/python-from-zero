checks = [
    {"name": "ocenki — правильный список", "passed": ocenki == [95, 82, 91, 77, 88]},
    {"name": "ocenki — это именно list", "passed": isinstance(ocenki, list)},
    {"name": "len(ocenki) == 5", "passed": len(ocenki) == 5},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
