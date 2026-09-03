checks = [
    {"name": "proverit_pobedu — верхняя строка X даёт победителя X", "passed": proverit_pobedu(["X", "X", "X", "", "", "", "", "", ""]) == "X"},
    {"name": "proverit_pobedu — без победителя возвращает None", "passed": proverit_pobedu(["O", "X", "O", "X", "O", "X", "X", "O", "X"]) is None},
    {"name": "pole_zapolneno — верно определяет полное поле без победителя", "passed": pole_zapolneno(["X", "O", "X", "X", "O", "O", "O", "X", "X"]) is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
