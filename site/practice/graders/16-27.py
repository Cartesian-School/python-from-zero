checks = [
    {"name": "f_100 — 100°C верно переведены в 212.0°F", "passed": f_100 == 212.0},
    {"name": "c_32 — 32°F верно переведены в 0.0°C", "passed": c_32 == 0.0},
    {"name": "roundtrip — обратное преобразование возвращает исходное значение", "passed": roundtrip == 37.0},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
