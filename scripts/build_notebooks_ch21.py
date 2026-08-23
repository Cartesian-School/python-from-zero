#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 21 (Космический шутер).

Как и в главе 20: настоящий игровой цикл — это `while rabotaet:`, зависящий от
событий пользователя. В ноутбуке вместо этого используем `for kadr in range(N):`
с фиксированным числом кадров — логика каждого кадра (движение, столкновения,
отрисовка) в точности та же, что и в `space_shooter.py`.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-21"

LOOP_NOTE_MD = (
    "## Про игровой цикл в этом ноутбуке\n\n"
    "В обычном `.py`-файле игровой цикл — это `while rabotaet:`, зависящий от событий "
    "пользователя (закрытие окна, нажатия клавиш). В автоматически выполняемом ноутбуке "
    "некому создавать такие события, поэтому здесь мы прогоняем фиксированное число кадров "
    "через `for kadr in range(N):` — логика каждого отдельного кадра (движение, столкновения, "
    "отрисовка, `clock.tick()`) при этом точно такая же, как в настоящей игре из "
    "`projects/pygame/space-shooter/space_shooter.py`."
)

SETUP_CODE = '''import random

import pygame

SHIRINA, VYSOTA = 480, 720
FPS = 60

KORABL_SHIRINA, KORABL_VYSOTA = 44, 44
KORABL_SKOROST = 6

PULYA_SHIRINA, PULYA_VYSOTA = 6, 18
PULYA_SKOROST = 9

VRAG_SHIRINA, VRAG_VYSOTA = 32, 28
VRAG_SKOROST = 2
INTERVAL_POYAVLENIYA_VRAGA = 45

BELYJ = (255, 255, 255)
CHERNYJ = (10, 10, 20)
ZELYONYJ = (80, 220, 120)
KRASNYJ = (230, 60, 60)
ZHYOLTYJ = (240, 220, 80)

pygame.init()
screen = pygame.display.set_mode((SHIRINA, VYSOTA))
pygame.display.set_caption("Космический шутер")
clock = pygame.time.Clock()
shrift = pygame.font.SysFont(None, 32)
shrift_bolshoj = pygame.font.SysFont(None, 64)


def novaya_igra():
    return {
        "korabl": pygame.Rect(
            SHIRINA // 2 - KORABL_SHIRINA // 2,
            VYSOTA - KORABL_VYSOTA - 20,
            KORABL_SHIRINA,
            KORABL_VYSOTA,
        ),
        "puli": [],
        "vragi": [],
        "schet": 0,
        "kadrov_do_vraga": INTERVAL_POYAVLENIYA_VRAGA,
        "igra_okonchena": False,
    }


def obrabotat_klavishi(state, klavishi):
    korabl = state["korabl"]
    if klavishi[pygame.K_LEFT]:
        korabl.x -= KORABL_SKOROST
    if klavishi[pygame.K_RIGHT]:
        korabl.x += KORABL_SKOROST
    korabl.x = max(0, min(korabl.x, SHIRINA - KORABL_SHIRINA))


def vystrelit(state):
    korabl = state["korabl"]
    pulya = pygame.Rect(
        korabl.centerx - PULYA_SHIRINA // 2,
        korabl.top,
        PULYA_SHIRINA,
        PULYA_VYSOTA,
    )
    state["puli"].append(pulya)


def sozdat_vraga():
    x = random.randint(0, SHIRINA - VRAG_SHIRINA)
    return pygame.Rect(x, -VRAG_VYSOTA, VRAG_SHIRINA, VRAG_VYSOTA)


def obnovit_igru(state):
    if state["igra_okonchena"]:
        return

    for pulya in state["puli"]:
        pulya.y -= PULYA_SKOROST
    state["puli"] = [p for p in state["puli"] if p.bottom > 0]

    state["kadrov_do_vraga"] -= 1
    if state["kadrov_do_vraga"] <= 0:
        state["vragi"].append(sozdat_vraga())
        state["kadrov_do_vraga"] = INTERVAL_POYAVLENIYA_VRAGA

    for vrag in state["vragi"]:
        vrag.y += VRAG_SKOROST

    novye_puli = []
    novye_vragi = list(state["vragi"])
    for pulya in state["puli"]:
        popala = False
        for vrag in list(novye_vragi):
            if pulya.colliderect(vrag):
                novye_vragi.remove(vrag)
                state["schet"] += 10
                popala = True
                break
        if not popala:
            novye_puli.append(pulya)
    state["puli"] = novye_puli
    state["vragi"] = novye_vragi

    for vrag in state["vragi"]:
        if vrag.bottom >= VYSOTA or vrag.colliderect(state["korabl"]):
            state["igra_okonchena"] = True
            break


def narisovat(state):
    screen.fill(CHERNYJ)
    pygame.draw.rect(screen, ZELYONYJ, state["korabl"])
    for pulya in state["puli"]:
        pygame.draw.rect(screen, ZHYOLTYJ, pulya)
    for vrag in state["vragi"]:
        pygame.draw.rect(screen, KRASNYJ, vrag)

    tablo = shrift.render(f"Счёт: {state['schet']}", True, BELYJ)
    screen.blit(tablo, (10, 10))

    if state["igra_okonchena"]:
        nadpis = shrift_bolshoj.render("ИГРА ОКОНЧЕНА", True, BELYJ)
        rect = nadpis.get_rect(center=(SHIRINA // 2, VYSOTA // 2))
        screen.blit(nadpis, rect)

    pygame.display.flip()'''


def build_01() -> None:
    nb = NotebookBuilder()
    nb.md("# 21-01 · Импорт и инициализация\n\nПрактика к разделу "
          "[«Игра «Космический шутер»»](../../site/chapters/glava-21/21-01-igra-import-init.html).")
    nb.md("## Цель\n\nПодключить нужные модули и настроить экран, часы и шрифт для новой игры.")
    nb.md("## Рабочий пример")
    nb.code('''import random

import pygame

SHIRINA, VYSOTA = 480, 720
FPS = 60

pygame.init()
screen = pygame.display.set_mode((SHIRINA, VYSOTA))
pygame.display.set_caption("Космический шутер")
clock = pygame.time.Clock()
shrift = pygame.font.SysFont(None, 32)

print("Экран создан:", screen.get_size())
print("Тип шрифта:", type(shrift))
pygame.quit()''')
    nb.md("## Проверка результата")
    nb.code('''pygame.init()
screen = pygame.display.set_mode((480, 720))
assert screen.get_size() == (480, 720)
print("Верно: размер экрана совпадает с задуманным.")
pygame.quit()''')
    nb.write(OUT_DIR / "21-01-init.ipynb")
    print(f"Записано: 21-01 ({len(nb)} ячеек)")


def build_02() -> None:
    nb = NotebookBuilder()
    nb.md("# 21-02 · Игровой цикл и корабль\n\nПрактика к разделу "
          "[«Игровой цикл»](../../site/chapters/glava-21/21-02-cikl-korabl.html).")
    nb.md("## Цель\n\nСоздать корабль игрока через pygame.Rect и отрисовать его.")
    nb.md(LOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import pygame

pygame.init()
screen = pygame.display.set_mode((480, 720))
clock = pygame.time.Clock()

KORABL_SHIRINA, KORABL_VYSOTA = 44, 44
korabl = pygame.Rect(480 // 2 - KORABL_SHIRINA // 2, 720 - KORABL_VYSOTA - 20,
                      KORABL_SHIRINA, KORABL_VYSOTA)

for kadr in range(5):
    for event in pygame.event.get():
        pass
    screen.fill((10, 10, 20))
    pygame.draw.rect(screen, (80, 220, 120), korabl)
    pygame.display.flip()
    clock.tick(60)

print("Корабль:", korabl)
print("Цвет в центре корабля:", screen.get_at(korabl.center))
pygame.quit()''')
    nb.md("## Проверка результата")
    nb.code('''pygame.init()
screen = pygame.display.set_mode((480, 720))
screen.fill((10, 10, 20))
pygame.draw.rect(screen, (80, 220, 120), korabl)
pygame.display.flip()

assert screen.get_at(korabl.center)[:3] == (80, 220, 120)
print("Верно: корабль нарисован в ожидаемом цвете.")
pygame.quit()''')
    nb.write(OUT_DIR / "21-02-korabl.ipynb")
    print(f"Записано: 21-02 ({len(nb)} ячеек)")


def build_03() -> None:
    nb = NotebookBuilder()
    nb.md("# 21-03 · Движение корабля и враги\n\nПрактика к разделу "
          "[«Перемещаем корабль. Создаём и перемещаем врагов»]"
          "(../../site/chapters/glava-21/21-03-dvizhenie-vragi.html).")
    nb.md("## Цель\n\nОграничить движение корабля краями экрана и заставить врагов появляться "
          "и спускаться вниз.")
    nb.md(LOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code(SETUP_CODE)
    nb.code('''state = novaya_igra()

# симулируем: стрелка вправо зажата 50 кадров подряд
for kadr in range(50):
    klavishi = {pygame.K_LEFT: False, pygame.K_RIGHT: True}
    obrabotat_klavishi(state, klavishi)
    obnovit_igru(state)
    narisovat(state)
    clock.tick(FPS)

print("Корабль после 50 кадров движения вправо:", state["korabl"])
print("Врагов появилось:", len(state["vragi"]))''')
    nb.md("## Проверка результата")
    nb.code('''assert state["korabl"].x == SHIRINA - KORABL_SHIRINA, "корабль должен упереться в правый край"
print("Верно: корабль остановился у правого края экрана, не выйдя за его пределы.")

assert len(state["vragi"]) >= 1, "за 50 кадров должен появиться хотя бы один враг (интервал 45)"
print(f"Найдено врагов: {len(state['vragi'])}")''')
    nb.md("## Задание ★ Базовая практика\n\nПрогоните ещё 45 кадров без движения корабля и "
          "убедитесь, что появился второй враг.")
    nb.code('''for kadr in range(45):
    klavishi = {pygame.K_LEFT: False, pygame.K_RIGHT: False}
    obrabotat_klavishi(state, klavishi)
    obnovit_igru(state)
    narisovat(state)

print("Врагов теперь:", len(state["vragi"]))
assert len(state["vragi"]) >= 2
print("Верно: появился второй враг.")''')
    nb.write(OUT_DIR / "21-03-dvizhenie-vragi.ipynb")
    print(f"Записано: 21-03 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 21-04 · Стреляем\n\nПрактика к разделу "
          "[«Стреляем»](../../site/chapters/glava-21/21-04-strelba.html).")
    nb.md("## Цель\n\nСоздать пулю у носа корабля и убедиться, что она улетает вверх.")
    nb.md("## Рабочий пример")
    nb.code(SETUP_CODE)
    nb.code('''state = novaya_igra()
vystrelit(state)

print("Пуль после выстрела:", len(state["puli"]))
print("Позиция пули:", state["puli"][0])
print("Позиция корабля:", state["korabl"])''')
    nb.md("## Проверка результата")
    nb.code('''pulya = state["puli"][0]
assert pulya.centerx == state["korabl"].centerx
assert pulya.top == state["korabl"].top
print("Верно: пуля появилась ровно у носа корабля.")''')
    nb.md("## Эксперимент — пуля улетает за экран и исчезает")
    nb.code('''y_do = state["puli"][0].y
for kadr in range(200):
    obnovit_igru(state)

print("Пуль осталось:", len(state["puli"]))
assert len(state["puli"]) == 0, "пуля должна улететь за верхний край экрана и исчезнуть"
print(f"Верно: пуля улетела с {y_do} за пределы экрана и была удалена из списка.")''')
    nb.write(OUT_DIR / "21-04-strelba.ipynb")
    print(f"Записано: 21-04 ({len(nb)} ячеек)")


def build_06() -> None:
    nb = NotebookBuilder()
    nb.md("# 21-06 · Уничтожаем врагов и корабль\n\nПрактика к разделам "
          "[«Уничтожаем врагов»](../../site/chapters/glava-21/21-06-unichtozhenie.html) и "
          "[«Перерисовываем врагов. Игра окончена!»]"
          "(../../site/chapters/glava-21/21-07-game-over.html).")
    nb.md("## Цель\n\nПроверить, что попадание пули уничтожает врага и начисляет очки, а "
          "враг, долетевший до низа экрана, завершает игру.")
    nb.md("## Рабочий пример — попадание пули по врагу")
    nb.code(SETUP_CODE)
    nb.code('''state = novaya_igra()

# ставим врага прямо перед носом корабля и стреляем
vrag = pygame.Rect(state["korabl"].centerx - 20, state["korabl"].top - 30, VRAG_SHIRINA, VRAG_VYSOTA)
state["vragi"] = [vrag]
vystrelit(state)

for kadr in range(10):
    obnovit_igru(state)
    if state["schet"] > 0:
        break

print("Счёт:", state["schet"])
print("Врагов осталось:", len(state["vragi"]))''')
    nb.md("## Проверка результата")
    nb.code('''assert state["schet"] == 10, "попадание должно добавить 10 очков"
assert len(state["vragi"]) == 0, "уничтоженный враг должен исчезнуть из списка"
print("Верно: враг уничтожен пулей, счёт увеличен на 10.")''')
    nb.md("## Эксперимент — враг долетает до низа экрана")
    nb.code('''state2 = novaya_igra()
state2["vragi"] = [pygame.Rect(100, VYSOTA - VRAG_VYSOTA - 1, VRAG_SHIRINA, VRAG_VYSOTA)]

obnovit_igru(state2)
narisovat(state2)

print("Игра окончена:", state2["igra_okonchena"])
assert state2["igra_okonchena"] is True
print("Верно: враг, долетевший до низа экрана, завершает игру.")''')
    nb.md("## Эксперимент — обновление игры останавливается после конца игры")
    nb.code('''schet_do = state2["schet"]
vragov_do = len(state2["vragi"])

for kadr in range(20):
    obnovit_igru(state2)

assert state2["schet"] == schet_do
assert len(state2["vragi"]) == vragov_do
print("Верно: после игра окончена состояние больше не меняется.")''')
    nb.write(OUT_DIR / "21-06-unichtozhenie.ipynb")
    print(f"Записано: 21-06 ({len(nb)} ячеек)")


def build_08() -> None:
    nb = NotebookBuilder()
    nb.md("# 21-08 · Полная игра целиком\n\nПрактика к разделу "
          "[«Полный код»](../../site/chapters/glava-21/21-08-polnyj-kod-itogi.html). "
          "Полный файл — `projects/pygame/space-shooter/space_shooter.py`.")
    nb.md("## Цель\n\nПрогнать игру много кадров подряд и убедиться, что движение корабля, "
          "появление врагов, отрисовка и завершение игры работают вместе, как единое целое.")
    nb.md(LOOP_NOTE_MD)
    nb.code(SETUP_CODE)
    nb.md("## Полная симуляция — движение и появление врагов без стрельбы\n\n"
          "Чтобы результат был предсказуемым (враги не уничтожаются случайными попаданиями), "
          "в этом прогоне корабль просто двигается, а первый же враг долетает до низа экрана "
          "и завершает игру — ровно так, как описано в разделе «Уничтожаем космический корабль!».")
    nb.code('''state = novaya_igra()
random.seed(3)

# При VRAG_SKOROST = 2 px/кадр первому врагу нужно больше 400/2 = 200 кадров,
# только чтобы пересечь VYSOTA = 720 px по вертикали — 500 кадров даёт запас.
for kadr in range(500):
    klavishi = {
        pygame.K_LEFT: kadr % 20 < 10,
        pygame.K_RIGHT: kadr % 20 >= 10,
    }
    obrabotat_klavishi(state, klavishi)
    obnovit_igru(state)
    narisovat(state)
    clock.tick(FPS)
    if state["igra_okonchena"]:
        break

print("Кадров прогнано:", kadr + 1)
print("Финальный счёт:", state["schet"])
print("Игра окончена:", state["igra_okonchena"])''')
    nb.md("## Проверка результата")
    nb.code('''assert state["igra_okonchena"] is True, "за 500 кадров хотя бы один враг должен долететь до низа экрана"
assert kadr + 1 <= 500
print(f"Верно: игра завершилась на кадре {kadr + 1} со счётом {state['schet']}.")
pygame.quit()''')
    nb.write(OUT_DIR / "21-08-polnaya-igra.ipynb")
    print(f"Записано: 21-08 ({len(nb)} ячеек)")


def build_09() -> None:
    nb = NotebookBuilder()
    nb.md("# 21-09 · Архитектура: набросок класса Player\n\nПрактика к разделу "
          "[«Архитектура: Game, Player, Bullet, Enemy»]"
          "(../../site/chapters/glava-21/21-09-arhitektura-proekta.html).")
    nb.md("## Цель\n\nСобрать минимальный класс Player с Vector2-позицией и Rect, "
          "синхронизированным из неё — тот же принцип, что использует настоящий "
          "space_shooter.py.")
    nb.md(LOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import pygame

pygame.init()
screen = pygame.display.set_mode((480, 720))


class Player:
    def __init__(self, image, center):
        self.image = image
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(center)
        self.rect.center = (round(self.position.x), round(self.position.y))

    def move(self, direction, dt, speed=200.0):
        if direction.length_squared() > 0:
            direction = direction.normalize()
        self.position += direction * speed * dt
        self.rect.center = (round(self.position.x), round(self.position.y))


image = pygame.Surface((44, 44), pygame.SRCALPHA)
pygame.draw.polygon(image, (60, 170, 255), [(22, 2), (40, 40), (4, 40)])

player = Player(image, (240.0, 600.0))
for _ in range(30):
    player.move(pygame.Vector2(1, 0), 1 / 60)

print("Позиция:", player.position)
print("Rect:", player.rect)
pygame.quit()''')
    nb.md("## Проверка результата")
    nb.code('''import math

assert math.isclose(player.position.x, 240.0 + 200.0 * 0.5, abs_tol=1e-6)
assert player.rect.centerx == round(player.position.x)
print("Верно: rect.center пересобран из position, а не обновлён напрямую.")''')
    nb.write(OUT_DIR / "21-09-arhitektura.ipynb")
    print(f"Записано: 21-09 ({len(nb)} ячеек)")


def build_11() -> None:
    nb = NotebookBuilder()
    nb.md("# 21-11 · Vector2 и точное движение\n\nПрактика к разделу "
          "[«Vector2 и точное движение»]"
          "(../../site/chapters/glava-21/21-11-vector2-tochnoe-dvizhenie.html).")
    nb.md("## Цель\n\nПосчитать нормализацию вектора направления и ограничение позиции "
          "границами игрового поля — той же логикой, что использует Player.move().")
    nb.md("## Рабочий пример")
    nb.code('''import math


def normalizovat(dx, dy):
    dlina = math.hypot(dx, dy)
    if dlina == 0:
        return (0.0, 0.0)
    return (dx / dlina, dy / dlina)


def zazhat_poziciyu(x, y, granicy):
    levaya, verhnyaya, pravaya, nizhnyaya = granicy
    return (max(levaya, min(x, pravaya)), max(verhnyaya, min(y, nizhnyaya)))


nx, ny = normalizovat(1, 1)
print("Нормализованный диагональный вектор:", (nx, ny))
print("Его длина:", math.hypot(nx, ny))

x, y = zazhat_poziciyu(-10, 1000, (0, 0, 480, 720))
print("Позиция после ограничения:", (x, y))''')
    nb.md("## Проверка результата")
    nb.code('''assert math.isclose(math.hypot(nx, ny), 1.0, abs_tol=1e-9)
assert (x, y) == (0, 720)
print("Верно: диагональ нормализована к единичной длине, позиция зажата в границах поля.")''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте, что горизонтальное и нормализованное "
          "диагональное перемещения на одинаковой скорости и dt дают одинаковую длину пути.")
    nb.code('''SKOROST, DT = 200.0, 1 / 60

pryamo = SKOROST * DT
dx, dy = normalizovat(1, 1)
diagonal = math.hypot(dx * SKOROST * DT, dy * SKOROST * DT)

assert math.isclose(pryamo, diagonal, rel_tol=1e-9)
print("Верно: нормализация делает диагональную скорость равной прямой, а не быстрее.")''')
    nb.write(OUT_DIR / "21-11-vector2.ipynb")
    print(f"Записано: 21-11 ({len(nb)} ячеек)")


def build_13() -> None:
    nb = NotebookBuilder()
    nb.md("# 21-13 · Скорострельность и кулдаун\n\nПрактика к разделу "
          "[«Скорострельность и кулдаун»]"
          "(../../site/chapters/glava-21/21-13-skorostrelnost.html).")
    nb.md("## Цель\n\nПосчитать, сколько выстрелов происходит при удержании огня в течение "
          "секунды, и убедиться, что результат не зависит от FPS.")
    nb.md("## Рабочий пример")
    nb.code('''FIRE_INTERVAL = 0.20


def vystrelov_za_sekundu(fps):
    cooldown = 0.0
    vystrelov = 0
    dt = 1 / fps
    for _ in range(fps):
        cooldown = max(0.0, cooldown - dt)
        if cooldown <= 0.0:
            vystrelov += 1
            cooldown = FIRE_INTERVAL
    return vystrelov


for fps in (30, 60, 120):
    print(fps, "FPS ->", vystrelov_za_sekundu(fps), "выстрелов")''')
    nb.md("## Проверка результата")
    nb.code('''znacheniya = [vystrelov_za_sekundu(fps) for fps in (30, 60, 120)]

assert max(znacheniya) - min(znacheniya) <= 1
assert all(v < 60 for v in znacheniya), "не должно быть выстрела на каждый кадр"
print("Верно: скорострельность почти не зависит от FPS и заметно меньше 60 выстрелов в секунду.")''')
    nb.write(OUT_DIR / "21-13-skorostrelnost.ipynb")
    print(f"Записано: 21-13 ({len(nb)} ячеек)")


def build_14() -> None:
    nb = NotebookBuilder()
    nb.md("# 21-14 · Появление врагов\n\nПрактика к разделу "
          "[«Появление врагов»](../../site/chapters/glava-21/21-14-poyavlenie-vragov.html).")
    nb.md("## Цель\n\nПроверить, что таймер появления врагов через while сохраняет "
          "«перелёт» времени, а не теряет его.")
    nb.md("## Рабочий пример")
    nb.code('''INTERVAL = 0.5


def poyavivshiesya_vragi(spawn_timer, dt):
    spawn_timer -= dt
    poyavilos = 0
    while spawn_timer <= 0.0:
        poyavilos += 1
        spawn_timer += INTERVAL
    return poyavilos, spawn_timer


poyavilos, ostatok = poyavivshiesya_vragi(INTERVAL, 1.2)
print("Заспавнилось врагов:", poyavilos)
print("Остаток таймера:", ostatok)''')
    nb.md("## Проверка результата")
    nb.code('''assert poyavilos == 2, "1.2 секунды при интервале 0.5 должны дать 2 полных интервала"
assert 0.0 < ostatok < INTERVAL
print("Верно: while не потерял остаток времени между интервалами.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nПроверьте координату появления врага: "
          "вся его ширина обязана остаться внутри игрового поля.")
    nb.code('''import random


def x_poyavleniya_vraga(rng, shirina_vraga, pole_levo, pole_pravo):
    levaya, pravaya = pole_levo, pole_pravo - shirina_vraga
    if pravaya <= levaya:
        return float(levaya)
    return rng.uniform(levaya, pravaya)


rng = random.Random(7)
for _ in range(200):
    x = x_poyavleniya_vraga(rng, 32, 0, 480)
    assert 0 <= x <= 480 - 32

print("Верно: враг всегда появляется полностью внутри игрового поля.")''')
    nb.write(OUT_DIR / "21-14-poyavlenie-vragov.ipynb")
    print(f"Записано: 21-14 ({len(nb)} ячеек)")


def build_15() -> None:
    nb = NotebookBuilder()
    nb.md("# 21-15 · Столкновения пуль и счёт\n\nПрактика к разделу "
          "[«Столкновения пуль и счёт»]"
          "(../../site/chapters/glava-21/21-15-stolknoveniya-i-schet.html).")
    nb.md("## Цель\n\nУбедиться, что очки за одного уничтоженного врага начисляются "
          "ровно один раз, даже если его задели две пули сразу.")
    nb.md("## Рабочий пример")
    nb.code('''def ochki_za_unichtozhennyh(vragi):
    return sum(ochki for _, ochki in vragi)


# Два "попадания" по одному и тому же врагу (одинаковый id) за одно обновление
vrag = ("vrag-1", 100)
popadaniya = [vrag, vrag]   # groupcollide() мог бы вернуть его дважды

unikalnye_vragi = set(popadaniya)
schet = ochki_za_unichtozhennyh(unikalnye_vragi)

print("Уникальных врагов в попаданиях:", len(unikalnye_vragi))
print("Начислено очков:", schet)''')
    nb.md("## Проверка результата")
    nb.code('''assert len(unikalnye_vragi) == 1
assert schet == 100, "врага, задетого дважды в одном обновлении, нельзя засчитать дважды"
print("Верно: подсчёт очков через set защищает от двойного начисления.")''')
    nb.write(OUT_DIR / "21-15-stolknoveniya.ipynb")
    print(f"Записано: 21-15 ({len(nb)} ячеек)")


def build_16() -> None:
    nb = NotebookBuilder()
    nb.md("# 21-16 · Урон кораблю и неуязвимость\n\nПрактика к разделу "
          "[«Урон кораблю и неуязвимость»]"
          "(../../site/chapters/glava-21/21-16-uron-i-neuyazvimost.html).")
    nb.md("## Цель\n\nПроверить, что несколько одновременных столкновений отнимают ровно "
          "одну жизнь, а неуязвимость блокирует урон до истечения таймера.")
    nb.md("## Рабочий пример")
    nb.code('''INVULNERABLE_SECONDS = 1.2


def primenit_stolknovenie(zhizni, invulnerable_timer, est_stolknovenie):
    if est_stolknovenie and invulnerable_timer <= 0.0:
        zhizni -= 1
        invulnerable_timer = INVULNERABLE_SECONDS
    return zhizni, invulnerable_timer


zhizni, timer = 3, 0.0
# Три врага столкнулись с кораблём в ОДНОМ обновлении -- это ОДНО событие "est_stolknovenie"
zhizni, timer = primenit_stolknovenie(zhizni, timer, est_stolknovenie=True)
print("Жизней после столкновения:", zhizni)''')
    nb.md("## Проверка результата")
    nb.code('''assert zhizni == 2, "одно событие столкновения должно отнять ровно одну жизнь"
assert timer == INVULNERABLE_SECONDS

# Повторное столкновение сразу же, пока ещё действует неуязвимость
zhizni2, timer2 = primenit_stolknovenie(zhizni, timer, est_stolknovenie=True)
assert zhizni2 == zhizni, "во время неуязвимости повторное столкновение не должно отнимать жизнь"
print("Верно: неуязвимость блокирует повторный урон сразу после первого удара.")''')
    nb.write(OUT_DIR / "21-16-uron.ipynb")
    print(f"Записано: 21-16 ({len(nb)} ячеек)")


def build_17() -> None:
    nb = NotebookBuilder()
    nb.md("# 21-17 · Рост сложности и волны\n\nПрактика к разделу "
          "[«Рост сложности и волны»](../../site/chapters/glava-21/21-17-slozhnost-i-volny.html).")
    nb.md("## Цель\n\nПроверить, что формулы сложности растут вместе со счётом, но не "
          "уходят за разумные границы.")
    nb.md("## Рабочий пример")
    nb.code('''BASE_SPAWN_INTERVAL = 1.10
MIN_SPAWN_INTERVAL = 0.35
SPAWN_FACTOR = 0.00055

MAX_SPEED_BONUS = 0.9
SPEED_FACTOR = 0.00045


def interval_poyavleniya_vraga(schet):
    return max(MIN_SPAWN_INTERVAL, BASE_SPAWN_INTERVAL - schet * SPAWN_FACTOR)


def mnozhitel_skorosti_vraga(schet):
    return 1.0 + min(MAX_SPEED_BONUS, schet * SPEED_FACTOR)


for schet in (0, 500, 5000):
    print(schet, "->", round(interval_poyavleniya_vraga(schet), 3), round(mnozhitel_skorosti_vraga(schet), 3))''')
    nb.md("## Проверка результата")
    nb.code('''assert interval_poyavleniya_vraga(0) == BASE_SPAWN_INTERVAL
assert interval_poyavleniya_vraga(100_000) == MIN_SPAWN_INTERVAL
assert interval_poyavleniya_vraga(500) < interval_poyavleniya_vraga(0)

assert mnozhitel_skorosti_vraga(0) == 1.0
assert mnozhitel_skorosti_vraga(100_000) == 1.0 + MAX_SPEED_BONUS
print("Верно: интервал спавна уменьшается, скорость растёт, обе формулы ограничены.")''')
    nb.write(OUT_DIR / "21-17-slozhnost.ipynb")
    print(f"Записано: 21-17 ({len(nb)} ячеек)")


def build_20() -> None:
    nb = NotebookBuilder()
    nb.md("# 21-20 · Анимация взрыва\n\nПрактика к разделу "
          "[«Анимация взрыва»](../../site/chapters/glava-21/21-20-animatsiya-vzryva.html).")
    nb.md("## Цель\n\nПроверить, что таймер анимации взрыва сохраняет остаток времени при "
          "одном длинном кадре, вместо того чтобы терять его.")
    nb.md("## Рабочий пример")
    nb.code('''FRAME_INTERVAL = 0.055
KADROV_VSEGO = 6


def prodvinut_animaciyu(frame_index, animation_time, dt):
    animation_time += dt
    while animation_time >= FRAME_INTERVAL:
        animation_time -= FRAME_INTERVAL
        frame_index += 1
        if frame_index >= KADROV_VSEGO:
            return frame_index, animation_time, True   # анимация завершена
    return frame_index, animation_time, False


frame_index, animation_time, zavershena = prodvinut_animaciyu(0, 0.0, FRAME_INTERVAL * 2.4)
print("Кадр анимации:", frame_index)
print("Остаток времени:", animation_time)''')
    nb.md("## Проверка результата")
    nb.code('''assert frame_index == 2, "2.4 интервала должны продвинуть анимацию на 2 полных кадра"
assert 0.0 < animation_time < FRAME_INTERVAL
assert zavershena is False
print("Верно: длинный кадр продвинул анимацию сразу на несколько кадров без потери времени.")''')
    nb.write(OUT_DIR / "21-20-animatsiya.ipynb")
    print(f"Записано: 21-20 ({len(nb)} ячеек)")


def build_25() -> None:
    nb = NotebookBuilder()
    nb.md("# 21-25 · Финальная версия игры\n\nПрактика к разделу "
          "[«Финальная версия игры»]"
          "(../../site/chapters/glava-21/21-25-finalnaya-arhitektura.html). "
          "Полный файл — `projects/pygame/space-shooter/space_shooter.py`.")
    nb.md("## Цель\n\nЗапустить настоящий класс Game из финальной игры, прогнать несколько "
          "секунд симуляции и убедиться, что счёт, жизни и объекты ведут себя как единое целое.")
    nb.md(LOOP_NOTE_MD)
    nb.md("## Рабочий пример")
    nb.code('''import random
import sys

sys.path.insert(0, "../../projects/pygame/space-shooter")

import space_shooter as ss

game = ss.Game(rng=random.Random(11))
game.start_new_game()

for _ in range(180):   # 3 симулированные секунды
    game.update(1 / 60)
    game.render()

print("Состояние:", game.state)
print("Счёт:", game.score)
print("Врагов на поле:", len(game.enemies))''')
    nb.md("## Проверка результата")
    nb.code('''assert game.state in (ss.GameStatus.PLAYING, ss.GameStatus.GAME_OVER)
assert game.score >= 0
assert game.lives >= 0
print("Верно: финальная игра проходит несколько секунд симуляции без ошибок.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nВручную создайте столкновение пули с "
          "врагом через `game.resolve_bullet_enemy_collisions()` и убедитесь, что счёт "
          "увеличивается ровно на стоимость одного врага.")
    nb.code('''tochka = (game.player.rect.centerx, 300.0)
vrag = ss.Enemy(game.assets.images["enemy_scout"], tochka, points=100, speed=0.0)
game.enemies.add(vrag)
pulya = ss.Bullet(game.assets.images["bullet"], tochka)
game.bullets.add(pulya)

schet_do = game.score
game.score += game.resolve_bullet_enemy_collisions()

assert game.score == schet_do + 100
print("Верно: столкновение пули и врага добавило ровно 100 очков.")''')
    nb.write(OUT_DIR / "21-25-final.ipynb")
    print(f"Записано: 21-25 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_01()
    build_02()
    build_03()
    build_04()
    build_06()
    build_08()
    build_09()
    build_11()
    build_13()
    build_14()
    build_15()
    build_16()
    build_17()
    build_20()
    build_25()
