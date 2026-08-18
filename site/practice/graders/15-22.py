checks = [
    {"name": "not_found_caught — FileNotFoundError перехвачен при чтении несуществующего файла", "passed": not_found_caught is True},
    {"name": "is_dir_error_caught — IsADirectoryError перехвачен при открытии папки как файла", "passed": is_dir_error_caught is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
