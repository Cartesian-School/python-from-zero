checks = [
    {"name": "term_proizoshlo — событие само по себе", "passed": term_proizoshlo == "event"},
    {"name": "term_funkciya_v_otvet — функция, вызванная в ответ", "passed": term_funkciya_v_otvet == "callback"},
    {"name": "term_svyaz_sobytiya_i_funkcii — связь события и callback-а", "passed": term_svyaz_sobytiya_i_funkcii == "binding"},
    {"name": "term_semanticheskaya_aktivaciya — крючок виджета", "passed": term_semanticheskaya_aktivaciya == "command"},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
