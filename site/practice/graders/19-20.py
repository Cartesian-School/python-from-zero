_snake = [(0, 0), (20, 0), (40, 0), (40, 20)]
_tail_move = move_snake(_snake, (40, 20), grow=False)
_middle_move = move_snake(_snake, (20, 0), grow=False)
_grow_move = move_snake(_snake, (40, 20), grow=True)

checks = [
    {"name": "заезд в клетку освободившегося хвоста легален", "passed": is_self_collision((40, 20), _tail_move[1:]) is False},
    {"name": "заезд в середину тела — столкновение", "passed": is_self_collision((20, 0), _middle_move[1:]) is True},
    {"name": "при росте хвост не освобождается — столкновение", "passed": is_self_collision((40, 20), _grow_move[1:]) is True},
]
passed = all(c["passed"] for c in checks)
{"passed": passed, "score": 100 if passed else 0, "checks": checks}
