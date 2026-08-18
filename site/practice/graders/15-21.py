checks = [
    {"name": "rename_ok — файл переименован, старое имя больше не существует", "passed": rename_ok is True},
    {"name": "copy_ok — копия содержит то же содержимое, что оригинал", "passed": copy_ok is True},
    {"name": "delete_ok — unlink() удалил временный файл", "passed": delete_ok is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
