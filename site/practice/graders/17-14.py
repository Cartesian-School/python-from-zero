checks = [
    {"name": "index_to_row_col(4) == (1, 1)", "passed": index_to_row_col(4) == (1, 1)},
    {"name": "row_col_to_index(2, 2) == 8", "passed": row_col_to_index(2, 2) == 8},
    {"name": "roundtrip_ok — верно для всех 9 клеток", "passed": roundtrip_ok is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
