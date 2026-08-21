checks = [
    {"name": "tegi['shape'] == [12, 13]", "passed": tegi.get("shape") == [12, 13]},
    {"name": "tegi['preview'] == [15]", "passed": tegi.get("preview") == [15]},
    {"name": "у 'shape' два элемента", "passed": len(tegi.get("shape", [])) == 2},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
