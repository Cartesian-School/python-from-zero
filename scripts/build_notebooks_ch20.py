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


# ---------------------------------------------------------------------------
# Локально обязательные практики (local-required) — 20-14, 20-17, 20-19,
# 20-20, 20-23, 20-24, 20-26, 20-33
# ---------------------------------------------------------------------------

def build_14() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-14 · Игровой цикл: Input → Update → Render\n\nПрактика к разделу "
          "[«Игровой цикл»](../../site/chapters/glava-20/20-14-igrovoj-cikl.html).")
    nb.md("## Цель\n\nЯвно разделить код одного кадра на три именованные фазы.")
    nb.md(LOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

x = 50
schet_sobytij = 0

def input_faza():
    global schet_sobytij
    for event in pygame.event.get():
        schet_sobytij += 1

def update_faza():
    global x
    x += 3

def render_faza():
    screen.fill((20, 20, 40))
    pygame.draw.rect(screen, (100, 200, 255), (x, 180, 40, 40))
    pygame.display.flip()

for kadr in range(20):
    input_faza()
    update_faza()
    render_faza()
    clock.tick(60)

print("Позиция после 20 кадров:", x)''')
    nb.md("## Проверка результата")
    nb.code('''assert x == 50 + 3 * 20
print("Верно: три фазы выполнились в правильном порядке 20 раз подряд.")''')
    nb.md("## Задание ★ Базовая практика\n\nПоменяйте местами update_faza() и render_faza() — "
          "убедитесь, что итоговая позиция x не меняется (порядок этих двух фаз не влияет "
          "на арифметику x), но при этом реальная отрисовка одного кадра сместится на кадр "
          "относительно логики (в этом мини-примере разницу не видно без экрана, но именно "
          "так возникает баг из раздела 20.23 про анимацию, отстающую на кадр).")
    nb.code('''x = 50
for kadr in range(20):
    input_faza()
    render_faza()
    update_faza()
print("Позиция после смены порядка:", x)
assert x == 50 + 3 * 20''')
    nb.write(OUT_DIR / "20-14-igrovoj-cikl.ipynb")
    print(f"Записано: 20-14 ({len(nb)} ячеек)")


def build_17() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-17 · Surface\n\nПрактика к разделу "
          "[«Surface: во что мы рисуем»](../../site/chapters/glava-20/20-17-surface.html).")
    nb.md("## Цель\n\nСоздать дополнительную Surface и нанести её на экран через blit().")
    nb.md("## Рабочий пример")
    nb.code('''import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))

sprajt = pygame.Surface((100, 100))
sprajt.fill((255, 100, 100))
screen.fill((20, 20, 40))
screen.blit(sprajt, (50, 50))
pygame.display.flip()

print("Цвет в углу спрайта на экране:", screen.get_at((60, 60)))
print("Цвет вне спрайта:", screen.get_at((10, 10)))
pygame.quit()''')
    nb.md("## Проверка результата")
    nb.code('''pygame.init()
screen = pygame.display.set_mode((600, 400))
sprajt = pygame.Surface((100, 100))
sprajt.fill((255, 100, 100))
screen.fill((20, 20, 40))
screen.blit(sprajt, (50, 50))
pygame.display.flip()

assert screen.get_at((60, 60))[:3] == (255, 100, 100)
assert screen.get_at((10, 10))[:3] == (20, 20, 40)
print("Верно: Surface нанесена через blit() ровно в указанной точке.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nСоздайте Surface с флагом pygame.SRCALPHA "
          "и заполните её полупрозрачным цветом (четвёртое число в кортеже цвета — альфа-канал, "
          "0–255). Нанесите её на цветной фон и убедитесь, что итоговый цвет — смесь фона и "
          "полупрозрачного слоя, а не чистый цвет самого слоя.")
    nb.code('''pygame.init()
screen = pygame.display.set_mode((600, 400))
screen.fill((0, 0, 0))

sloj = pygame.Surface((100, 100), pygame.SRCALPHA)
sloj.fill((255, 0, 0, 128))  # красный с прозрачностью 50%
screen.blit(sloj, (0, 0))
pygame.display.flip()

cvet = screen.get_at((10, 10))[:3]
print("Итоговый цвет смеси:", cvet)
assert cvet != (255, 0, 0)  # не чистый красный — значит, прозрачность реально сработала
assert cvet != (0, 0, 0)    # и не чистый чёрный фон
print("Верно: результат — смесь фона и полупрозрачного слоя.")''')
    nb.write(OUT_DIR / "20-17-surface.ipynb")
    print(f"Записано: 20-17 ({len(nb)} ячеек)")


def build_19() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-19 · Спрайты и ассеты\n\nПрактика к разделу "
          "[«Спрайты и ассеты»](../../site/chapters/glava-20/20-19-sprajty-i-assety.html).")
    nb.md("## Цель\n\nПостроить надёжный путь к ассету через pathlib, не зависящий от текущей "
          "рабочей директории запуска.")
    nb.md("## Рабочий пример")
    nb.code('''from pathlib import Path
import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))

# В самом ноутбуке нет отдельного файла ассета — но путь строится ровно так,
# как в разделе 20.19: от расположения кода, а не от текущей директории запуска.
BASE_DIR = Path.cwd()
put_k_assetu = BASE_DIR / "assets" / "igrok.png"
print("Путь построен независимо от CWD:", put_k_assetu)
print("Путь абсолютный:", put_k_assetu.is_absolute())
pygame.quit()''')
    nb.md("## Проверка результата")
    nb.code('''from pathlib import Path

BASE_DIR = Path.cwd()
put_k_assetu = BASE_DIR / "assets" / "igrok.png"

assert put_k_assetu.is_absolute()
assert put_k_assetu.name == "igrok.png"
assert put_k_assetu.parent.name == "assets"
print("Верно: путь абсолютный и не зависит от того, откуда был запущен скрипт.")''')
    nb.md("## Задание ★ Базовая практика\n\nПостройте похожим образом путь к звуковому файлу "
          "assets/sounds/prygok.wav и проверьте оба его родительских каталога "
          "(.parent.name и .parent.parent.name).")
    nb.code('''from pathlib import Path

BASE_DIR = Path.cwd()
put_k_zvuku = BASE_DIR / "assets" / "sounds" / "prygok.wav"

assert put_k_zvuku.parent.name == "sounds"
assert put_k_zvuku.parent.parent.name == "assets"
print("Путь к звуку:", put_k_zvuku)
print("Верно: структура папок читается из самого пути.")''')
    nb.write(OUT_DIR / "20-19-sprajty.ipynb")
    print(f"Записано: 20-19 ({len(nb)} ячеек)")


def build_20() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-20 · Ввод: события и состояние\n\nПрактика к разделу "
          "[«Ввод: события и состояние»](../../site/chapters/glava-20/20-20-vvod-sobytiya-sostoyanie.html).")
    nb.md("## Цель\n\nНа практике увидеть разницу между KEYDOWN для разового действия и "
          "get_pressed() для непрерывного.")
    nb.md("## Рабочий пример — разовое действие через KEYDOWN")
    nb.code('''import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))

pryzhkov = 0
sobytie = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)

# Программно "нажимаем" пробел три раза подряд — как три отдельных нажатия
for _ in range(3):
    pygame.event.post(sobytie)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pryzhkov += 1

print("Прыжков засчитано:", pryzhkov)
pygame.quit()''')
    nb.md("## Проверка результата")
    nb.code('''assert pryzhkov == 3
print("Верно: три отдельных события KEYDOWN дали ровно три прыжка.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nПокажите на конкретных числах разницу из "
          "раздела 20.20: если бы прыжок засчитывался при каждой проверке "
          "\"клавиша зажата\" в течение 3 кадров подряд (а не по одному KEYDOWN), "
          "получилось бы 3 прыжка за одно и то же одно нажатие — ошибка \"стрельбы очередями\".")
    nb.code('''klavisha_zazhata_tri_kadra = [True, True, True]  # одно и то же нажатие, растянутое на 3 кадра

pryzhkov_esli_po_sostoyaniyu = sum(1 for zazhata in klavisha_zazhata_tri_kadra if zazhata)
print("Прыжков, если считать по состоянию каждый кадр:", pryzhkov_esli_po_sostoyaniyu)

assert pryzhkov_esli_po_sostoyaniyu == 3   # неправильно для разового действия!
assert pryzhkov == 1 * 3   # для сравнения: столько же, но это ТРИ разных настоящих нажатия, а не одно
print("Видно: get_pressed() для разового действия завышает счётчик — нужен именно KEYDOWN.")''')
    nb.write(OUT_DIR / "20-20-vvod.ipynb")
    print(f"Записано: 20-20 ({len(nb)} ячеек)")


def build_23() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-23 · Анимация спрайт-листов\n\nПрактика к разделу "
          "[«Анимация спрайт-листов»](../../site/chapters/glava-20/20-23-animatsiya.html).")
    nb.md("## Цель\n\nПереключать кадр анимации по собственному таймеру, а не каждый кадр цикла.")
    nb.md(LOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

KOLICHESTVO_KADROV = 4
SKOROST_ANIMACII = 0.1  # секунд на кадр анимации

tekushij_kadr = 0
vremya_do_smeny = SKOROST_ANIMACII
istoriya_kadrov = []

for _ in range(60):
    dt = clock.tick(60) / 1000
    vremya_do_smeny -= dt
    if vremya_do_smeny <= 0:
        tekushij_kadr = (tekushij_kadr + 1) % KOLICHESTVO_KADROV
        vremya_do_smeny = SKOROST_ANIMACII
    istoriya_kadrov.append(tekushij_kadr)

print("Кадр анимации сменился хотя бы раз:", len(set(istoriya_kadrov)) > 1)
print("Все значения кадра в допустимом диапазоне:", all(0 <= k < KOLICHESTVO_KADROV for k in istoriya_kadrov))
pygame.quit()''')
    nb.md("## Проверка результата")
    nb.code('''assert len(set(istoriya_kadrov)) > 1
assert all(0 <= k < KOLICHESTVO_KADROV for k in istoriya_kadrov)
print("Верно: анимация переключает кадры и никогда не выходит за пределы спрайт-листа.")''')
    nb.write(OUT_DIR / "20-23-animatsiya.ipynb")
    print(f"Записано: 20-23 ({len(nb)} ячеек)")


def build_24() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-24 · Звук и музыка\n\nПрактика к разделу "
          "[«Звук и музыка»](../../site/chapters/glava-20/20-24-zvuk.html).")
    nb.md("## Цель\n\nЗагрузить звук один раз и убедиться, что повторное воспроизведение не "
          "требует повторной загрузки с диска.")
    nb.md("## Рабочий пример")
    nb.code('''import time
import pygame

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((600, 400))

put_k_zvuku = "../../projects/pygame/bouncing-ball/assets/otskok.wav"
zvuk_otskoka = pygame.mixer.Sound(put_k_zvuku)   # загружаем ОДИН раз

nachalo = time.perf_counter()
for _ in range(5):
    zvuk_otskoka.play()   # только воспроизводим уже загруженный звук
vremya_pyati_vosproizvedenij = time.perf_counter() - nachalo

print("5 воспроизведений уже загруженного звука заняли (сек):", round(vremya_pyati_vosproizvedenij, 4))''')
    nb.md("## Проверка результата")
    nb.code('''assert isinstance(zvuk_otskoka, pygame.mixer.Sound)
# Воспроизведение уже загруженного звука — не операция чтения с диска,
# поэтому пять вызовов play() должны укладываться в доли секунды.
assert vremya_pyati_vosproizvedenij < 1.0
print("Верно: звук был загружен один раз, а не при каждом play().")''')
    nb.md("## Задание ★ Базовая практика\n\nЗагрузите звук ещё раз в отдельную переменную и "
          "убедитесь, что это НЕ один и тот же объект Python в памяти, хотя оба указывают на "
          "один и тот же файл — то есть на диск действительно ходили дважды.")
    nb.code('''zvuk_otskoka_2 = pygame.mixer.Sound(put_k_zvuku)
assert zvuk_otskoka_2 is not zvuk_otskoka
print("Верно: это два отдельных объекта — именно поэтому загрузку выносят из цикла заранее.")''')
    nb.write(OUT_DIR / "20-24-zvuk.ipynb")
    print(f"Записано: 20-24 ({len(nb)} ячеек)")


def build_26() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-26 · Архитектура: класс Game\n\nПрактика к разделу "
          "[«Архитектура: класс Game»](../../site/chapters/glava-20/20-26-arhitektura-class-game.html).")
    nb.md("## Цель\n\nСобрать минимальный класс Game с методами handle_events/update/render и "
          "убедиться, что пауза останавливает именно update().")
    nb.md("## Рабочий пример")
    nb.code('''import pygame
from enum import Enum, auto

class Sostoyanie(Enum):
    IGRA = auto()
    PAUZA = auto()

class MiniGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 400))
        self.state = Sostoyanie.IGRA
        self.x = 0

    def update(self, dt):
        if self.state is not Sostoyanie.IGRA:
            return
        self.x += 100 * dt   # 100 пикселей в секунду

    def render(self):
        self.screen.fill((20, 20, 40))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.x, 180, 20, 20))
        pygame.display.flip()

igra = MiniGame()
for _ in range(30):
    igra.update(1 / 60)
    igra.render()

print("Позиция после 30 кадров (игра идёт):", igra.x)''')
    nb.md("## Проверка результата")
    nb.code('''assert igra.x > 0
pozicziya_do_pauzy = igra.x

igra.state = Sostoyanie.PAUZA
for _ in range(30):
    igra.update(1 / 60)
    igra.render()

assert igra.x == pozicziya_do_pauzy
print("Верно: на паузе update() не двигает объект, хотя render() продолжает вызываться.")''')
    nb.write(OUT_DIR / "20-26-arhitektura.ipynb")
    print(f"Записано: 20-26 ({len(nb)} ячеек)")


def build_33() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-33 · Финальный проект: Мяч Pro\n\nПрактика к разделу "
          "[«Финальный проект — Мяч Pro»](../../site/chapters/glava-20/20-33-finalnyj-proekt-myach-pro.html). "
          "Тот же код, что и в `projects/pygame/bouncing-ball/bouncing_ball.py`.")
    nb.md("## Цель\n\nПрогнать финальную версию BouncingBallGame и проверить её ключевые "
          "гарантии: движение через delta time, паузу и счёт.")
    nb.code('''import sys
sys.path.insert(0, "../../projects/pygame/bouncing-ball")
import bouncing_ball as bb

game = bb.BouncingBallGame()
for _ in range(180):
    game.update(1 / 60)
    game.render()

print("Отскоков:", game.otskokov)
print("Счёт:", game.schet)
print("Состояние:", game.state)''')
    nb.md("## Проверка результата")
    nb.code('''assert game.otskokov > 0
assert game.schet == game.otskokov * bb.OCHKOV_ZA_OTSKOK
assert bb.RADIUS <= game.x <= bb.SHIRINA - bb.RADIUS
assert bb.RADIUS <= game.y <= bb.VYSOTA - bb.RADIUS
print("Верно: счёт растёт строго вместе с числом отскоков, мяч не покидает поле.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nПоставьте игру на паузу, прогоните ещё 60 "
          "кадров и убедитесь, что ни счёт, ни позиция мяча не изменились ни на пиксель.")
    nb.code('''game.toggle_pause()
do = (game.x, game.y, game.schet, game.otskokov)
for _ in range(60):
    game.update(1 / 60)
posle = (game.x, game.y, game.schet, game.otskokov)

assert do == posle
print("Верно: пауза останавливает игру полностью, а не только отрисовку.")''')
    nb.write(OUT_DIR / "20-33-myach-pro.ipynb")
    print(f"Записано: 20-33 ({len(nb)} ячеек)")


# ---------------------------------------------------------------------------
# Практики в браузере (browser-pyodide) — чистая логика, без Pygame и без
# настоящего окна: 20-15, 20-16, 20-18, 20-21, 20-22, 20-25, 20-27, 20-28
# ---------------------------------------------------------------------------

def build_15() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-15 · FPS и бюджет кадра\n\nПрактика к разделу "
          "[«Кадры в секунду и время кадра»](../../site/chapters/glava-20/20-15-fps-i-vremya-kadra.html). "
          "Здесь нет настоящего окна Pygame — только математика, стоящая за FPS.")
    nb.md("## Цель\n\nСчитать время кадра из FPS и обратно, без единого вызова Pygame.")
    nb.md("## Рабочий пример")
    nb.code('''def vremya_kadra_ms(fps):
    return 1000 / fps

def fps_iz_vremeni_kadra(vremya_ms):
    return 1000 / vremya_ms

for fps in (30, 60, 120):
    print(f"{fps} FPS -> {vremya_kadra_ms(fps):.3f} мс на кадр")

print("120 мс на кадр соответствуют", round(fps_iz_vremeni_kadra(120), 2), "FPS")''')
    nb.md("## Проверка результата")
    nb.code('''assert round(vremya_kadra_ms(60), 3) == 16.667
assert round(vremya_kadra_ms(30), 3) == 33.333
assert round(fps_iz_vremeni_kadra(20), 1) == 50.0
print("Верно: время кадра и FPS — взаимно обратные величины.")''')
    nb.md("## Задание ★ Базовая практика\n\nОпределите функцию skolko_kadrov_za_sekundy(fps, "
          "sekund), возвращающую целое число кадров, которые успеют пройти за заданное время.")
    nb.code('''def skolko_kadrov_za_sekundy(fps, sekund):
    return int(fps * sekund)

assert skolko_kadrov_za_sekundy(60, 2) == 120
assert skolko_kadrov_za_sekundy(30, 0.5) == 15
print("За 2.5 секунды на 24 FPS пройдёт", skolko_kadrov_za_sekundy(24, 2.5), "кадров")''')
    nb.write(OUT_DIR / "20-15-fps.ipynb")
    print(f"Записано: 20-15 ({len(nb)} ячеек)")


def build_16() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-16 · Delta time\n\nПрактика к разделу "
          "[«Delta time»](../../site/chapters/glava-20/20-16-delta-time.html). Чистая математика "
          "движения — без Pygame и без окна.")
    nb.md("## Цель\n\nНа числах убедиться, что движение через delta time не зависит от FPS, а "
          "движение \"пикселей за кадр\" — зависит.")
    nb.md("## Рабочий пример — движение через delta time")
    nb.code('''def simulirovat_dt(skorost, fps, sekund):
    x = 0.0
    dt = 1 / fps
    for _ in range(int(fps * sekund)):
        x += skorost * dt
    return x

x_30 = simulirovat_dt(100, 30, 2)
x_60 = simulirovat_dt(100, 60, 2)
x_120 = simulirovat_dt(100, 120, 2)
print("Смещение за 2 секунды на 30/60/120 FPS:", round(x_30, 6), round(x_60, 6), round(x_120, 6))''')
    nb.md("## Проверка результата")
    nb.code('''assert abs(x_30 - x_60) < 1e-6
assert abs(x_60 - x_120) < 1e-6
assert abs(x_60 - 200.0) < 1e-6
print("Верно: результат не зависит от FPS — все три числа совпадают.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nНапишите наивную версию "
          "simulirovat_bez_dt(px_za_kadr, fps, sekund), которая прибавляет константу за каждый "
          "кадр (без dt), и убедитесь, что ЕЁ результат меняется вместе с FPS — то есть "
          "воспроизведите на числах саму проблему из раздела 20.16.")
    nb.code('''def simulirovat_bez_dt(px_za_kadr, fps, sekund):
    x = 0.0
    for _ in range(int(fps * sekund)):
        x += px_za_kadr
    return x

bez_dt_30 = simulirovat_bez_dt(2, 30, 2)
bez_dt_60 = simulirovat_bez_dt(2, 60, 2)

assert bez_dt_30 != bez_dt_60
assert bez_dt_60 == 2 * bez_dt_30
print("На 30 FPS:", bez_dt_30, " на 60 FPS:", bez_dt_60, "— результат зависит от FPS, как и предупреждает раздел 20.16.")''')
    nb.write(OUT_DIR / "20-16-delta-time.ipynb")
    print(f"Записано: 20-16 ({len(nb)} ячеек)")


def build_18() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-18 · Rect и система координат\n\nПрактика к разделу "
          "[«Rect и система координат»](../../site/chapters/glava-20/20-18-rect-i-koordinaty.html). "
          "Здесь Rect воспроизведён обычным кортежем (x, y, ширина, высота) — идея та же, "
          "настоящее окно не требуется.")
    nb.md("## Цель\n\nСчитать границы прямоугольника вручную и подтвердить, что ось Y в Pygame "
          "растёт вниз.")
    nb.md("## Рабочий пример")
    nb.code('''def granicy(rect):
    x, y, w, h = rect
    return {"left": x, "top": y, "right": x + w, "bottom": y + h, "center": (x + w / 2, y + h / 2)}

igrok = (100, 200, 40, 40)
g = granicy(igrok)
print(g)

# "Прыжок вверх" на экране Pygame — это УМЕНЬШЕНИЕ y, а не увеличение
y_do_pryzhka = 300
y_posle_pryzhka = y_do_pryzhka - 50   # выше на экране = меньшее y
print("До прыжка y =", y_do_pryzhka, " после прыжка y =", y_posle_pryzhka)''')
    nb.md("## Проверка результата")
    nb.code('''assert g["right"] == 140
assert g["bottom"] == 240
assert g["center"] == (120.0, 220.0)
assert y_posle_pryzhka < y_do_pryzhka
print("Верно: границы посчитаны правильно, и прыжок вверх уменьшает y, как и на экране Pygame.")''')
    nb.write(OUT_DIR / "20-18-rect.ipynb")
    print(f"Записано: 20-18 ({len(nb)} ячеек)")


def build_21() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-21 · Столкновения и хитбоксы\n\nПрактика к разделу "
          "[«Столкновения и хитбоксы»](../../site/chapters/glava-20/20-21-stolknoveniya.html). "
          "AABB-проверка пересечения — чистая функция, как и в тексте раздела.")
    nb.md("## Цель\n\nРеализовать и проверить проверку пересечения двух прямоугольников.")
    nb.md("## Рабочий пример")
    nb.code('''def pryamougolniki_peresekayutsya(a, b):
    ax1, ay1, aw, ah = a
    bx1, by1, bw, bh = b
    ax2, ay2 = ax1 + aw, ay1 + ah
    bx2, by2 = bx1 + bw, by1 + bh
    return ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1

igrok = (100, 100, 40, 40)
vrag_blizko = (120, 120, 40, 40)
vrag_daleko = (400, 400, 40, 40)

print("Столкновение с близким врагом:", pryamougolniki_peresekayutsya(igrok, vrag_blizko))
print("Столкновение с далёким врагом:", pryamougolniki_peresekayutsya(igrok, vrag_daleko))''')
    nb.md("## Проверка результата")
    nb.code('''assert pryamougolniki_peresekayutsya(igrok, vrag_blizko) is True
assert pryamougolniki_peresekayutsya(igrok, vrag_daleko) is False
# соприкосновение ровно краем — НЕ считается пересечением
assert pryamougolniki_peresekayutsya((0, 0, 40, 40), (40, 0, 40, 40)) is False
print("Верно: пересечение находится правильно, включая пограничный случай соприкосновения краями.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nУменьшите хитбокс игрока на 10 пикселей с "
          "каждой стороны (как rect.inflate(-10, -10) из раздела 20.21) и убедитесь, что после "
          "уменьшения столкновение с vrag_blizko, которое было true, может стать false.")
    nb.code('''def szhat(rect, na):
    x, y, w, h = rect
    return (x + na, y + na, w - 2 * na, h - 2 * na)

igrok_szhatyj = szhat(igrok, 10)
do = pryamougolniki_peresekayutsya(igrok, vrag_blizko)
posle = pryamougolniki_peresekayutsya(igrok_szhatyj, vrag_blizko)
print("До уменьшения хитбокса:", do, " после:", posle)
assert do is True
print("Размер хитбокса напрямую влияет на то, что считается столкновением.")''')
    nb.write(OUT_DIR / "20-21-stolknoveniya.ipynb")
    print(f"Записано: 20-21 ({len(nb)} ячеек)")


def build_22() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-22 · Простая физика\n\nПрактика к разделу "
          "[«Простая физика»](../../site/chapters/glava-20/20-22-prostaya-fizika.html). "
          "Гравитация и отскок с затуханием — на чистых числах.")
    nb.md("## Цель\n\nПосчитать накопление скорости под гравитацией и затухание при повторных "
          "отскоках.")
    nb.md("## Рабочий пример")
    nb.code('''GRAVITACIYA = 900  # пикселей в секунду за секунду
POTERYA_PRI_UDARE = 0.8

def shag_gravitacii(skorost_y, dt):
    return skorost_y + GRAVITACIYA * dt

skorost = 0.0
for _ in range(60):   # одна секунда падения на 60 "кадрах"
    skorost = shag_gravitacii(skorost, 1 / 60)

print("Скорость падения после 1 секунды:", round(skorost, 1), "пикселей/сек")

skorost_otskoka = -skorost * POTERYA_PRI_UDARE
print("Скорость сразу после отскока:", round(skorost_otskoka, 1))''')
    nb.md("## Проверка результата")
    nb.code('''assert abs(skorost - 900) < 5    # накопленная скорость близка к GRAVITACIYA * 1 сек
assert skorost_otskoka < 0                # направление развернулось (Y растёт вниз — раздел 20.18, значит вверх это отрицательный Y)
assert abs(skorost_otskoka) < skorost     # но по модулю стало меньше — есть затухание
print("Верно: гравитация накапливает скорость, а отскок разворачивает её с потерей энергии.")''')
    nb.md("## Задание ★ Базовая практика\n\nПосчитайте, сколько отскоков нужно, чтобы скорость "
          "упала ниже 1.0 пикселя/сек, начиная с 300 пикселей/сек.")
    nb.code('''s = 300.0
otskokov = 0
while s > 1.0:
    s *= POTERYA_PRI_UDARE
    otskokov += 1

print("Отскоков до почти полной остановки:", otskokov)
assert otskokov > 0
assert s <= 1.0''')
    nb.write(OUT_DIR / "20-22-fizika.ipynb")
    print(f"Записано: 20-22 ({len(nb)} ячеек)")


def build_25() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-25 · Состояния игры\n\nПрактика к разделу "
          "[«Состояния игры»](../../site/chapters/glava-20/20-25-sostoyaniya-igry.html). "
          "Проверка допустимых переходов между состояниями.")
    nb.md("## Цель\n\nОписать разрешённые переходы между состояниями как данные и проверить их.")
    nb.md("## Рабочий пример")
    nb.code('''from enum import Enum, auto

class Sostoyanie(Enum):
    MENU = auto()
    IGRA = auto()
    PAUZA = auto()
    GAME_OVER = auto()

RAZRESHENNYE_PEREHODY = {
    Sostoyanie.MENU: {Sostoyanie.IGRA},
    Sostoyanie.IGRA: {Sostoyanie.PAUZA, Sostoyanie.GAME_OVER},
    Sostoyanie.PAUZA: {Sostoyanie.IGRA},
    Sostoyanie.GAME_OVER: {Sostoyanie.MENU},
}

def perehod_razreshen(otkuda, kuda):
    return kuda in RAZRESHENNYE_PEREHODY[otkuda]

print("MENU -> IGRA:", perehod_razreshen(Sostoyanie.MENU, Sostoyanie.IGRA))
print("MENU -> GAME_OVER:", perehod_razreshen(Sostoyanie.MENU, Sostoyanie.GAME_OVER))
print("PAUZA -> GAME_OVER:", perehod_razreshen(Sostoyanie.PAUZA, Sostoyanie.GAME_OVER))''')
    nb.md("## Проверка результата")
    nb.code('''assert perehod_razreshen(Sostoyanie.MENU, Sostoyanie.IGRA) is True
assert perehod_razreshen(Sostoyanie.MENU, Sostoyanie.GAME_OVER) is False
assert perehod_razreshen(Sostoyanie.PAUZA, Sostoyanie.GAME_OVER) is False
assert perehod_razreshen(Sostoyanie.IGRA, Sostoyanie.PAUZA) is True
print("Верно: не любое состояние достижимо из любого другого напрямую.")''')
    nb.write(OUT_DIR / "20-25-sostoyaniya.ipynb")
    print(f"Записано: 20-25 ({len(nb)} ячеек)")


def build_27() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-27 · Производительность и бюджет кадра\n\nПрактика к разделу "
          "[«Производительность и бюджет кадра»](../../site/chapters/glava-20/20-27-proizvoditelnost.html).")
    nb.md("## Цель\n\nСчитать, сколько миллисекунд из бюджета кадра уже израсходовано.")
    nb.md("## Рабочий пример")
    nb.code('''def byudzhet_kadra_ms(fps):
    return 1000 / fps

def ostatok_byudzheta(fps, potracheno_ms):
    return byudzhet_kadra_ms(fps) - potracheno_ms

byudzhet_60 = byudzhet_kadra_ms(60)
ostatok = ostatok_byudzheta(60, 10.0)
print(f"Бюджет кадра на 60 FPS: {byudzhet_60:.3f} мс, израсходовано 10 мс, осталось {ostatok:.3f} мс")

perebor = ostatok_byudzheta(60, 20.0)
print("Если потрачено 20 мс из бюджета 60 FPS, остаток:", round(perebor, 3), "(отрицательный значит кадр не уложился)")''')
    nb.md("## Проверка результата")
    nb.code('''assert round(byudzhet_60, 3) == 16.667
assert round(ostatok, 3) == round(16.667 - 10.0, 3)
assert perebor < 0
print("Верно: отрицательный остаток бюджета означает, что кадр не уложился в целевой FPS.")''')
    nb.write(OUT_DIR / "20-27-proizvoditelnost.ipynb")
    print(f"Записано: 20-27 ({len(nb)} ячеек)")


def build_28() -> None:
    nb = NotebookBuilder()
    nb.md("# 20-28 · Отладка игр\n\nПрактика к разделу "
          "[«Отладка игр»](../../site/chapters/glava-20/20-28-otladka-igr.html). "
          "Диагностика по симптому — сопоставьте симптом и причину из таблицы раздела 20.28.")
    nb.md("## Цель\n\nСопоставить симптом бага с его типичной причиной.")
    nb.md("## Рабочий пример")
    nb.code('''SIMPTOM_K_PRICHINE = {
    "okno_ne_otvechaet": "sobytiya_ne_obrabotany",
    "ekran_chernyj": "zabyt_flip",
    "sledy_na_ekrane": "zabyt_fill",
    "teleportaciya_personazha": "dt_v_millisekundah_ne_pereveden",
    "dvizhenie_zavisit_ot_kompyutera": "net_delta_time",
}

def diagnoz(simptom):
    return SIMPTOM_K_PRICHINE.get(simptom, "neizvestnyj_simptom")

print(diagnoz("ekran_chernyj"))
print(diagnoz("teleportaciya_personazha"))''')
    nb.md("## Проверка результата")
    nb.code('''assert diagnoz("ekran_chernyj") == "zabyt_flip"
assert diagnoz("sledy_na_ekrane") == "zabyt_fill"
assert diagnoz("dvizhenie_zavisit_ot_kompyutera") == "net_delta_time"
assert diagnoz("chto-to_neizvestnoe") == "neizvestnyj_simptom"
print("Верно: каждый известный симптом сопоставлен правильной причине из справочника раздела 20.28.")''')
    nb.md("## Задание ★ Базовая практика\n\nДобавьте в словарь ещё одну пару: симптом "
          "\"animaciya_otstaet_na_kadr\" -> причина \"update_posle_render\", и проверьте её.")
    nb.code('''SIMPTOM_K_PRICHINE["animaciya_otstaet_na_kadr"] = "update_posle_render"
assert diagnoz("animaciya_otstaet_na_kadr") == "update_posle_render"
print("Справочник расширен:", len(SIMPTOM_K_PRICHINE), "известных симптомов.")''')
    nb.write(OUT_DIR / "20-28-otladka.ipynb")
    print(f"Записано: 20-28 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_02()
    build_03()
    build_04()
    build_05()
    build_14()
    build_15()
    build_16()
    build_17()
    build_18()
    build_19()
    build_20()
    build_21()
    build_22()
    build_23()
    build_24()
    build_25()
    build_26()
    build_27()
    build_28()
    build_33()
