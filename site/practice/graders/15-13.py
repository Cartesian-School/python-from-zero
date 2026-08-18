checks = [
    {"name": "first — первые 2 символа AB", "passed": first == "AB"},
    {"name": "pos_after_first — курсор на позиции 2", "passed": pos_after_first == 2},
    {"name": "second — следующие 2 символа CD", "passed": second == "CD"},
    {"name": "reread — после seek(0) файл читается заново целиком", "passed": reread == "ABCDE"},
    {"name": "posle_konca_pusto — повторный read() на EOF возвращает пустую строку", "passed": posle_konca_pusto is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
