#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 20 (Pygame).

Важно: в обычном .py-файле игровой цикл — while с условием, зависящим от событий
пользователя (например, закрытия окна). В автоматически выполняемом ноутбуке нет
живого пользователя, поэтому здесь мы вместо `while rabotaet:` прогоняем цикл
фиксированное число кадров (`for _ in range(N)`) — сама логика кадра (движение,
отрисовка, tick) при этом остаётся ровно той же.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-20"

LOOP_NOTE_MD = (
    "## Про игровой цикл в этом ноутбуке\n\n"
    "В обычном `.py`-файле игровой цикл — это `while rabotaet:`, где `rabotaet` становится "
    "`False`, когда пользователь закрывает окно. В автоматически выполняемом ноутбуке некому "
    "закрыть окно, поэтому здесь мы прогоняем фиксированное число кадров через "
    "`for _ in range(N):` — логика каждого отдельного кадра (движение, отрисовка, "
    "`clock.tick()`) при этом точно такая же, как в настоящей игре."
)


def build_02() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-02 · Игровой экран\n\nПрактика к разделу "
          "[«Настраиваем игровой экран! Делаем экран красивым»](../../site/chapters/glava-20/20-02-igrovoj-ekran.html).")
    nb.md("## Цель\n\nСоздать экран Pygame и прогнать несколько кадров игрового цикла.")
    nb.md(LOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Моя первая игра")
clock = pygame.time.Clock()

CVET_FONA = (20, 20, 40)

for kadr in range(5):
    for event in pygame.event.get():
        pass  # в этом примере события пока не обрабатываем

    screen.fill(CVET_FONA)
    pygame.display.flip()
    clock.tick(60)

print("5 кадров отрисовано.")
print("Цвет фона в углу экрана:", screen.get_at((0, 0)))
pygame.quit()''')
    nb.md("## Проверка результата")
    nb.code('''import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
screen.fill((20, 20, 40))
pygame.display.flip()

assert screen.get_at((0, 0))[:3] == (20, 20, 40)
print("Верно: экран залит нужным цветом.")
pygame.quit()''')
    nb.write(OUT_DIR / "20-02-ekran.ipynb")
    print(f"Записано: 20-02 ({len(nb)} ячеек)")


def build_03() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-03 · Персонажи\n\nПрактика к разделу "
          "[«Создаём персонажей на экране»](../../site/chapters/glava-20/20-03-personazhi.html).")
    nb.md("## Цель\n\nНарисовать персонажей простыми фигурами.")
    nb.md("## Рабочий пример")
    nb.code('''import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))

CVET_IGROKA = (100, 200, 255)
CVET_VRAGA = (255, 80, 80)

x_igroka, y_igroka = 300, 350
x_vraga, y_vraga = 300, 50

screen.fill((0, 0, 0))
pygame.draw.rect(screen, CVET_IGROKA, (x_igroka, y_igroka, 40, 40))
pygame.draw.circle(screen, CVET_VRAGA, (x_vraga, y_vraga), 20)
pygame.display.flip()

print("Цвет в центре игрока:", screen.get_at((x_igroka + 20, y_igroka + 20)))
print("Цвет в центре врага:", screen.get_at((x_vraga, y_vraga)))
pygame.quit()''')
    nb.md("## Проверка результата")
    nb.code('''import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
screen.fill((0, 0, 0))
pygame.draw.rect(screen, (100, 200, 255), (300, 350, 40, 40))
pygame.display.flip()

assert screen.get_at((320, 370))[:3] == (100, 200, 255)
print("Верно: прямоугольник игрока нарисован правильным цветом.")
pygame.quit()''')
    nb.md("## Задание ★ Базовая практика\n\nНарисуйте трёх врагов в ряд разными цветами.")
    nb.code('''import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
screen.fill((0, 0, 0))

cveta = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
for i, cvet in enumerate(cveta):
    pygame.draw.circle(screen, cvet, (150 + i * 150, 100), 20)

pygame.display.flip()
print("Три врага нарисованы.")
pygame.quit()''')
    nb.write(OUT_DIR / "20-03-personazhi.ipynb")
    print(f"Записано: 20-03 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-04 · Движение и клавиши\n\nПрактика к разделу "
          "[«Перемещаем персонажей. События клавиш»](../../site/chapters/glava-20/20-04-peremeshenie-klavishi.html).")
    nb.md("## Цель\n\nДвигать персонажа изменением координат и обработать событие клавиши.")
    nb.md(LOOP_NOTE_MD)
    nb.md("## Рабочий пример — движение")
    nb.code('''import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

x_igroka = 50
skorost_x = 5

for kadr in range(10):
    x_igroka += skorost_x
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (100, 200, 255), (x_igroka, 180, 40, 40))
    pygame.display.flip()
    clock.tick(60)

print("Позиция игрока после 10 кадров:", x_igroka)
pygame.quit()''')
    nb.md("## Проверка результата")
    nb.code('''assert x_igroka == 50 + 5 * 10
print("Верно: игрок сдвинулся на", 5 * 10, "пикселей за 10 кадров.")''')
    nb.md("## Эксперимент 1 — событие KEYDOWN")
    nb.code('''import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))

# программно создаём событие нажатия клавиши, как это сделала бы клавиатура
sobytie = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
pygame.event.post(sobytie)

for event in pygame.event.get():
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        print("Прыжок! (клавиша SPACE обработана)")

pygame.quit()''')
    nb.md("## Эксперимент 2 — get_pressed() для непрерывного движения")
    nb.code('''import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))

klavishi = pygame.key.get_pressed()
# в реальном приложении это будет True, если клавиша действительно зажата;
# здесь просто проверяем, что функция возвращает объект, с которым можно так работать
print("Тип результата get_pressed():", type(klavishi))
print("Стрелка влево зажата:", klavishi[pygame.K_LEFT])
pygame.quit()''')
    nb.write(OUT_DIR / "20-04-dvizhenie-klavishi.ipynb")
    print(f"Записано: 20-04 ({len(nb)} ячеек)")


def build_05() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-05 · Прыгающий мяч\n\nПрактика к разделу "
          "[«Мини-проект — прыгающий мяч»](../../site/chapters/glava-20/20-05-mini-proekt-myach-itogi.html). "
          "Тот же код, что и в `projects/pygame/bouncing-ball/bouncing_ball.py`.")
    nb.md("## Цель\n\nСобрать и протестировать мяч, отскакивающий от стен.")
    nb.md(LOOP_NOTE_MD)
    nb.md("## Полный мини-проект")
    nb.code('''import pygame

SHIRINA, VYSOTA = 600, 400
RADIUS = 20

pygame.init()
screen = pygame.display.set_mode((SHIRINA, VYSOTA))
clock = pygame.time.Clock()

x, y = SHIRINA // 2, VYSOTA // 2
dx, dy = 4, 3

otskokov = 0

for kadr in range(200):
    for event in pygame.event.get():
        pass

    x += dx
    y += dy

    if x - RADIUS < 0 or x + RADIUS > SHIRINA:
        dx = -dx
        otskokov += 1
    if y - RADIUS < 0 or y + RADIUS > VYSOTA:
        dy = -dy
        otskokov += 1

    screen.fill((20, 20, 40))
    pygame.draw.circle(screen, (255, 100, 100), (int(x), int(y)), RADIUS)
    pygame.display.flip()
    clock.tick(60)

print("Кадров прогнано: 200")
print("Отскоков от стен:", otskokov)
print("Финальная позиция:", (x, y))
pygame.quit()''')
    nb.md("## Проверка результата")
    nb.code('''assert otskokov > 0
print(f"Верно: мяч отскочил от стен {otskokov} раз(а) за 200 кадров.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nПроверьте, что мяч всегда остаётся в "
          "границах экрана на каждом кадре.")
    nb.code('''pygame.init()
screen = pygame.display.set_mode((SHIRINA, VYSOTA))
clock = pygame.time.Clock()

x, y = SHIRINA // 2, VYSOTA // 2
dx, dy = 7, 5  # быстрее — легче случайно "пробить" стену при ошибке в коде

vyshel_za_granicy = False
for kadr in range(300):
    x += dx
    y += dy
    if x - RADIUS < 0 or x + RADIUS > SHIRINA:
        dx = -dx
        x = max(RADIUS, min(x, SHIRINA - RADIUS))
    if y - RADIUS < 0 or y + RADIUS > VYSOTA:
        dy = -dy
        y = max(RADIUS, min(y, VYSOTA - RADIUS))

    if not (RADIUS <= x <= SHIRINA - RADIUS and RADIUS <= y <= VYSOTA - RADIUS):
        vyshel_za_granicy = True

print("Мяч когда-либо вышел за границы:", vyshel_za_granicy)
assert vyshel_za_granicy is False
print("Верно: мяч всегда оставался в пределах экрана.")
pygame.quit()''')
    nb.write(OUT_DIR / "20-05-myach.ipynb")
    print(f"Записано: 20-05 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_02()
    build_03()
    build_04()
    build_05()
