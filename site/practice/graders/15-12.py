checks = [
    {"name": "closed_inside — файл открыт внутри блока with", "passed": closed_inside is False},
    {"name": "closed_outside — файл закрыт после выхода из блока with", "passed": closed_outside is True},
    {"name": "closed_before_manual_close — файл открыт до вызова close()", "passed": closed_before_manual_close is False},
    {"name": "closed_after_manual_close — файл закрыт после явного close()", "passed": closed_after_manual_close is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
