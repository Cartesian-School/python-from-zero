checks = [
    {"name": "kvadraty_chetnyh — квадраты чётных чисел 1..10", "passed": kvadraty_chetnyh == [4, 16, 36, 64, 100]},
    {"name": "bukvy — уникальные строчные буквы 'Programming'", "passed": bukvy == set("programming")},
    {"name": "slovar_dlin — словарь «слово → длина»", "passed": slovar_dlin == {"python": 6, "git": 3, "sql": 3}},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
