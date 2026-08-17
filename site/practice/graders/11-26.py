checks = [
    {"name": "contacts — итоговая записная книжка после add/update/delete", "passed": contacts == {"Anna": "anna.new@example.com", "Maria": "maria@example.com"}},
    {"name": "missing — required - available", "passed": missing == {"sql"}},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
