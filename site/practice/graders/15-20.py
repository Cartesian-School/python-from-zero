checks = [
    {"name": "vse_items — iterdir() показал все 3 элемента папки", "passed": vse_items == ["a.txt", "b.csv", "c.txt"]},
    {"name": "txt_files — glob(\"*.txt\") отобрал только .txt файлы", "passed": txt_files == ["a.txt", "c.txt"]},
    {"name": "otchet — отчёт по папке построен для всех элементов", "passed": len(otchet) == 3 and all("файл" in line or "папка" in line for line in otchet)},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
