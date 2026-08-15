checks = [
    {"name": "krik — phrase.upper() + \"!!!\"", "passed": krik == phrase.upper() + "!!!"},
    {"name": "perevernutoe — name развёрнуто срезом [::-1]", "passed": perevernutoe == name[::-1]},
    {"name": "word — введено для проверки палиндрома", "passed": isinstance(word, str) and len(word) > 0},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
