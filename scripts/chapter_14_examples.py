"""EXAMPLES for Chapter 14's real-Turtle-output pipeline (see
turtle_output_lib.py). Every entry is a complete runnable script — creates
`screen = turtle.Screen()` (exact name, required by the shared runner),
draws, and deliberately omits exitonclick()/bye() (added by the runner).

Chapter 14 is the OOP chapter. Both examples wrap turtle.Turtle objects
inside a custom class (composition — "HAS-A turtle", never subclassing
Turtle itself):

  14-gonka-obektov — the 14-04 project's Uchastnik class (one turtle per
  racer, a random step each turn) frozen at its final finish-line frame.

  14-gonka-v2 — the 14-26 extension: a Gonka ("Race") class that OWNS a
  list of Uchastnik objects and a finish line, drawing the finish line
  itself and reporting standings — objects collaborating with objects.
"""

EXAMPLES: dict[str, str] = {
    "14-gonka-obektov": (
        'import turtle\n'
        'import random\n\n'
        'random.seed(5)\n'
        'screen = turtle.Screen()\n'
        'screen.setup(500, 400)\n\n'
        'class Uchastnik:\n'
        '    def __init__(self, cvet, startovyj_y):\n'
        '        self.t = turtle.Turtle()\n'
        '        self.t.shape("turtle")\n'
        '        self.t.color(cvet)\n'
        '        self.t.penup()\n'
        '        self.t.goto(-200, startovyj_y)\n'
        '        self.cvet = cvet\n\n'
        '    def sdelat_shag(self):\n'
        '        self.t.forward(random.randint(1, 10))\n\n'
        '    def finishiroval(self, finish_line):\n'
        '        return self.t.xcor() >= finish_line\n\n'
        'cveta = ["red", "blue", "green", "orange"]\n'
        'uchastniki = [Uchastnik(cvet, i * 40 - 60) for i, cvet in enumerate(cveta)]\n\n'
        'pobeditel = None\n'
        'while pobeditel is None:\n'
        '    for u in uchastniki:\n'
        '        u.sdelat_shag()\n'
        '        if u.finishiroval(200):\n'
        '            pobeditel = u.cvet\n'
        '            break\n'
    ),
    "14-gonka-v2": (
        'import turtle\n'
        'import random\n\n'
        'random.seed(7)\n'
        'screen = turtle.Screen()\n'
        'screen.setup(520, 420)\n\n'
        'class Uchastnik:\n'
        '    def __init__(self, cvet, startovyj_y):\n'
        '        self.t = turtle.Turtle()\n'
        '        self.t.shape("turtle")\n'
        '        self.t.color(cvet)\n'
        '        self.t.penup()\n'
        '        self.t.goto(-220, startovyj_y)\n'
        '        self.cvet = cvet\n'
        '        self.finishiroval = False\n\n'
        '    def sdelat_shag(self):\n'
        '        if not self.finishiroval:\n'
        '            self.t.forward(random.randint(1, 10))\n\n'
        '    def proverit_finish(self, finish_x):\n'
        '        if self.t.xcor() >= finish_x:\n'
        '            self.finishiroval = True\n'
        '        return self.finishiroval\n\n\n'
        'class Gonka:\n'
        '    def __init__(self, cveta, finish_x):\n'
        '        self.finish_x = finish_x\n'
        '        self.uchastniki = [\n'
        '            Uchastnik(cvet, i * 50 - 75) for i, cvet in enumerate(cveta)\n'
        '        ]\n'
        '        self.rezultaty = []\n\n'
        '    def narisovat_finish(self):\n'
        '        liniya = turtle.Turtle()\n'
        '        liniya.hideturtle()\n'
        '        liniya.penup()\n'
        '        liniya.goto(self.finish_x, -120)\n'
        '        liniya.pendown()\n'
        '        liniya.pencolor("#0D0230")\n'
        '        liniya.pensize(3)\n'
        '        liniya.setheading(90)\n'
        '        liniya.forward(240)\n\n'
        '    def sygrat_do_kontsa(self):\n'
        '        self.narisovat_finish()\n'
        '        while len(self.rezultaty) < len(self.uchastniki):\n'
        '            for u in self.uchastniki:\n'
        '                u.sdelat_shag()\n'
        '                if u.proverit_finish(self.finish_x) and u.cvet not in self.rezultaty:\n'
        '                    self.rezultaty.append(u.cvet)\n\n'
        'gonka = Gonka(["red", "blue", "green"], 210)\n'
        'gonka.sygrat_do_kontsa()\n'
    ),
}
