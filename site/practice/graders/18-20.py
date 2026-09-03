# Порядок наложения: последний элемент списка — верхний, первый — нижний
# (раздел 18.20). tag_raise поднимает в конец, tag_lower опускает в начало.
checks = [
    {"name": "podnyat переносит элемент в конец", "passed": poryadok == [13, 14, 12]},
    {"name": "opustit переносит элемент в начало", "passed": poryadok_vniz == [14, 12, 13]},
    {"name": "podnyat/opustit работают на любом списке", "passed": poryadok2 == [2, 1, 3]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
