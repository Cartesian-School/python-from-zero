checks = [
    {"name": "vybor_dlya_nastroek — вложенная структура настроек лучше всего подходит для JSON", "passed": vybor_dlya_nastroek == "JSON"},
    {"name": "vybor_dlya_tablitsy_rezultatov — однородная таблица результатов лучше всего подходит для CSV", "passed": vybor_dlya_tablitsy_rezultatov == "CSV"},
    {"name": "vybor_dlya_zametok — простой список заметок лучше всего подходит для обычного текста", "passed": vybor_dlya_zametok == "текст"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
