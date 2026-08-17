checks = [
    {"name": "udalit_tovar — товар удалён из корзины", "passed": korzina.kolichestvo_tovarov() == 1},
    {"name": "obshchaya_summa — пересчиталась после удаления", "passed": korzina.obshchaya_summa() == 590},
    {"name": "udalit_tovar — возвращает False, если товара нет", "passed": korzina.udalit_tovar("Несуществующий") is False},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
