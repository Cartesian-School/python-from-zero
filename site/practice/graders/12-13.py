checks = [
    {"name": "contacts — итоговая записная книжка после add/update/delete", "passed": contacts == {"Anna": "+48 111 000 000", "Maria": "+48 333 333 333"}},
    {"name": "kolichestvo — число оставшихся контактов", "passed": kolichestvo == 2},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
