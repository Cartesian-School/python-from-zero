checks = [
    {"name": "existed_before — файл отчёта не существовал до записи", "passed": existed_before is False},
    {"name": "existed_after — файл отчёта существует после write_text", "passed": existed_after is True},
    {"name": "file_path — имя и расширение верны", "passed": file_path.name == "otchet.txt" and file_path.suffix == ".txt"},
    {"name": "sovpadaet — родитель родителя data_dir совпадает с BASE_DIR.parent", "passed": sovpadaet is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
