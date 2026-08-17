checks = [
    {"name": "t1 — total(*numbers) с произвольным числом аргументов", "passed": t1 == 10},
    {"name": "profile — show_profile(**fields) собрал словарь", "passed": profile == {"name": "Anna", "city": "Warsaw"}},
    {"name": "moved — move(*point) распаковал кортеж в аргументы", "passed": moved == 30},
    {"name": "total — верна на новых аргументах", "passed": total(5, 5, 5) == 15},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
