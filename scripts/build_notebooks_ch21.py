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

SHIRINA, VYSOTA = 500, 600
FPS = 60

KORABL_SHIRINA, KORABL_VYSOTA = 50, 40
KORABL_SKOROST = 6

PULYA_SHIRINA, PULYA_VYSOTA = 4, 12
PULYA_SKOROST = 9

VRAG_SHIRINA, VRAG_VYSOTA = 40, 30
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

SHIRINA, VYSOTA = 500, 600
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
screen = pygame.display.set_mode((500, 600))
assert screen.get_size() == (500, 600)
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
screen = pygame.display.set_mode((500, 600))
clock = pygame.time.Clock()

KORABL_SHIRINA, KORABL_VYSOTA = 50, 40
korabl = pygame.Rect(500 // 2 - KORABL_SHIRINA // 2, 600 - KORABL_VYSOTA - 20,
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
screen = pygame.display.set_mode((500, 600))
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

for kadr in range(400):
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
    nb.code('''assert state["igra_okonchena"] is True, "за 400 кадров хотя бы один враг должен долететь до низа экрана"
assert kadr + 1 <= 400
print(f"Верно: игра завершилась на кадре {kadr + 1} со счётом {state['schet']}.")
pygame.quit()''')
    nb.write(OUT_DIR / "21-08-polnaya-igra.ipynb")
    print(f"Записано: 21-08 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_01()
    build_02()
    build_03()
    build_04()
    build_06()
    build_08()
