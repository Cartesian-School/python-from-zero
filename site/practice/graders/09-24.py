checks = [
    {"name": "level — score=82 попадает в «хорошо»", "passed": level == "хорошо"},
    {"name": "action — command=\"START\" нормализуется и запускает", "passed": action == "Запуск..."},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
