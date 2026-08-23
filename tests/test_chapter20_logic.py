"""Регрессионный набор для чистой игровой логики главы 20 (кадры/FPS, delta
time, столкновения, физика, состояния) — работает через SDL dummy-драйверы,
поэтому не требует ни Xvfb, ни настоящего дисплея (раздел 20.16, 20.21,
20.22, 20.25).
"""

import math
import os
import sys
from enum import Enum, auto
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

ROOT = Path(__file__).resolve().parent.parent
BALL_DIR = ROOT / "projects" / "pygame" / "bouncing-ball"
sys.path.insert(0, str(BALL_DIR))

import bouncing_ball as bb  # noqa: E402
import bouncing_ball_basic as bb_basic  # noqa: E402


# ---------- 20.15 — FPS и бюджет кадра ----------

def test_frame_budget_matches_fps():
    for fps, ozhidaemyj_ms in ((30, 33.333), (60, 16.667), (120, 8.333)):
        byudzhet_ms = 1000 / fps
        assert math.isclose(byudzhet_ms, ozhidaemyj_ms, abs_tol=0.001)


# ---------- 20.16 — delta time: ОБЯЗАТЕЛЬНЫЙ регрессионный тест ----------

def test_dt_based_movement_is_fps_independent():
    """Прямое доказательство раздела 20.16 и 20.33: движение через
    `x += vx * dt` за одно и то же реальное время даёт один и тот же
    результат независимо от того, на сколько шагов это время было нарезано
    (30, 60 или 120 "кадров" в секунду). Мяч расположен и направлен так,
    чтобы за одну симулируемую секунду не долететь ни до одной стены —
    иначе итог перестаёт быть детерминированным (столкновение делает
    дальнейшую траекторию чувствительной к точному моменту отскока, что уже
    вопрос раздела 20.21/20.22, а не самого delta time)."""
    itogi = {}
    for fps in (30, 60, 120):
        game = bb.BouncingBallGame()
        game.x, game.y = 300.0, 200.0
        game.vx, game.vy = 50.0, 30.0   # пикселей в секунду, заведомо не долетит до стены за 1 секунду
        dt = 1 / fps
        for _ in range(fps):   # ровно 1.0 секунда реального времени, из fps шагов
            game.update(dt)
        itogi[fps] = (game.x, game.y)

    x30, y30 = itogi[30]
    x60, y60 = itogi[60]
    x120, y120 = itogi[120]

    assert math.isclose(x30, x60, abs_tol=1e-6)
    assert math.isclose(x60, x120, abs_tol=1e-6)
    assert math.isclose(y30, y60, abs_tol=1e-6)
    assert math.isclose(y60, y120, abs_tol=1e-6)

    # За 1 секунду на скорости (50, 30) мяч обязан сместиться ровно на (50, 30)
    assert math.isclose(x60, 350.0, abs_tol=1e-6)
    assert math.isclose(y60, 230.0, abs_tol=1e-6)


def test_naive_per_frame_movement_is_not_fps_independent():
    """Контрольный, "отрицательный" тест: наивное движение в стиле
    bouncing_ball_basic.py ("+= dx за кадр", без delta time) НЕ обладает
    свойством из теста выше — итоговое смещение за одну и ту же реальную
    секунду растёт вместе с числом кадров, потому что каждый кадр
    прибавляет одну и ту же константу независимо от того, сколько реального
    времени этот кадр занял. Это ровно та ошибка, о которой предупреждает
    раздел 20.16 — здесь она воспроизведена намеренно, чтобы контраст с
    тестом выше был доказанным фактом, а не просто утверждением в тексте
    главы."""
    dx_za_kadr = 5.0   # "пикселей за кадр", НЕ пикселей в секунду

    def proshlo_kadrov_za_sekundu(fps):
        x = 0.0
        for _ in range(fps):   # 1.0 секунда, нарезанная на fps кадров
            x += dx_za_kadr
        return x

    smeshenie_30 = proshlo_kadrov_za_sekundu(30)
    smeshenie_60 = proshlo_kadrov_za_sekundu(60)
    smeshenie_120 = proshlo_kadrov_za_sekundu(120)

    assert smeshenie_30 == 30 * dx_za_kadr
    assert smeshenie_60 == 60 * dx_za_kadr
    assert smeshenie_120 == 120 * dx_za_kadr
    # На 120 FPS мяч за ту же секунду улетает вчетверо дальше, чем на 30 FPS —
    # именно такого разброса и не должно быть у версии с delta time выше.
    assert smeshenie_120 == 4 * smeshenie_30
    assert smeshenie_120 != smeshenie_30


# ---------- 20.16 — нормализация диагонального движения ----------

def test_diagonal_push_keeps_speed_magnitude():
    """tolknut_k_tochke() использует normalizovat() именно для того, чтобы
    скорость после клика мышью не зависела от расстояния до точки клика —
    без нормализации она была бы пропорциональна этому расстоянию."""
    game = bb.BouncingBallGame()
    game.x, game.y = 300.0, 200.0
    game.vx, game.vy = 120.0, -40.0
    skorost_do = math.hypot(game.vx, game.vy)

    game.tolknut_k_tochke(game.x + 3, game.y + 3)   # близкая точка клика
    skorost_blizko = math.hypot(game.vx, game.vy)

    game.vx, game.vy = 120.0, -40.0
    game.tolknut_k_tochke(game.x + 900, game.y + 900)   # далёкая точка клика
    skorost_daleko = math.hypot(game.vx, game.vy)

    assert math.isclose(skorost_do, skorost_blizko, rel_tol=1e-9)
    assert math.isclose(skorost_do, skorost_daleko, rel_tol=1e-9)


def test_normalizovat_returns_unit_vector():
    nx, ny = bb.normalizovat(3.0, 4.0)   # классический треугольник 3-4-5
    assert math.isclose(math.hypot(nx, ny), 1.0, abs_tol=1e-9)
    assert math.isclose(nx, 0.6, abs_tol=1e-9)
    assert math.isclose(ny, 0.8, abs_tol=1e-9)


def test_normalizovat_zero_vector_is_safe():
    assert bb.normalizovat(0.0, 0.0) == (0.0, 0.0)


# ---------- 20.5 / 20.33 — clamp: позиция не перелетает границу поля ----------

def test_clamp_keeps_ball_inside_field_on_overshoot():
    """Даже если один шаг физики "перелетает" границу поля целиком (крупный
    dx за один кадр), позиция после отскока должна быть прижата ровно к
    границе, а не оставлена за её пределами."""
    x, y, dx, dy = bb_basic.shag_fiziki(bb_basic.SHIRINA - 5, 200, 500, 0)
    assert x == bb_basic.SHIRINA - bb_basic.RADIUS
    assert dx == -500

    x, y, dx, dy = bb_basic.shag_fiziki(5, 200, -500, 0)
    assert x == bb_basic.RADIUS
    assert dx == 500


# ---------- 20.21 — столкновения: AABB-проверка пересечения прямоугольников ----------

def pryamougolniki_peresekayutsya(a, b):
    """Та же самая AABB-проверка, что показана на странице 20.21 —
    продублирована здесь как чистая функция, чтобы её можно было
    протестировать без Pygame и без реального окна."""
    ax1, ay1, aw, ah = a
    bx1, by1, bw, bh = b
    ax2, ay2 = ax1 + aw, ay1 + ah
    bx2, by2 = bx1 + bw, by1 + bh
    return ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1


def test_aabb_overlap_true_for_overlapping_rects():
    assert pryamougolniki_peresekayutsya((0, 0, 40, 40), (20, 20, 40, 40)) is True


def test_aabb_overlap_false_for_distant_rects():
    assert pryamougolniki_peresekayutsya((0, 0, 40, 40), (200, 200, 40, 40)) is False


def test_aabb_overlap_false_for_merely_touching_edges():
    # Прямоугольники соприкасаются краем (правый край A == левый край B),
    # но не пересекаются площадью — строгое неравенство должно это различать.
    assert pryamougolniki_peresekayutsya((0, 0, 40, 40), (40, 0, 40, 40)) is False


def test_colliderect_agrees_with_manual_aabb():
    import pygame  # noqa: PLC0415 — требует SDL_VIDEODRIVER=dummy, уже выставлен выше

    a = (10, 10, 30, 30)
    b = (25, 25, 30, 30)
    rect_a, rect_b = pygame.Rect(*a), pygame.Rect(*b)
    assert rect_a.colliderect(rect_b) == pryamougolniki_peresekayutsya(a, b) is True


# ---------- 20.21 — Rect.inflate(): меняет ОБЩИЙ размер, сохраняя центр ----------

def test_rect_inflate_changes_total_size_not_per_side():
    """Раздел 20.21: rect.inflate(x, y) меняет ширину на x и высоту на y
    ЦЕЛИКОМ (не на x/y с каждой стороны), сохраняя центр прямоугольника —
    поэтому rect.inflate(-20, -20) убирает 20 пикселей суммарно по каждой
    оси, то есть примерно 10 пикселей с каждой стороны."""
    import pygame  # noqa: PLC0415 — требует SDL_VIDEODRIVER=dummy, уже выставлен выше

    rect = pygame.Rect(0, 0, 100, 100)
    smaller = rect.inflate(-20, -20)

    assert smaller.size == (80, 80)
    assert smaller.center == rect.center


# ---------- 20.22 — простая физика: отскок с затуханием ----------

def test_bounce_with_damping_loses_speed_but_keeps_direction_flip():
    koeff_otskoka = 0.8
    skorost_do = -300.0   # летит вверх (отрицательный Y — раздел 20.18)
    skorost_posle = -skorost_do * koeff_otskoka
    assert skorost_posle == 240.0
    assert skorost_posle > 0   # направление развернулось
    assert skorost_posle < abs(skorost_do)   # но по модулю стало меньше


def test_repeated_damped_bounces_eventually_settle_below_threshold():
    koeff_otskoka = 0.8
    skorost = 300.0
    otskokov = 0
    while skorost > 1.0 and otskokov < 200:
        skorost *= koeff_otskoka
        otskokov += 1
    assert skorost <= 1.0
    assert otskokov < 200   # действительно затухает, а не зацикливается вечно


# ---------- 20.22 — trenie: ОБЯЗАТЕЛЬНЫЙ регрессионный тест на dt ----------

def _primenit_trenie_dt(skorost, trenie, dt):
    """Тот же dt-based алгоритм торможения, что показан на странице 20.22:
    ускорение торможения в px/s^2, умноженное на dt, а не постоянный
    коэффициент, умножаемый на скорость каждый кадр."""
    if skorost > 0:
        return max(0.0, skorost - trenie * dt)
    elif skorost < 0:
        return min(0.0, skorost + trenie * dt)
    return skorost


def test_dt_based_friction_is_fps_independent():
    """Обязательный регрессионный тест раздела 20.22: одна и та же реальная
    секунда торможения, нарезанная на 30, 60 или 120 шагов, обязана дать
    приблизительно одинаковую итоговую скорость -- иначе трение, как и
    нескорректированное движение из раздела 20.16, зависело бы от FPS."""
    TRENIE = 300.0
    NACHALNAYA_SKOROST = 250.0

    itogi = {}
    for fps in (30, 60, 120):
        skorost = NACHALNAYA_SKOROST
        dt = 1 / fps
        for _ in range(fps):   # ровно 1.0 секунда реального времени
            skorost = _primenit_trenie_dt(skorost, TRENIE, dt)
        itogi[fps] = skorost

    assert math.isclose(itogi[30], itogi[60], abs_tol=1e-6)
    assert math.isclose(itogi[60], itogi[120], abs_tol=1e-6)
    # За 1 секунду скорость обязана снизиться ровно на TRENIE (250 - 300 -> упёрлась в 0)
    assert itogi[60] == 0.0


def test_naive_per_frame_friction_is_not_fps_independent():
    """Контрольный, "отрицательный" тест: наивное торможение "умножить
    скорость на константу каждый кадр" (без dt) НЕ обладает свойством из
    теста выше -- на более высоком FPS такое умножение срабатывает чаще за
    ту же реальную секунду, и объект останавливается быстрее."""
    KOEFFICIENT = 0.98

    def naivnoe_tormozhenie(fps):
        skorost = 250.0
        for _ in range(fps):   # 1.0 секунда, нарезанная на fps кадров
            skorost *= KOEFFICIENT
        return skorost

    skorost_30 = naivnoe_tormozhenie(30)
    skorost_60 = naivnoe_tormozhenie(60)
    skorost_120 = naivnoe_tormozhenie(120)

    assert skorost_30 != skorost_60
    assert skorost_60 != skorost_120
    # Больше кадров за ту же секунду -> сильнее суммарное торможение
    assert skorost_120 < skorost_60 < skorost_30


# ---------- 20.25 — состояния игры: разрешённые переходы ----------

class _SostoyanieDlyaTesta(Enum):
    MENU = auto()
    IGRA = auto()
    PAUZA = auto()
    GAME_OVER = auto()


_RAZRESHENNYE_PEREHODY = {
    _SostoyanieDlyaTesta.MENU: {_SostoyanieDlyaTesta.IGRA},
    _SostoyanieDlyaTesta.IGRA: {_SostoyanieDlyaTesta.PAUZA, _SostoyanieDlyaTesta.GAME_OVER},
    _SostoyanieDlyaTesta.PAUZA: {_SostoyanieDlyaTesta.IGRA},
    _SostoyanieDlyaTesta.GAME_OVER: {_SostoyanieDlyaTesta.MENU},
}


def test_menu_cannot_jump_directly_to_game_over():
    assert _SostoyanieDlyaTesta.GAME_OVER not in _RAZRESHENNYE_PEREHODY[_SostoyanieDlyaTesta.MENU]


def test_every_state_has_at_least_one_way_out():
    for sostoyanie, dostupnye in _RAZRESHENNYE_PEREHODY.items():
        assert len(dostupnye) >= 1, f"{sostoyanie} — тупиковое состояние без переходов"


def test_pause_only_reachable_from_and_returns_to_igra():
    assert _RAZRESHENNYE_PEREHODY[_SostoyanieDlyaTesta.PAUZA] == {_SostoyanieDlyaTesta.IGRA}
    assert _SostoyanieDlyaTesta.PAUZA in _RAZRESHENNYE_PEREHODY[_SostoyanieDlyaTesta.IGRA]


# ---------- 20.26 — пауза действительно останавливает update(), не только render() ----------

def test_pause_freezes_update_not_only_render():
    game = bb.BouncingBallGame()
    game.toggle_pause()
    assert game.state is bb.SostoyanieIgry.PAUZA
    do = (game.x, game.y, game.vx, game.vy, game.otskokov, game.schet)
    for _ in range(120):
        game.update(1 / 60)
    assert (game.x, game.y, game.vx, game.vy, game.otskokov, game.schet) == do


# ---------- 20.23 — таймер анимации: аккумулятор сохраняет "перелёт" времени ----------

def _prodvinut_kadr_animacii(tekushij_kadr, vremya_animacii, dt, interval_kadra, kolichestvo_kadrov):
    """Тот же while-based алгоритм таймера анимации, что показан на
    странице 20.23: копит dt в аккумуляторе vremya_animacii и продвигает
    кадр столько раз подряд, сколько целых интервалов туда поместилось —
    ничего не теряя, даже если один игровой кадр длиннее одного интервала
    анимации."""
    vremya_animacii += dt
    while vremya_animacii >= interval_kadra:
        vremya_animacii -= interval_kadra
        tekushij_kadr = (tekushij_kadr + 1) % kolichestvo_kadrov
    return tekushij_kadr, vremya_animacii


def test_animation_accumulator_preserves_overshoot_across_frames():
    """Обязательный регрессионный тест раздела 20.23: один длинный игровой
    кадр (dt = 0.32 c) при интервале анимации 0.10 c обязан продвинуть кадр
    анимации ровно на 3 позиции за один вызов, а не на 1 (как было бы у
    старой версии с if вместо while, которая теряла лишние 0.22 c), и
    сохранить остаток в аккумуляторе. dt намеренно не кратен interval_kadra
    ровно (0.32, а не 0.30) — чтобы сравнение не попадало на границу
    интервала, где точное равенство float ненадёжно само по себе."""
    tekushij_kadr, vremya_animacii = _prodvinut_kadr_animacii(
        tekushij_kadr=0, vremya_animacii=0.0, dt=0.32,
        interval_kadra=0.10, kolichestvo_kadrov=10,
    )
    assert tekushij_kadr == 3
    assert math.isclose(vremya_animacii, 0.02, abs_tol=1e-9)


def test_animation_accumulator_is_fps_independent_over_equal_elapsed_time():
    """Ровно одна и та же реальная секунда анимации, нарезанная на 30, 60
    или 120 игровых кадров, обязана продвинуть счётчик кадра анимации на
    одинаковое число позиций — иначе таймер анимации зависел бы от FPS,
    как нескорректированное движение из раздела 20.16. Интервал 0.12 c —
    тот же INTERVAL_KADRA, что и на странице 20.23; он выбран специально,
    чтобы не делить секунду ровно нацело и не попадать на границу
    интервала, где сравнение float с "==" ненадёжно само по себе."""
    INTERVAL_KADRA = 0.12
    KOLICHESTVO_KADROV = 1000   # достаточно большое, чтобы не зацикливаться в тесте

    itogi = {}
    for fps in (30, 60, 120):
        tekushij_kadr, vremya_animacii = 0, 0.0
        dt = 1 / fps
        for _ in range(fps):   # ровно 1.0 секунда реального времени
            tekushij_kadr, vremya_animacii = _prodvinut_kadr_animacii(
                tekushij_kadr, vremya_animacii, dt, INTERVAL_KADRA, KOLICHESTVO_KADROV,
            )
        itogi[fps] = tekushij_kadr

    # 1.0 с / 0.12 с = 8 целых интервалов и 0.04 с в остатке
    assert itogi[30] == itogi[60] == itogi[120] == 8
