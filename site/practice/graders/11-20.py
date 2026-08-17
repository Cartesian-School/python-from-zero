checks = [
    {"name": "counts — итоговый подсчёт после pop('b')", "passed": counts == {"a": 3, "c": 1}},
    {"name": "vse_klyuchi — отсортированные ключи до удаления", "passed": vse_klyuchi == ["a", "b", "c"]},
    {"name": "udalyonnoe — значение, удалённое через pop()", "passed": udalyonnoe == 2},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
