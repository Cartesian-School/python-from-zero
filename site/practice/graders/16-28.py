checks = [
    {"name": "t1/t2/t3 — format_time() форматирует минуты и секунды верно", "passed": t1 == "01:05" and t2 == "10:00" and t3 == "00:05"},
    {"name": "after_tick — тик уменьшает remaining, пока running истинно", "passed": after_tick == 9},
    {"name": "after_stop — тик не уменьшает remaining, когда running ложно", "passed": after_stop == 10},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
