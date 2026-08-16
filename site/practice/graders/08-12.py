checks = [
    {"name": "multiline — три строки текста, соединённые переносами", "passed": len(multiline.split("\n")) == 3},
    {"name": "raw_path — путь без экранирования, содержит обратные чёрточки", "passed": raw_path == "D:\\Data\\file.txt"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
