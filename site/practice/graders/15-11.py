checks = [
    {"name": "mode_value — файл открыт в режиме r", "passed": mode_value == "r"},
    {"name": "name_value — имя файла верно", "passed": name_value == "privet2.txt"},
    {"name": "closed_during — файл открыт внутри блока with", "passed": closed_during is False},
    {"name": "closed_after — файл закрыт после выхода из блока with", "passed": closed_after is True},
    {"name": "content — содержимое прочитано верно", "passed": content == "привет"},
    {"name": "tip_ne_str и tip_ne_list — объект файла не строка и не список", "passed": tip_ne_str is True and tip_ne_list is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
