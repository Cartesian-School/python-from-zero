checks = [
    {"name": "Korova.zvuk() — своя реализация", "passed": burenka.zvuk() == "Му!"},
    {"name": "Korova — унаследовала predstavitsya() от Zhivotnoe", "passed": burenka.predstavitsya() == "Я Бурёнка"},
    {"name": "burenka — является Zhivotnoe (IS-A)", "passed": isinstance(burenka, Zhivotnoe)},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
