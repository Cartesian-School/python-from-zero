checks = [
    {"name": "dlina — len(\"Cartesian\") == 9", "passed": dlina == 9},
    {"name": "posledniy_index — dlina - 1 == 8", "passed": posledniy_index == 8},
    {"name": "word[posledniy_index] совпадает с word[-1]", "passed": word[posledniy_index] == word[-1]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
