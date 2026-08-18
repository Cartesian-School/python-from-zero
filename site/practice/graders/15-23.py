checks = [
    {"name": "result — строки, слова и символы посчитаны потоково верно", "passed": result == {"строки": 3, "слова": 7, "символы": 48}},
    {"name": "razmer_v_baytah — размер файла в байтах (не в символах!) получен через stat().st_size", "passed": razmer_v_baytah == 89},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
