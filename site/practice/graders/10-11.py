checks = [
    {"name": "slova — текст разбит на 5 слов", "passed": len(slova) == 5},
    {"name": "glasnye_count — гласные посчитаны верно", "passed": glasnye_count == sum(1 for ch in tekst if ch in "аеёиоуыэюя")},
    {"name": "samoe_dlinnoe — самое длинное слово найдено верно", "passed": samoe_dlinnoe == "понятно"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
