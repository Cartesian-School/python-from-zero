checks = [
    {"name": "lines — readlines() вернул все 4 строки", "passed": len(lines) == 4},
    {"name": "lines[0] — первый элемент списка покупок", "passed": lines[0].strip() == "яблоки"},
    {"name": "count — подсчёт строк циклом совпадает с фактическим числом строк", "passed": count == 4},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
