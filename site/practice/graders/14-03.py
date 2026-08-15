checks = [
    {"name": "Kniga.opisanie() — верно форматирует «Название — Автор»", "passed": k.opisanie() == "Война и мир — Толстой"},
    {"name": "Biblioteka — хранит добавленные книги", "passed": len(biblioteka.knigi) == 2},
    {"name": "все книги в библиотеке имеют рабочий opisanie()", "passed": all(hasattr(b, "opisanie") and callable(b.opisanie) for b in biblioteka.knigi)},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
