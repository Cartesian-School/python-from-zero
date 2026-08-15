checks = [
    {"name": "full_name — введено имя, отчество и фамилия через пробел", "passed": len(full_name.split()) == 3},
    {"name": "initials — инициалы построены из name и patronymic", "passed": initials == f"{name[0]}.{patronymic[0]}."},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
