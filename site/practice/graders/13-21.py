checks = [
    {"name": "pipeline_result — normalize_text → split_words → count_words", "passed": pipeline_result == 3},
    {"name": "normalize_text — верна на новом входе", "passed": normalize_text("HELLO") == "hello"},
    {"name": "split_words — верна на новом входе", "passed": split_words("a b c") == ["a", "b", "c"]},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
