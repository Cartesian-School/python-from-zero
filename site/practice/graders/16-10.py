checks = [
    {"name": "log — события обработаны в порядке очереди", "passed": log == ["click", "timer", "type"]},
    {"name": "calls — greet() был вызван ровно один раз (при command_wrong)", "passed": len(calls) == 1},
    {"name": "command_wrong — получил возвращённое значение, а не функцию", "passed": command_wrong == "hello"},
    {"name": "command_correct — осталась сама функция, вызываемая позже", "passed": callable(command_correct) is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
