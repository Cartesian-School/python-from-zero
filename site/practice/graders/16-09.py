checks = [
    {"name": "before_dispatch — callback ещё не вызван при регистрации", "passed": before_dispatch == []},
    {"name": "after_dispatch — callback вызван при явной диспетчеризации", "passed": after_dispatch == ["clicked"]},
    {"name": "registered_is_callable — registered остаётся вызываемым объектом", "passed": registered_is_callable is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
