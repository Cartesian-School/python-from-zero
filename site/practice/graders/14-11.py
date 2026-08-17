checks = [
    {"name": "krug.ploshchad — вычислено верно (radius=10)", "passed": abs(ploshchad_do - 314.159) < 0.01},
    {"name": "отрицательный radius — вызывает ValueError", "passed": validatsiya_srabotala is True},
    {"name": "неудачное присваивание не меняет radius", "passed": krug.radius == 10},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
