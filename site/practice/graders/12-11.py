checks = [
    {"name": "kolichestvo_simvolov — длина введённого текста", "passed": kolichestvo_simvolov == len(text)},
    {"name": "kolichestvo_slov — число слов", "passed": kolichestvo_slov == 7},
    {"name": "kolichestvo_unikalnyh — число уникальных слов", "passed": kolichestvo_unikalnyh == 5},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
