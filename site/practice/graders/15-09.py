checks = [
    {"name": "path.name — scores.txt", "passed": path.name == "scores.txt"},
    {"name": "path.stem — scores", "passed": path.stem == "scores"},
    {"name": "path.suffix — .txt", "passed": path.suffix == ".txt"},
    {"name": "suffix_pust — путь без расширения имеет пустой suffix", "passed": suffix_pust is True},
    {"name": "stem_ravno_name — без суффикса stem совпадает с name", "passed": stem_ravno_name is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
