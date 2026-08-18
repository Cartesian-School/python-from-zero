checks = [
    {"name": "file_path — путь собран правильно через /", "passed": str(file_path) == "data/players/anna.json" or file_path.as_posix() == "data/players/anna.json"},
    {"name": "parts_increased — более глубокий путь имеет больше частей", "passed": parts_increased is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
