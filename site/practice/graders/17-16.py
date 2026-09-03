CANONICAL_LINES = {
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
}

checks = [
    {"name": "все восемь линий верны для X и O", "passed": vse_linii_ok is True},
    {"name": "пустое поле — победителя нет", "passed": find_winner([""] * 9) == (None, None)},
    # Проверки ниже НЕ используют WINNING_LINES ученика: доски заданы явно, поэтому
    # опечатка в самой константе (например (0, 4, 6) вместо (0, 4, 8) — Debug Lab 9)
    # не может «спрятаться» за тестом, построенным из той же опечатки.
    {"name": "главная диагональ 0-4-8 распознана",
     "passed": find_winner(["X", "", "", "", "X", "", "", "", "X"]) == ("X", (0, 4, 8))},
    {"name": "побочная диагональ 2-4-6 распознана",
     "passed": find_winner(["", "", "O", "", "O", "", "O", "", ""]) == ("O", (2, 4, 6))},
    {"name": "нижняя строка 6-7-8 распознана",
     "passed": find_winner(["", "", "", "", "", "", "X", "X", "X"]) == ("X", (6, 7, 8))},
    {"name": "WINNING_LINES содержит ровно восемь канонических линий",
     "passed": set(WINNING_LINES) == CANONICAL_LINES},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
