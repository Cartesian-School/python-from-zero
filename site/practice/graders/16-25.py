checks = [
    {"name": "defaults — при отсутствии файла возвращаются значения по умолчанию", "passed": defaults == {"theme": "light", "window_width": 900}},
    {"name": "loaded — после save_settings загруженные настройки совпадают с сохранёнными", "passed": loaded == {"theme": "dark", "window_width": 1024}},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
