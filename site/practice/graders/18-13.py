checks = [
    {"name": "state.tool is Tool.RECTANGLE", "passed": state.tool is Tool.RECTANGLE},
    {"name": "state.color == '#2563eb'", "passed": state.color == "#2563eb"},
    {"name": "state.width == 4 (умолчание не тронуто)", "passed": state.width == 4},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
