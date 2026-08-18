checks = [
    {"name": "loaded — json.dump/load сохранили и вернули словарь верно", "passed": loaded == {"name": "Anna", "score": 1200}},
    {"name": "settings_missing — при отсутствии файла возвращаются значения по умолчанию", "passed": settings_missing == {"theme": "light", "language": "ru"}},
    {"name": "settings_loaded — после save_settings загруженные настройки совпадают с сохранёнными", "passed": settings_loaded == {"theme": "dark", "language": "ru"}},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
