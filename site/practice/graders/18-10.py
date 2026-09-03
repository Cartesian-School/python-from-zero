# item_id — это КЛЮЧ словаря, а не индекс списка (раздел 18.10, Debug Lab 8).
# Самая ожидаемая ошибка здесь — собрать shapes_by_id списком; проверяем тип
# первым, чтобы такая работа получила понятный FAIL, а не падение проверки.
is_dict = isinstance(shapes_by_id, dict)

checks = [
    {
        "name": "shapes_by_id — словарь (item_id как ключ, а не индекс списка)",
        "passed": is_dict,
    },
    {"name": "shapes_by_id[3] == 'rectangle'", "passed": is_dict and shapes_by_id.get(3) == "rectangle"},
    {"name": "shapes_by_id[7] == 'oval'", "passed": is_dict and shapes_by_id.get(7) == "oval"},
    {"name": "5 не зарегистрирован", "passed": is_dict and 5 not in shapes_by_id},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
