"""EXAMPLES for Chapter 10's real-Turtle-output pipeline (see
turtle_output_lib.py). Every entry is a complete runnable script — creates
`screen = turtle.Screen()` (exact name, required by the shared runner),
draws, and deliberately omits exitonclick()/bye() (added by the runner).

Chapter 10 is about automating the shapes from Chapters 6-7 with loops —
these examples ARE the automated (loop) versions; the "before" (repeated,
non-loop) code shown alongside them on the page produces the identical
geometry, so it reuses the same generated image rather than wastefully
re-rendering a pixel-identical picture.
"""

EXAMPLES: dict[str, str] = {
    # --- квадрат: до/после (одна и та же геометрия) ---
    "10-square": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=300, height=300)\n'
        'artist = turtle.Turtle()\n'
        'artist.speed(0)\n'
        'artist.pencolor("#5B24F9")\n'
        'artist.pensize(3)\n\n'
        'for _ in range(4):\n'
        '    artist.forward(100)\n'
        '    artist.right(90)\n'
    ),
    # --- универсальный многоугольник: одна формула, разное число сторон ---
    "10-polygon-3": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=300, height=300)\n'
        'artist = turtle.Turtle()\n'
        'artist.speed(0)\n'
        'artist.pencolor("#5B24F9")\n'
        'artist.pensize(3)\n\n'
        'storony = 3\n'
        'dlina = 110\n'
        'ugol = 360 / storony\n\n'
        'for _ in range(storony):\n'
        '    artist.forward(dlina)\n'
        '    artist.right(ugol)\n'
    ),
    "10-polygon-5": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=300, height=300)\n'
        'artist = turtle.Turtle()\n'
        'artist.speed(0)\n'
        'artist.pencolor("#5B24F9")\n'
        'artist.pensize(3)\n\n'
        'storony = 5\n'
        'dlina = 75\n'
        'ugol = 360 / storony\n\n'
        'for _ in range(storony):\n'
        '    artist.forward(dlina)\n'
        '    artist.right(ugol)\n'
    ),
    "10-polygon-6": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=300, height=300)\n'
        'artist = turtle.Turtle()\n'
        'artist.speed(0)\n'
        'artist.pencolor("#5B24F9")\n'
        'artist.pensize(3)\n\n'
        'storony = 6\n'
        'dlina = 65\n'
        'ugol = 360 / storony\n\n'
        'for _ in range(storony):\n'
        '    artist.forward(dlina)\n'
        '    artist.right(ugol)\n'
    ),
    "10-polygon-8": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=300, height=300)\n'
        'artist = turtle.Turtle()\n'
        'artist.speed(0)\n'
        'artist.pencolor("#5B24F9")\n'
        'artist.pensize(3)\n\n'
        'storony = 8\n'
        'dlina = 55\n'
        'ugol = 360 / storony\n\n'
        'for _ in range(storony):\n'
        '    artist.forward(dlina)\n'
        '    artist.right(ugol)\n'
    ),
    # --- мандала: стадии повторения (circle() без остатка возвращает черепашку в старт) ---
    "10-mandala-1": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=300, height=300)\n'
        'artist = turtle.Turtle()\n'
        'artist.speed(0)\n'
        'artist.pencolor("#5B24F9")\n'
        'artist.pensize(2)\n\n'
        'artist.circle(60)\n'
    ),
    "10-mandala-4": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=300, height=300)\n'
        'artist = turtle.Turtle()\n'
        'artist.speed(0)\n'
        'artist.pencolor("#5B24F9")\n'
        'artist.pensize(2)\n\n'
        'for _ in range(4):\n'
        '    artist.circle(60)\n'
        '    artist.left(90)\n'
    ),
    "10-mandala-12": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=300, height=300)\n'
        'artist = turtle.Turtle()\n'
        'artist.speed(0)\n'
        'artist.pencolor("#5B24F9")\n'
        'artist.pensize(1)\n\n'
        'for _ in range(12):\n'
        '    artist.circle(60)\n'
        '    artist.left(30)\n'
    ),
    "10-mandala-full": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=340, height=340)\n'
        'artist = turtle.Turtle()\n'
        'artist.speed(0)\n'
        'artist.pensize(1)\n\n'
        'cvieta = ["#5B24F9", "#DB2777", "#059669"]\n'
        'for i in range(24):\n'
        '    artist.pencolor(cvieta[i % 3])\n'
        '    artist.circle(80)\n'
        '    artist.left(15)\n'
    ),
    # --- случайные автоматизации ---
    "10-random-walk": (
        'import turtle\n'
        'import random\n\n'
        'random.seed(7)\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=420, height=420)\n'
        'artist = turtle.Turtle()\n'
        'artist.speed(0)\n'
        'artist.pencolor("#5B24F9")\n'
        'artist.pensize(2)\n\n'
        'for _ in range(100):\n'
        '    artist.setheading(random.randint(0, 360))\n'
        '    artist.forward(10)\n'
    ),
    "10-star-field": (
        'import turtle\n'
        'import random\n\n'
        'random.seed(3)\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=420, height=420)\n'
        'screen.bgcolor("#0D0230")\n'
        'artist = turtle.Turtle()\n'
        'artist.speed(0)\n'
        'artist.hideturtle()\n'
        'artist.penup()\n\n'
        'for _ in range(60):\n'
        '    x = random.randint(-190, 190)\n'
        '    y = random.randint(-190, 190)\n'
        '    artist.goto(x, y)\n'
        '    artist.dot(6, "white")\n'
    ),
    # --- вложенные циклы: сетка ---
    "10-grid": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=380, height=380)\n'
        'artist = turtle.Turtle()\n'
        'artist.speed(0)\n'
        'artist.hideturtle()\n'
        'artist.penup()\n\n'
        'shag = 60\n'
        'for row in range(5):\n'
        '    for col in range(5):\n'
        '        x = -140 + col * shag\n'
        '        y = -140 + row * shag\n'
        '        artist.goto(x, y)\n'
        '        artist.dot(16, "#5B24F9")\n'
    ),
    # --- спираль из дуг ---
    "10-spiral": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=420, height=420)\n'
        'artist = turtle.Turtle()\n'
        'artist.speed(0)\n'
        'artist.pencolor("#5B24F9")\n'
        'artist.pensize(2)\n\n'
        'radius = 5\n'
        'for _ in range(60):\n'
        '    artist.circle(radius, 90)\n'
        '    radius += 3\n'
    ),
    # --- break в Turtle: рисуем сегменты, пока не выйдем за границу ---
    "10-break-turtle": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=420, height=420)\n'
        'artist = turtle.Turtle()\n'
        'artist.speed(0)\n'
        'artist.pencolor("#5B24F9")\n'
        'artist.pensize(3)\n\n'
        'dlina = 10\n'
        'for _ in range(50):\n'
        '    if artist.xcor() > 150:\n'
        '        break\n'
        '    artist.forward(dlina)\n'
        '    artist.left(90)\n'
        '    dlina += 6\n'
    ),
}
