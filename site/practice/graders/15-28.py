checks = [
    {"name": "tmp_exists_after — временный файл заменил основной и сам не остался", "passed": tmp_exists_after is False},
    {"name": "result_data — данные сохранены и читаются верно после безопасной записи", "passed": result_data == {"score": 500}},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
