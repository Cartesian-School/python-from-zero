checks = [
    {"name": "names — итоговый список после remove/pop/del", "passed": names == ["Maria"]},
    {"name": "last — значение, удалённое через pop()", "passed": last == "Leo"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
