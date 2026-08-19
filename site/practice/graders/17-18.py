checks = [
    {"name": "виджет показывает превью 'X'", "passed": fresh_buttons[0].text == "X"},
    {"name": "модель НЕ изменилась при наведении", "passed": board_model[0] == ""},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
