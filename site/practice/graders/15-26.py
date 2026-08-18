checks = [
    {"name": "loaded_player — восстановленный Player равен по значению исходному", "passed": loaded_player == player},
    {"name": "is_same_object — это НЕ тот же объект, а новый экземпляр", "passed": is_same_object is False},
    {"name": "loaded_player.inventory — инвентарь восстановлен верно", "passed": loaded_player.inventory == ["меч", "щит"]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
