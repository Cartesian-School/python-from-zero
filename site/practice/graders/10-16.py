checks = [
    {"name": "ugadal — все 5 попыток исчерпаны без угадывания, сработал loop-else", "passed": ugadal is False},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
