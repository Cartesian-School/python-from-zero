checks = [
    {"name": "exists_before — путь не существовал до проверки", "passed": exists_before is False},
    {"name": "created — mkdir(parents=True, exist_ok=True) создал вложенные папки", "passed": created is True},
    {"name": "is_file_check — файл внутри созданных папок распознан как файл", "passed": is_file_check is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
