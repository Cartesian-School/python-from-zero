checks = [
    {"name": "read_data — бинарные данные прочитаны байт-в-байт", "passed": read_data == bytes([10, 20, 30])},
    {"name": "chars_len2 — «Питон🐍» состоит из 6 символов", "passed": chars_len2 == 6},
    {"name": "bytes_len2 — в UTF-8 «Питон🐍» занимает 14 байт", "passed": bytes_len2 == 14},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
