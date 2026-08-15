checks = [
    {"name": "result — значение вернулось наружу через return", "passed": result == "Теперь я возвращаюсь наружу"},
    {"name": "schet — global верно увеличен двумя вызовами", "passed": schet == 2},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
