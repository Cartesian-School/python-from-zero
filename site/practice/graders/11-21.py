checks = [
    {"name": "anna_python — students[0]['scores']['python']", "passed": anna_python == 100},
    {"name": "bob_math — students[1]['scores']['math']", "passed": bob_math == 82},
    {"name": "imena — список всех имён по порядку", "passed": imena == ["Anna", "Bob"]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
