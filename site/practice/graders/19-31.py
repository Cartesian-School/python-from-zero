checks = [
    {
        "name": "разворот на 180 -> is_reverse не проверяется",
        "passed": diagnose("змейка мгновенно врезается в себя при развороте") == "is_reverse не проверяется",
    },
    {
        "name": "зависшее окно -> time.sleep() в цикле",
        "passed": diagnose("окно не реагирует на клавиши несколько секунд") == "time.sleep() в игровом цикле",
    },
    {
        "name": "призрак прошлой игры -> нет generation guard",
        "passed": diagnose("после Restart появляется фигура из прошлой игры") == "нет generation guard",
    },
    {
        "name": "пауза визуальная -> status не проверяется",
        "passed": diagnose("оверлей ПАУЗА показан, но змейка всё равно едет") == "status не проверяется в game_tick",
    },
    {
        "name": "незнакомый симптом не выдаётся за диагноз",
        "passed": diagnose("змейка светится розовым") == "неизвестный симптом",
    },
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
