checks = [
    {"name": "nadyozhnyj — совпадает с самостоятельно посчитанным правилом", "passed": nadyozhnyj == (len(password) >= 8 and any(ch.isdigit() for ch in password) and any(ch.isalpha() for ch in password))},
    {"name": "pohozhe_na_email — совпадает с самостоятельно посчитанной проверкой", "passed": pohozhe_na_email == (email.count("@") == 1)},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
