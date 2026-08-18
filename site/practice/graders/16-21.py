checks = [
    {"name": "vse_s_metkami — все поля формы имеют видимую подпись", "passed": vse_s_metkami is True},
    {"name": "poryadok_ok — порядок перехода Tab последователен", "passed": poryadok_ok is True},
    {"name": "najdena_problema — форма без подписи распознана как проблемная", "passed": najdena_problema is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
