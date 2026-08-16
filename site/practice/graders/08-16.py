checks = [
    {"name": "is_pdf — filename.endswith(\".pdf\") is True", "passed": is_pdf is True},
    {"name": "position — filename.find(\"_\") == 6", "passed": position == 6},
    {"name": "parts — filename.split(\"_\") == ['report', 'final.pdf']", "passed": parts == ["report", "final.pdf"]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
