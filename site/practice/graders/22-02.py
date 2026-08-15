checks = [
    {"name": "html_bez_stilej — содержит заголовок <h1>", "passed": "<h1>" in html_bez_stilej},
    {"name": "html_bez_stilej — содержит оба пункта списка", "passed": "<li>Учу Python</li>" in html_bez_stilej and "<li>Учу HTML</li>" in html_bez_stilej},
    {"name": "html_so_stilyami — содержит блок <style>", "passed": "<style>" in html_so_stilyami},
    {"name": "html_svoj_stil — добавлено правило зелёного текста", "passed": "color: green" in html_svoj_stil},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
