checks = [
    {"name": "поверхностная копия: оригинал тоже изменился", "passed": posle_melkoy == 999},
    {"name": "глубокая копия: оригинал остался прежним", "passed": posle_glubokoy == 10},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
