p_fresh = Player("Fresh")
p_fresh.take_damage(150)

checks = [
    {"name": "p.health — 100 минус 30 урона", "passed": p.health == 70},
    {"name": "p.score — начислено 15 очков", "passed": p.score == 15},
    {"name": "p.is_alive() — True при положительном health", "passed": p.is_alive() is True},
    {"name": "take_damage — не уходит ниже 0", "passed": p_fresh.health == 0},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
