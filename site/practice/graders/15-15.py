checks = [
    {"name": "posle_dozapisi — дозапись добавила строку, не стирая старую", "passed": posle_dozapisi == "старт\nпродолжение\n"},
    {"name": "x_failed_as_expected — режим x отказал создавать уже существующий файл", "passed": x_failed_as_expected is True},
    {"name": "igroki_content — writelines() потребовал явных \\n в каждом элементе", "passed": igroki_content == "Anna\nBob\n"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
