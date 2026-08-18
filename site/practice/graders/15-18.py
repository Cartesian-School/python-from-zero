checks = [
    {"name": "text_back — write_text/read_text сохранили текст с кириллицей верно", "passed": text_back == "привет"},
    {"name": "bytes_back — write_bytes/read_bytes сохранили байты верно", "passed": bytes_back == bytes([1, 2, 3])},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
