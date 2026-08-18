checks = [
    {"name": "top2 — top_n() вернул двух лучших игроков по убыванию очков", "passed": len(top2) == 2 and top2[0]["name"] == "Bob" and top2[1]["name"] == "Carlos"},
    {"name": "anna_score — повторная запись обновила рекорд, а не добавила вторую строку", "passed": anna_score == 2000},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
