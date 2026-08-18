checks = [
    {"name": "papka — распознана как папка", "passed": papka.is_dir()},
    {"name": "fajl — распознан как файл", "passed": fajl.is_file()},
    {"name": "total_items — три элемента внутри proekt/ (data, README.md, assets)", "passed": total_items == 3},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
