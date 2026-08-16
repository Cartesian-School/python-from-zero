checks = [
    {"name": "quote — содержит экранированную кавычку внутри текста", "passed": quote.count('"') == 2},
    {"name": "two_lines — состоит из двух строк, разделённых \\n", "passed": len(two_lines.split("\n")) == 2},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
