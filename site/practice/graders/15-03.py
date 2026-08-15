checks = [
    {"name": "file_path — существует, имя и расширение верны", "passed": file_path.exists() and file_path.name == "rezultaty.txt" and file_path.suffix == ".txt"},
    {"name": "режим \"w\" стёр старое содержимое (осталась только последняя запись)", "passed": file_path.read_text() == "Новая игра началась.\n"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
