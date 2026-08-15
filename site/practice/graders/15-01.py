checks = [
    {"name": "content — прочитанное содержимое privet.txt верно", "passed": content == "Привет из файла!\nЭто вторая строка."},
    {"name": "o_sebe.txt — реально создан и содержит верный текст", "passed": open("o_sebe.txt").read() == "Cartesian\nМосква"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
