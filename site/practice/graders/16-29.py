checks = [
    {"name": "tasks — пустая задача не добавилась, остальные две сохранились по порядку", "passed": tasks == ["Купить молоко", "Позвонить"]},
    {"name": "loaded_tasks — задачи корректно загружены из JSON-файла", "passed": loaded_tasks == ["Купить молоко", "Позвонить"]},
    {"name": "tasks_after_remove — remove_task() удалил именно первую задачу", "passed": tasks_after_remove == ["Позвонить"]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
