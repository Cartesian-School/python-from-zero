checks = [
    {"name": "total_widgets — дерево содержит все 5 узлов", "passed": total_widgets == 5},
    {"name": "save_button_parent — родитель save_button найден верно", "passed": save_button_parent == "main_frame"},
    {"name": "title_label_parent — родитель title_label найден верно", "passed": title_label_parent == "main_frame"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
