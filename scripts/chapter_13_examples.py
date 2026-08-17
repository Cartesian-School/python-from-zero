"""EXAMPLES for Chapter 13's real-Turtle-output pipeline (see
turtle_output_lib.py). Every entry is a complete runnable script — creates
`screen = turtle.Screen()` (exact name, required by the shared runner),
draws, and deliberately omits exitonclick()/bye() (added by the runner).

Chapter 13's Turtle Function Studio (13-08) turns the repeated shape-drawing
code from chapters 6/10/12 into one reusable draw_polygon(artist, sides,
length) function — these two examples show it called once directly, and
then called repeatedly inside a loop with a changing `sides` argument to
produce a rotated fan of polygons (loop + function + changing parameter,
all three working together).
"""

EXAMPLES: dict[str, str] = {
    # --- одна функция, один вызов ---
    "13-polygon-function": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=300, height=300)\n'
        'artist = turtle.Turtle()\n'
        'artist.speed(0)\n'
        'artist.pencolor("#5B24F9")\n'
        'artist.pensize(3)\n\n'
        'def draw_polygon(artist, sides, length):\n'
        '    angle = 360 / sides\n'
        '    for _ in range(sides):\n'
        '        artist.forward(length)\n'
        '        artist.right(angle)\n\n'
        'draw_polygon(artist, 6, 80)\n'
    ),
    # --- та же функция, вызванная в цикле с меняющимся sides ---
    "13-polygon-scene": (
        'import turtle\n\n'
        'screen = turtle.Screen()\n'
        'screen.setup(width=420, height=420)\n'
        'artist = turtle.Turtle()\n'
        'artist.speed(0)\n'
        'artist.pensize(2)\n\n'
        'def draw_polygon(artist, sides, length):\n'
        '    angle = 360 / sides\n'
        '    for _ in range(sides):\n'
        '        artist.forward(length)\n'
        '        artist.right(angle)\n\n'
        'cveta = ["#5B24F9", "#DB2777", "#059669"]\n'
        'for i, sides in enumerate(range(3, 9)):\n'
        '    artist.pencolor(cveta[i % 3])\n'
        '    draw_polygon(artist, sides, 70)\n'
        '    artist.right(15)\n'
    ),
}
