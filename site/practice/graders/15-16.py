checks = [
    {"name": "chars_len — «Питон» состоит из 5 символов", "passed": chars_len == 5},
    {"name": "bytes_len — в UTF-8 «Питон» занимает 10 байт", "passed": bytes_len == 10},
    {"name": "decoded_back — decode(encode(text)) возвращает исходный текст", "passed": decoded_back == "Питон"},
    {"name": "read_back — текст с кириллицей прочитан обратно верно при encoding=\"utf-8\"", "passed": read_back == "Привет!"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
