"""Игра «Космический шутер» на Pygame.

Проект к главе 21 книги «Python с нуля» (Cartesian School).
Запуск: python space_shooter.py
Управление: стрелки влево/вправо — движение, пробел — выстрел.
"""

import random

import pygame

SHIRINA, VYSOTA = 500, 600
FPS = 60

KORABL_SHIRINA, KORABL_VYSOTA = 50, 40
KORABL_SKOROST = 6

PULYA_SHIRINA, PULYA_VYSOTA = 4, 12
PULYA_SKOROST = 9

VRAG_SHIRINA, VRAG_VYSOTA = 40, 30
VRAG_SKOROST = 2
INTERVAL_POYAVLENIYA_VRAGA = 45  # кадров между новыми врагами

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
    """Возвращает свежий словарь состояния игры."""
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

    # пули летят вверх; убираем те, что улетели за экран
    for pulya in state["puli"]:
        pulya.y -= PULYA_SKOROST
    state["puli"] = [p for p in state["puli"] if p.bottom > 0]

    # враги появляются периодически и двигаются вниз
    state["kadrov_do_vraga"] -= 1
    if state["kadrov_do_vraga"] <= 0:
        state["vragi"].append(sozdat_vraga())
        state["kadrov_do_vraga"] = INTERVAL_POYAVLENIYA_VRAGA

    for vrag in state["vragi"]:
        vrag.y += VRAG_SKOROST

    # столкновение пуль с врагами — уничтожаем обоих, начисляем очки
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

    # враг долетел до низа экрана или столкнулся с кораблём — игра окончена
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

    pygame.display.flip()


def glavnyj_cikl():
    state = novaya_igra()
    rabotaet = True
    while rabotaet:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rabotaet = False
            elif (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                and not state["igra_okonchena"]
            ):
                vystrelit(state)

        klavishi = pygame.key.get_pressed()
        obrabotat_klavishi(state, klavishi)
        obnovit_igru(state)
        narisovat(state)
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    glavnyj_cikl()
