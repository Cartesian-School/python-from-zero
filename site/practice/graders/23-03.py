checks = [
    {"name": "opredelit_pobeditelya — камень бьёт ножницы", "passed": rps.opredelit_pobeditelya("камень", "ножницы") == "игрок"},
    {"name": "opredelit_pobeditelya — ничья при одинаковом выборе", "passed": rps.opredelit_pobeditelya("бумага", "бумага") == "ничья"},
    {"name": "schet — 200 случайных раундов дали все три исхода", "passed": sum(schet.values()) == 200 and schet["игрок"] > 0 and schet["компьютер"] > 0},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
