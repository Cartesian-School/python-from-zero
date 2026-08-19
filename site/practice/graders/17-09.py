checks = [
    {"name": "seq_klavisha_enter == '<Return>'", "passed": seq_klavisha_enter == "<Return>"},
    {"name": "seq_navedenie_vhod == '<Enter>'", "passed": seq_navedenie_vhod == "<Enter>"},
    {"name": "seq_navedenie_vyhod == '<Leave>'", "passed": seq_navedenie_vyhod == "<Leave>"},
    {"name": "seq_klik_levoj_knopkoj == '<Button-1>'", "passed": seq_klik_levoj_knopkoj == "<Button-1>"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
