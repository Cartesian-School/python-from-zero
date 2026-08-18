checks = [
    {"name": "razobrannaya_stroka — csv.reader корректно разобрал запятую внутри поля в кавычках", "passed": razobrannaya_stroka == ["Anna", "Отлично, продолжай!"]},
    {"name": "zagruzhennye — DictWriter/DictReader сохранили и вернули обе записи", "passed": len(zagruzhennye) == 2 and zagruzhennye[0]["name"] == "Anna"},
    {"name": "zagruzhennye[1] — значения CSV читаются как строки, пока их не преобразовать", "passed": zagruzhennye[1]["score"] == "900" and int(zagruzhennye[1]["score"]) == 900},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
