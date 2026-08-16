"""Единый источник правды для примеров Turtle в главе 6.

Каждая запись EXAMPLES[name] — это ЗАВЕРШЁННЫЙ код на turtle (import,
создание screen/artist, команды рисования), БЕЗ финального
screen.exitonclick()/screen.bye() — это единственное, что отличается между
двумя потребителями одного и того же кода:

  - scripts/build_chapter_06.py показывает этот код читателю через
    code_block(), сам дописывая `screen.exitonclick()` в конце — так, как
    выглядел бы код, если запустить его локально.
  - scripts/generate_chapter_06_outputs.py выполняет ЭТОТ ЖЕ код headless
    (Xvfb), затем экспортирует холст в PNG и сохраняет в
    site/assets/img/chapter-06/output/<name>.png — так на странице рядом с
    кодом оказывается по-настоящему выполненный результат, а не картинка
    "как бы должно получиться".

Это гарантирует, что показанный код и показанная картинка никогда не
разойдутся — они в буквальном смысле одна и та же строка.
"""

EXAMPLES: dict[str, str] = {
    # --- 06-01 · приступаем ---
    "06-01-screen-turtle": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=480, height=360)\n'
        'artist = turtle.Turtle()\n'
    ),
    # --- 06-09 · координаты ---
    "06-09-axes": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=480, height=480)\n'
        'artist = turtle.Turtle()\n'
        'artist.hideturtle()\n'
        'artist.speed(0)\n\n'
        '# ось X\n'
        'artist.penup(); artist.goto(-200, 0); artist.pendown()\n'
        'artist.pencolor("#0D0230"); artist.pensize(2)\n'
        'artist.goto(200, 0)\n\n'
        '# ось Y\n'
        'artist.penup(); artist.goto(0, -200); artist.pendown()\n'
        'artist.goto(0, 200)\n\n'
        '# отметим начало координат и одну точку\n'
        'artist.penup(); artist.goto(0, 0)\n'
        'artist.dot(10, "#5B24F9")\n'
        'artist.goto(120, 80)\n'
        'artist.dot(10, "#5B24F9")\n'
        'artist.write("  (120, 80)", font=("Arial", 12, "normal"))\n'
        'artist.goto(0, -20)\n'
        'artist.write("  (0, 0)", font=("Arial", 12, "normal"))\n'
    ),
    # --- 06-02 · движение вперёд и назад ---
    "06-02-forward-120": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=480, height=300)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(3)\n'
        'artist.pencolor("#5B24F9")\n\n'
        'artist.forward(120)\n'
    ),
    "06-02-forward-backward": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=480, height=300)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(3)\n'
        'artist.pencolor("#5B24F9")\n\n'
        'artist.forward(120)\n'
        'artist.backward(50)\n'
    ),
    "06-02-letter-g": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=480, height=360)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(3)\n'
        'artist.pencolor("#5B24F9")\n\n'
        'artist.forward(120)\n'
        'artist.left(90)\n'
        'artist.forward(80)\n'
    ),
    # --- 06-10 · направление и угол ---
    "06-10-heading-states": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=480, height=480)\n'
        'artist = turtle.Turtle()\n'
        'artist.shape("classic")\n'
        'artist.speed(0)\n'
        'artist.penup()\n\n'
        'headings = [(0, "0°  восток"), (90, "90°  север"), (180, "180°  запад"), (270, "270°  юг")]\n'
        'colors = ["#5B24F9", "#DB2777", "#059669", "#D97706"]\n'
        'for (angle, label), color in zip(headings, colors):\n'
        '    artist.setheading(angle)\n'
        '    artist.goto(0, 0)\n'
        '    artist.pencolor(color)\n'
        '    artist.pendown()\n'
        '    artist.forward(90)\n'
        '    artist.penup()\n'
        '    artist.write("  " + label, font=("Arial", 11, "normal"))\n'
        '    artist.goto(0, 0)\n'
    ),
    # --- 06-03 · setheading/home ---
    "06-03-setheading-home": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=480, height=400)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(3)\n'
        'artist.pencolor("#5B24F9")\n\n'
        'artist.setheading(90)\n'
        'artist.forward(100)\n\n'
        'artist.setheading(180)\n'
        'artist.forward(100)\n'
    ),
    # --- 06-11 · первые фигуры ---
    "06-11-triangle": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=480, height=400)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(3)\n'
        'artist.pencolor("#5B24F9")\n\n'
        'artist.forward(120)\n'
        'artist.right(120)\n'
        'artist.forward(120)\n'
        'artist.right(120)\n'
        'artist.forward(120)\n'
        'artist.right(120)\n'
    ),
    "06-11-rectangle": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=480, height=360)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(3)\n'
        'artist.pencolor("#5B24F9")\n\n'
        'artist.forward(160)\n'
        'artist.right(90)\n'
        'artist.forward(90)\n'
        'artist.right(90)\n'
        'artist.forward(160)\n'
        'artist.right(90)\n'
        'artist.forward(90)\n'
        'artist.right(90)\n'
    ),
    "06-11-pentagon": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=480, height=440)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(3)\n'
        'artist.pencolor("#5B24F9")\n\n'
        'artist.forward(90)\n'
        'artist.right(72)\n'
        'artist.forward(90)\n'
        'artist.right(72)\n'
        'artist.forward(90)\n'
        'artist.right(72)\n'
        'artist.forward(90)\n'
        'artist.right(72)\n'
        'artist.forward(90)\n'
        'artist.right(72)\n'
    ),
    # --- 06-04 · мини-проекты: квадрат и шестиугольник ---
    "06-04-kvadrat": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=400, height=400)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(3)\n'
        'artist.pencolor("#5B24F9")\n\n'
        'artist.forward(100)\n'
        'artist.right(90)\n'
        'artist.forward(100)\n'
        'artist.right(90)\n'
        'artist.forward(100)\n'
        'artist.right(90)\n'
        'artist.forward(100)\n'
        'artist.right(90)\n'
    ),
    "06-04-shestiugolnik": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=420, height=400)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(3)\n'
        'artist.pencolor("#5B24F9")\n\n'
        'artist.forward(80)\n'
        'artist.right(60)\n'
        'artist.forward(80)\n'
        'artist.right(60)\n'
        'artist.forward(80)\n'
        'artist.right(60)\n'
        'artist.forward(80)\n'
        'artist.right(60)\n'
        'artist.forward(80)\n'
        'artist.right(60)\n'
        'artist.forward(80)\n'
        'artist.right(60)\n'
    ),
    # --- 06-05 · сокращённые приёмы ---
    "06-05-oformlenie": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=420, height=300)\n'
        'artist = turtle.Turtle()\n\n'
        'artist.pencolor("purple")\n'
        'artist.pensize(6)\n'
        'artist.fd(200)\n'
    ),
    # --- 06-12 · перо вверх/вниз ---
    "06-12-pen-up-down": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=480, height=260)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(3)\n'
        'artist.pencolor("#5B24F9")\n\n'
        'artist.forward(60)      # перо опущено — рисует\n'
        'artist.penup()\n'
        'artist.forward(60)      # перо поднято — просто перемещение, без линии\n'
        'artist.pendown()\n'
        'artist.forward(60)      # перо снова опущено — рисует\n'
    ),
    # --- 06-07 · goto и координатная панель ---
    "06-07-goto-square": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=400, height=400)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(3)\n'
        'artist.pencolor("#5B24F9")\n\n'
        'artist.goto(100, 0)\n'
        'artist.goto(100, 100)\n'
        'artist.goto(0, 100)\n'
        'artist.goto(0, 0)\n'
    ),
    "06-07-navigation": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=480, height=360)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(3)\n'
        'artist.pencolor("#5B24F9")\n\n'
        'artist.penup()\n'
        'artist.dot(8, "#B9A0FC")\n'
        'artist.write("  старт (0, 0)", font=("Arial", 11, "normal"))\n'
        'artist.setx(150)\n'
        'artist.sety(80)\n'
        'artist.dot(8, "#5B24F9")\n'
        'artist.write("  после setx(150), sety(80)", font=("Arial", 11, "normal"))\n'
    ),
    # --- 06-13 · цвет, толщина, вид ---
    "06-13-thin-black": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=380, height=200)\n'
        'artist = turtle.Turtle()\n\n'
        'artist.pensize(1)\n'
        'artist.pencolor("black")\n'
        'artist.forward(220)\n'
    ),
    "06-13-thick-blue": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=380, height=200)\n'
        'artist = turtle.Turtle()\n\n'
        'artist.pensize(10)\n'
        'artist.pencolor("#2563EB")\n'
        'artist.forward(220)\n'
    ),
    "06-13-shape-bgcolor": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=380, height=300)\n'
        'screen.bgcolor("#FAFAFC")\n'
        'artist = turtle.Turtle()\n'
        'artist.shape("turtle")\n'
        'artist.pencolor("#5B24F9")\n'
        'artist.pensize(2)\n'
        'artist.forward(120)\n'
        'artist.left(90)\n'
        'artist.forward(60)\n'
    ),
    # --- 06-14 · заливка, круг, дуга, точка ---
    "06-14-outline-triangle": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=380, height=360)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(3)\n'
        'artist.pencolor("#5B24F9")\n\n'
        'artist.forward(140)\n'
        'artist.left(120)\n'
        'artist.forward(140)\n'
        'artist.left(120)\n'
        'artist.forward(140)\n'
        'artist.left(120)\n'
    ),
    "06-14-filled-triangle": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=380, height=360)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(3)\n'
        'artist.pencolor("#5B24F9")\n'
        'artist.fillcolor("#B9A0FC")\n\n'
        'artist.begin_fill()\n'
        'artist.forward(140)\n'
        'artist.left(120)\n'
        'artist.forward(140)\n'
        'artist.left(120)\n'
        'artist.forward(140)\n'
        'artist.left(120)\n'
        'artist.end_fill()\n'
    ),
    "06-14-circle": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=380, height=380)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(3)\n'
        'artist.pencolor("#5B24F9")\n\n'
        'artist.circle(80)\n'
    ),
    "06-14-arc": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=380, height=300)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(3)\n'
        'artist.pencolor("#5B24F9")\n\n'
        'artist.circle(80, 90)\n'
    ),
    "06-14-dots": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=380, height=260)\n'
        'artist = turtle.Turtle()\n'
        'artist.hideturtle()\n'
        'artist.penup()\n\n'
        'artist.goto(-100, 0); artist.dot(20, "#5B24F9")\n'
        'artist.goto(0, 0); artist.dot(30, "#DB2777")\n'
        'artist.goto(100, 0); artist.dot(40, "#059669")\n'
    ),
    # --- 06-06 · случайные точки ---
    "06-06-random-points": (
        'import turtle\n'
        'import random\n\n'
        'random.seed(7)\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=420, height=340)\n'
        'artist = turtle.Turtle()\n'
        'artist.hideturtle()\n'
        'artist.penup()\n\n'
        'for _ in range(10):\n'
        '    x = random.randint(-200, 200)\n'
        '    y = random.randint(-150, 150)\n'
        '    artist.goto(x, y)\n'
        '    artist.dot(14, "#5B24F9")\n'
    ),
    # --- 06-15 · случайное движение ---
    "06-15-random-walk": (
        'import turtle\n'
        'import random\n\n'
        'random.seed(3)\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=420, height=420)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(2)\n'
        'artist.pencolor("#5B24F9")\n'
        'artist.speed(0)\n\n'
        'for _ in range(40):\n'
        '    artist.forward(15)\n'
        '    artist.right(random.randint(-60, 60))\n'
    ),
    # --- 06-16 · рисуем по координатам ---
    "06-16-triangle-mark": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=380, height=380)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(3)\n'
        'artist.pencolor("#5B24F9")\n'
        'artist.fillcolor("#B9A0FC")\n'
        'artist.penup()\n'
        'artist.goto(-60, -50)\n'
        'artist.pendown()\n\n'
        'artist.begin_fill()\n'
        'artist.goto(60, -50)\n'
        'artist.goto(0, 70)\n'
        'artist.goto(-60, -50)\n'
        'artist.end_fill()\n'
    ),
    # --- 06-18 · мини-проекты ---
    "06-18-house": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=420, height=420)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(3)\n'
        'artist.speed(0)\n\n'
        '# стены\n'
        'artist.penup(); artist.goto(-80, -80); artist.pendown()\n'
        'artist.pencolor("#5B24F9"); artist.fillcolor("#EDE9FE")\n'
        'artist.begin_fill()\n'
        'for _ in range(4):\n'
        '    artist.forward(160)\n'
        '    artist.left(90)\n'
        'artist.end_fill()\n\n'
        '# крыша\n'
        'artist.penup(); artist.goto(-100, 80); artist.pendown()\n'
        'artist.pencolor("#B91C1C"); artist.fillcolor("#FCA5A5")\n'
        'artist.begin_fill()\n'
        'artist.goto(0, 160)\n'
        'artist.goto(100, 80)\n'
        'artist.goto(-100, 80)\n'
        'artist.end_fill()\n\n'
        '# дверь\n'
        'artist.penup(); artist.goto(-20, -80); artist.pendown()\n'
        'artist.pencolor("#78350F"); artist.fillcolor("#92400E")\n'
        'artist.begin_fill()\n'
        'for _ in range(2):\n'
        '    artist.forward(40)\n'
        '    artist.left(90)\n'
        '    artist.forward(70)\n'
        '    artist.left(90)\n'
        'artist.end_fill()\n'
    ),
    "06-18-target": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=380, height=380)\n'
        'artist = turtle.Turtle()\n'
        'artist.speed(0)\n'
        'artist.hideturtle()\n\n'
        'rings = [(90, "#DC2626"), (65, "#FAFAFC"), (40, "#DC2626"), (15, "#FAFAFC")]\n'
        'for radius, color in rings:\n'
        '    artist.penup()\n'
        '    artist.goto(0, -radius)\n'
        '    artist.pendown()\n'
        '    artist.fillcolor(color)\n'
        '    artist.pencolor("#0D0230")\n'
        '    artist.begin_fill()\n'
        '    artist.circle(radius)\n'
        '    artist.end_fill()\n'
    ),
    "06-18-starry-sky": (
        'import turtle\n'
        'import random\n\n'
        'random.seed(11)\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=420, height=340)\n'
        'screen.bgcolor("#0D0230")\n'
        'artist = turtle.Turtle()\n'
        'artist.hideturtle()\n'
        'artist.penup()\n\n'
        'for _ in range(35):\n'
        '    x = random.randint(-200, 200)\n'
        '    y = random.randint(-150, 150)\n'
        '    size = random.choice([6, 8, 10])\n'
        '    artist.goto(x, y)\n'
        '    artist.dot(size, "#FDE68A")\n'
    ),
    "06-18-star-pattern": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=380, height=380)\n'
        'artist = turtle.Turtle()\n'
        'artist.pensize(3)\n'
        'artist.pencolor("#5B24F9")\n'
        'artist.speed(0)\n\n'
        'artist.forward(150)\n'
        'artist.right(144)\n'
        'artist.forward(150)\n'
        'artist.right(144)\n'
        'artist.forward(150)\n'
        'artist.right(144)\n'
        'artist.forward(150)\n'
        'artist.right(144)\n'
        'artist.forward(150)\n'
        'artist.right(144)\n'
    ),
    # --- 06-08 · мандала и итоги ---
    "06-08-motif": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=420, height=420)\n'
        'artist = turtle.Turtle()\n'
        'artist.speed(0)\n'
        'artist.pencolor("#5B24F9")\n\n'
        'shag_ugla = 10\n'
        'ugol = 0\n'
        'while ugol < 60:\n'
        '    artist.setheading(ugol)\n'
        '    artist.forward(150)\n'
        '    artist.backward(150)\n'
        '    ugol += shag_ugla\n'
    ),
    "06-08-mandala-full": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=420, height=420)\n'
        'artist = turtle.Turtle()\n'
        'artist.speed(0)\n'
        'artist.pencolor("#5B24F9")\n\n'
        'shag_ugla = 10\n'
        'ugol = 0\n'
        'while ugol < 360:\n'
        '    artist.setheading(ugol)\n'
        '    artist.forward(150)\n'
        '    artist.backward(150)\n'
        '    ugol += shag_ugla\n'
    ),
}
