checks = [
    {"name": "poluchit_zvuk(Sobaka()) — Гав!", "passed": zvuk_sobaki == "Гав!"},
    {"name": "poluchit_zvuk(Koshka()) — Мяу!", "passed": zvuk_koshki == "Мяу!"},
    {"name": "poluchit_zvuk(Korova()) — Му!", "passed": zvuk_korovy == "Му!"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
