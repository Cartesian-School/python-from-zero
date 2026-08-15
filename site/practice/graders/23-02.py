checks = [
    {"name": "kolichestvo_variantov — общее число возможных историй посчитано верно", "passed": kolichestvo_variantov == 5 * 5 * 4 * 5 * 4},
    {"name": "sg.sluchajnaya_istoriya() — генерирует историю по шаблону", "passed": sg.sluchajnaya_istoriya().startswith("Однажды")},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
