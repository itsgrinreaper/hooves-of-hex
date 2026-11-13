"""
Hooves of Hex — a Grin Reaper arcade shooter.

Built with: Python + Pygame.

The black goat has had ENOUGH of the haunting backlog. Armed with enchanted
hooves and highly questionable aim, he blasts the descending dead back into
the filing system. The white lamb is a protected species. The Raven provides
commentary nobody requested.

Controls: Arrow keys / A,D to move, SPACE to fire, ENTER to start, R to retry.
Works on desktop (python main.py) and in the browser via pygbag.
"""

import asyncio
import math
import os
import random
import sys

import pygame

WIDTH, HEIGHT = 800, 600
FPS = 60

# --- palette: pink / purple / gold on near-black (brand) ---
BG = (16, 10, 26)
BG2 = (28, 16, 44)
PINK = (244, 167, 200)
PINK_DEEP = (214, 90, 148)
PURPLE = (124, 84, 196)
GOLD = (212, 175, 55)
IVORY = (245, 242, 232)
GREY = (160, 152, 178)
BLACK = (8, 6, 12)
GOAT = (26, 22, 34)
GHOST = (216, 208, 240)
DEMON = (196, 88, 120)
SKULL = (238, 234, 220)
LAMB = (250, 248, 244)

AUTOTEST = "--autotest" in sys.argv or os.environ.get("GRIN_AUTOTEST") == "1"
TITLETEST = "--titletest" in sys.argv

RAVEN_IDLE = [
    "The dead are descending. Paperwork follows.",
    "Aim is a courtesy. Panic is also accepted.",
    "He files his hooves under 'weapons'. Correctly.",
    "Somewhere, Death is taking notes. And credit.",
    "The lamb is protected. The ghosts are not.",
]
RAVEN_LAMB_SHOT = "You shot the LAMB. There will be a hearing."
RAVEN_LAMB_SAFE = "The lamb crosses unharmed. Mercy, filed."
RAVEN_ROSE = "A golden rose. Rapid hooves. Terrible idea, great results."
RAVEN_LEAK = "One got through. The graveyard accepts walk-ins now, apparently."
RAVEN_WAVE = "More dead inbound. They brought friends. Rude."


# ---------------------------------------------------------------- drawing ---
def draw_death_face(surf, cx, cy, r):
    """Death's skull face — FIXED, exactly as the official logo, always:
    narrow evil slanted eyes angled toward the nose, small dark nose hole,
    and a mouth that is a FLAT straight row of small scalloped teeth.
    Never smiling, never laughing, never any other expression."""
    pygame.draw.ellipse(surf, IVORY, (cx - r, cy - r, r * 2, r * 2))
    pygame.draw.rect(surf, IVORY, (cx - r * 0.55, cy + r * 0.45, r * 1.1, r * 0.5))
    # evil slanted eyes (angled down toward the nose)
    ex, ey, ew, eh = r * 0.52, r * 0.18, r * 0.52, r * 0.30
    pygame.draw.polygon(surf, BLACK, [(cx - ex - ew / 2, cy - ey - eh), (cx - ex + ew / 2, cy - ey + eh * 0.2),
                                      (cx - ex + ew / 2, cy - ey + eh), (cx - ex - ew / 2, cy - ey + eh * 0.4)])
    pygame.draw.polygon(surf, BLACK, [(cx + ex + ew / 2, cy - ey - eh), (cx + ex - ew / 2, cy - ey + eh * 0.2),
                                      (cx + ex - ew / 2, cy - ey + eh), (cx + ex + ew / 2, cy - ey + eh * 0.4)])
    # small nose hole
    pygame.draw.polygon(surf, BLACK, [(cx, cy + r * 0.08), (cx - r * 0.11, cy + r * 0.34), (cx + r * 0.11, cy + r * 0.34)])
    # mouth: flat straight row of small scalloped teeth — a straight line, never a curve
    my = cy + r * 0.66
    n = 6
    tw = (r * 1.0) / n
    for i in range(n):
        x = cx - r * 0.5 + i * tw
        pygame.draw.arc(surf, BLACK, (x, my - tw * 0.5, tw, tw), math.pi, 2 * math.pi, 2)
    pygame.draw.line(surf, BLACK, (cx - r * 0.5, my), (cx + r * 0.5, my), 2)


def draw_death(surf, cx, cy, s=1.0):
    r = int(26 * s)
    # robe
    pygame.draw.polygon(surf, BLACK, [(cx - r * 1.5, cy + r * 3.2), (cx + r * 1.5, cy + r * 3.2), (cx, cy - r * 0.4)])
    # wing
    pygame.draw.polygon(surf, (20, 16, 30), [(cx - r * 0.8, cy), (cx - r * 2.6, cy - r * 1.2),
                                             (cx - r * 2.0, cy + r * 0.2), (cx - r * 2.7, cy + r * 0.6), (cx - r * 1.2, cy + r * 0.9)])
    # hood
    pygame.draw.circle(surf, BLACK, (cx, cy), int(r * 1.25))
    draw_death_face(surf, cx, cy + int(r * 0.1), int(r * 0.82))
    # scythe
    pygame.draw.line(surf, (90, 70, 50), (cx + r * 1.5, cy + r * 3.0), (cx + r * 1.9, cy - r * 1.6), max(2, int(4 * s)))
    pygame.draw.arc(surf, (200, 200, 210), (cx + r * 0.7, cy - r * 2.3, r * 2.2, r * 1.4), math.pi * 0.95, math.pi * 1.75, max(2, int(5 * s)))


def draw_unicorn(surf, cx, cy, s=1.0, flip=False):
    d = -1 if flip else 1
    # body
    pygame.draw.ellipse(surf, PINK, (cx - 34 * s, cy - 14 * s, 68 * s, 30 * s))
    # legs
    for lx in (-24, -8, 14, 26):
        pygame.draw.rect(surf, PINK, (cx + lx * s - 3 * s, cy + 10 * s, 6 * s, 16 * s))
    # neck + head
    pygame.draw.polygon(surf, PINK, [(cx + d * 22 * s, cy - 8 * s), (cx + d * 40 * s, cy - 30 * s), (cx + d * 52 * s, cy - 24 * s), (cx + d * 34 * s, cy - 2 * s)])
    pygame.draw.circle(surf, PINK, (int(cx + d * 46 * s), int(cy - 26 * s)), int(11 * s))
    # horn (striped)
    pygame.draw.polygon(surf, GOLD, [(cx + d * 50 * s, cy - 34 * s), (cx + d * 62 * s, cy - 52 * s), (cx + d * 56 * s, cy - 30 * s)])
    # mane + tail
    pygame.draw.polygon(surf, PINK_DEEP, [(cx + d * 26 * s, cy - 30 * s), (cx + d * 36 * s, cy - 34 * s), (cx + d * 30 * s, cy - 6 * s)])
    pygame.draw.polygon(surf, PINK_DEEP, [(cx - d * 34 * s, cy - 12 * s), (cx - d * 46 * s, cy + 6 * s), (cx - d * 32 * s, cy + 10 * s)])
    # plain dot eye + small smile (the unicorn may smile; only Death's face is fixed)
    pygame.draw.circle(surf, BLACK, (int(cx + d * 48 * s), int(cy - 28 * s)), max(1, int(1.8 * s)))
    pygame.draw.arc(surf, BLACK, (cx + d * 46 * s - 4 * s, cy - 24 * s, 8 * s, 6 * s), math.pi * 1.15, math.pi * 1.85, max(1, int(1.5 * s)))


def draw_raven(surf, cx, cy, s=1.0):
    pygame.draw.ellipse(surf, BLACK, (cx - 13 * s, cy - 7 * s, 26 * s, 15 * s))
    pygame.draw.circle(surf, BLACK, (int(cx + 11 * s), int(cy - 9 * s)), int(7 * s))
    pygame.draw.polygon(surf, GOLD, [(cx + 16 * s, cy - 10 * s), (cx + 25 * s, cy - 7 * s), (cx + 16 * s, cy - 4 * s)])
    pygame.draw.polygon(surf, BLACK, [(cx - 12 * s, cy - 2 * s), (cx - 24 * s, cy + 4 * s), (cx - 11 * s, cy + 6 * s)])
    pygame.draw.circle(surf, IVORY, (int(cx + 12 * s), int(cy - 10 * s)), max(1, int(1.6 * s)))


def draw_goat(surf, cx, cy, rapid=False):
    # backlight so the black goat reads against the night
    glow = pygame.Surface((130, 110), pygame.SRCALPHA)
    pygame.draw.ellipse(glow, (124, 84, 196, 70), (0, 0, 130, 110))
    surf.blit(glow, (cx - 65, cy - 52))
    # legs
    for lx in (-20, -7, 8, 20):
        pygame.draw.rect(surf, GOAT, (cx + lx - 3, cy + 16, 6, 14))
        pygame.draw.rect(surf, GOLD if rapid else (70, 60, 84), (cx + lx - 4, cy + 28, 8, 5))  # hooves
    # body
    pygame.draw.ellipse(surf, (40, 33, 54), (cx - 30, cy - 6, 60, 30))
    pygame.draw.ellipse(surf, (96, 78, 128), (cx - 30, cy - 6, 60, 30), 2)
    # head
    pygame.draw.ellipse(surf, GOAT, (cx - 13, cy - 34, 26, 30))
    pygame.draw.polygon(surf, GOAT, [(cx - 6, cy - 8), (cx + 6, cy - 8), (cx, cy + 4)])  # muzzle
    # goatee
    pygame.draw.polygon(surf, IVORY, [(cx - 4, cy - 2), (cx + 4, cy - 2), (cx, cy + 10)])
    # horns (gold, curved suggestion)
    pygame.draw.arc(surf, GOLD, (cx - 22, cy - 46, 18, 20), math.pi * 0.4, math.pi * 1.5, 4)
    pygame.draw.arc(surf, GOLD, (cx + 4, cy - 46, 18, 20), math.pi * 1.5, math.pi * 0.6 + 2 * math.pi, 4)
    # ears
    pygame.draw.ellipse(surf, GOAT, (cx - 24, cy - 28, 12, 6))
    pygame.draw.ellipse(surf, GOAT, (cx + 12, cy - 28, 12, 6))
    pygame.draw.ellipse(surf, PINK, (cx - 22, cy - 26.5, 8, 3))
    pygame.draw.ellipse(surf, PINK, (cx + 14, cy - 26.5, 8, 3))
    # determined gold eyes
    pygame.draw.circle(surf, GOLD, (cx - 6, cy - 22), 3)
    pygame.draw.circle(surf, GOLD, (cx + 6, cy - 22), 3)
    # pentagram collar tag
    pygame.draw.circle(surf, GOLD, (cx, cy + 2), 4, 1)


def draw_ghost(surf, cx, cy, kind):
    color = {"ghost": GHOST, "demon": DEMON, "skull": SKULL}[kind]
    if kind == "skull":
        pygame.draw.ellipse(surf, color, (cx - 15, cy - 16, 30, 30))
        pygame.draw.rect(surf, color, (cx - 9, cy + 8, 18, 9))
        pygame.draw.circle(surf, BLACK, (cx - 7, cy - 2), 5)
        pygame.draw.circle(surf, BLACK, (cx + 7, cy - 2), 5)
        pygame.draw.polygon(surf, BLACK, [(cx, cy + 2), (cx - 3, cy + 8), (cx + 3, cy + 8)])
        for i in (-5, 0, 5):
            pygame.draw.line(surf, BLACK, (cx + i, cy + 10), (cx + i, cy + 16), 2)
        return
    # chibi spirit body with wavy hem
    pygame.draw.ellipse(surf, color, (cx - 16, cy - 17, 32, 30))
    pts = [(cx - 16, cy + 10)]
    for i in range(5):
        pts.append((cx - 16 + i * 8 + 4, cy + (4 if i % 2 else 12)))
    pts.append((cx + 16, cy + 10))
    pygame.draw.polygon(surf, color, pts)
    if kind == "demon":
        pygame.draw.polygon(surf, (120, 30, 60), [(cx - 14, cy - 14), (cx - 8, cy - 26), (cx - 4, cy - 13)])
        pygame.draw.polygon(surf, (120, 30, 60), [(cx + 14, cy - 14), (cx + 8, cy - 26), (cx + 4, cy - 13)])
    # mischievous eyes + mouth
    pygame.draw.circle(surf, BLACK, (cx - 6, cy - 4), 3)
    pygame.draw.circle(surf, BLACK, (cx + 6, cy - 4), 3)
    pygame.draw.arc(surf, BLACK, (cx - 5, cy + 1, 10, 7), math.pi * 1.1, math.pi * 1.9, 2)
    pygame.draw.ellipse(surf, PINK, (cx - 14, cy + 1, 6, 4))
    pygame.draw.ellipse(surf, PINK, (cx + 8, cy + 1, 6, 4))


def draw_lamb(surf, cx, cy, flip=False):
    d = -1 if flip else 1
    pygame.draw.ellipse(surf, LAMB, (cx - 20, cy - 10, 40, 22))  # wool body
    for wx in (-14, -4, 6, 14):
        pygame.draw.circle(surf, LAMB, (cx + wx, cy - 10), 8)
    pygame.draw.circle(surf, (40, 36, 48), (int(cx + d * 24), int(cy - 6)), 9)  # face
    pygame.draw.ellipse(surf, (40, 36, 48), (cx + d * 24 - 3, cy - 16, 14, 6))  # ear
    pygame.draw.circle(surf, IVORY, (int(cx + d * 27), int(cy - 7)), 2)
    for lx in (-12, 10):
        pygame.draw.rect(surf, (40, 36, 48), (cx + lx - 2, cy + 10, 4, 9))
    # tiny gold bell
    pygame.draw.circle(surf, GOLD, (int(cx + d * 18), int(cy + 4)), 3)


def draw_background(surf, stars, t):
    surf.fill(BG)
    # distant castle + spires
    pygame.draw.rect(surf, BG2, (620, 120, 130, 130))
    for sx, sh in ((632, 190), (676, 230), (716, 175)):
        pygame.draw.rect(surf, BG2, (sx, 250 - sh, 22, sh))
        pygame.draw.polygon(surf, (10, 6, 18), [(sx - 3, 250 - sh), (sx + 25, 250 - sh), (sx + 11, 250 - sh - 26)])
    for wx, wy in ((646, 160), (690, 140), (724, 180), (652, 205)):
        pygame.draw.rect(surf, GOLD, (wx, wy, 6, 9))
    # moon
    pygame.draw.circle(surf, (238, 230, 200), (96, 84), 30)
    pygame.draw.circle(surf, BG, (112, 74), 26)
    # stars
    for (sx, sy, ph) in stars:
        a = 120 + int(100 * math.sin(t * 0.002 + ph))
        pygame.draw.circle(surf, (a, a, a + 30), (sx, sy), 2)
    # ground + faint pentagram
    pygame.draw.rect(surf, (12, 8, 20), (0, 520, WIDTH, 80))
    pygame.draw.ellipse(surf, (40, 26, 58), (250, 528, 300, 52), 2)
    cx, cy, r = 400, 554, 130
    pts = [(cx + r * math.cos(-math.pi / 2 + i * 4 * math.pi / 5), cy + 24 * math.sin(-math.pi / 2 + i * 4 * math.pi / 5)) for i in range(6)]
    pygame.draw.lines(surf, (40, 26, 58), False, pts, 2)
    # tombstones
    for tx, th in ((36, 46), (700, 56), (96, 34), (648, 36)):
        pygame.draw.rect(surf, (44, 38, 58), (tx, 520 - th, 30, th))
        pygame.draw.circle(surf, (44, 38, 58), (tx + 15, 520 - th), 15)


# ---------------------------------------------------------------- entities --
class Bolt:
    def __init__(self, x, y):
        self.x, self.y, self.speed = x, y, 560
        self.rect = pygame.Rect(x - 3, y - 10, 6, 16)

    def update(self, dt):
        self.y -= self.speed * dt
        self.rect.center = (self.x, self.y)


class Enemy:
    def __init__(self, kind, x):
        self.kind = kind
        self.x, self.y = float(x), -30.0
        self.hp = 2 if kind == "skull" else 1
        self.points = {"ghost": 10, "demon": 20, "skull": 30}[kind]
        self.speed = {"ghost": 46, "demon": 74, "skull": 56}[kind] * random.uniform(0.85, 1.2)
        self.phase = random.uniform(0, math.tau)
        self.rect = pygame.Rect(x - 17, -47, 34, 34)

    def update(self, dt, t):
        self.y += self.speed * dt
        self.x += math.sin(t * 0.002 + self.phase) * 22 * dt
        self.rect.center = (self.x, self.y)


class FloatText:
    def __init__(self, x, y, text, color):
        self.x, self.y, self.text, self.color, self.life = x, y, text, color, 1.0

    def update(self, dt):
        self.y -= 34 * dt
        self.life -= dt * 0.9


# ------------------------------------------------------------------- game ---
async def main():
    pygame.init()
    pygame.display.set_caption("Hooves of Hex — Grin Reaper")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    def font(size, bold=False):
        return pygame.font.Font(None, size)

    F_TITLE, F_BIG, F_MED, F_SMALL = font(92), font(40), font(30), font(24)

    stars = [(random.randint(0, WIDTH), random.randint(0, 300), random.uniform(0, 6)) for _ in range(70)]

    state = "title"  # title | play | over
    best = 0

    # per-run state
    def reset():
        return dict(px=WIDTH / 2, score=0, lives=3, bolts=[], enemies=[], floats=[],
                    spawn=0.0, fire_cd=0.0, rapid=0.0, raven=random.choice(RAVEN_IDLE),
                    raven_t=6.0, lamb=None, lamb_t=14.0, unicorn=None, unicorn_t=20.0,
                    rose=None, elapsed=0.0)

    G = reset()
    frame = 0
    shot_saved = False

    if AUTOTEST:
        state = "play"

    running = True
    while running:
        dt = min(clock.tick(FPS) / 1000.0, 0.05)
        t = pygame.time.get_ticks()
        frame += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if state == "title" and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    G = reset(); state = "play"
                elif state == "over" and event.key == pygame.K_r:
                    G = reset(); state = "play"

        keys = pygame.key.get_pressed()

        # ------------------------------------------------------------ play --
        if state == "play":
            G["elapsed"] += dt
            speed = 330
            if AUTOTEST:
                # scripted pilot: chase nearest enemy, fire constantly
                if G["enemies"]:
                    tx = min(G["enemies"], key=lambda e: abs(e.x - G["px"])).x
                    if G["px"] < tx - 6: G["px"] += speed * dt
                    elif G["px"] > tx + 6: G["px"] -= speed * dt
            else:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]: G["px"] -= speed * dt
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]: G["px"] += speed * dt
            G["px"] = max(36, min(WIDTH - 36, G["px"]))

            # firing
            G["fire_cd"] -= dt
            firing = keys[pygame.K_SPACE] or AUTOTEST
            if firing and G["fire_cd"] <= 0:
                G["bolts"].append(Bolt(G["px"], 470))
                G["fire_cd"] = 0.11 if G["rapid"] > 0 else 0.22
            G["rapid"] = max(0.0, G["rapid"] - dt)

            # spawning — pace quickens with score
            G["spawn"] -= dt
            interval = max(0.45, 1.15 - G["score"] / 2500.0)
            if G["spawn"] <= 0:
                roll = random.random()
                kind = "skull" if roll > 0.86 else ("demon" if roll > 0.62 else "ghost")
                G["enemies"].append(Enemy(kind, random.randint(40, WIDTH - 40)))
                G["spawn"] = interval * random.uniform(0.7, 1.3)

            # the lamb crosses — protected species
            G["lamb_t"] -= dt
            if G["lamb"] is None and G["lamb_t"] <= 0:
                d = random.choice((1, -1))
                G["lamb"] = dict(x=-30.0 if d == 1 else WIDTH + 30.0, d=d, y=150.0)
            if G["lamb"]:
                L = G["lamb"]
                L["x"] += L["d"] * 68 * dt
                if L["x"] < -45 or L["x"] > WIDTH + 45:
                    G["score"] += 25
                    G["floats"].append(FloatText(WIDTH / 2, 190, "+25 MERCY", GOLD))
                    G["raven"], G["raven_t"] = RAVEN_LAMB_SAFE, 4.0
                    G["lamb"], G["lamb_t"] = None, random.uniform(16, 26)

            # the unicorn crosses and drops a golden rose (rapid fire)
            G["unicorn_t"] -= dt
            if G["unicorn"] is None and G["unicorn_t"] <= 0:
                d = random.choice((1, -1))
                G["unicorn"] = dict(x=-50.0 if d == 1 else WIDTH + 50.0, d=d, y=88.0, dropped=False)
            if G["unicorn"]:
                U = G["unicorn"]
                U["x"] += U["d"] * 95 * dt
                if not U["dropped"] and 200 < U["x"] < 600:
                    G["rose"] = dict(x=U["x"], y=U["y"] + 16)
                    U["dropped"] = True
                if U["x"] < -70 or U["x"] > WIDTH + 70:
                    G["unicorn"], G["unicorn_t"] = None, random.uniform(22, 32)
            if G["rose"]:
                R = G["rose"]
                R["y"] += 120 * dt
                if abs(R["x"] - G["px"]) < 34 and R["y"] > 452:
                    G["rapid"] = 8.0
                    G["raven"], G["raven_t"] = RAVEN_ROSE, 4.0
                    G["floats"].append(FloatText(G["px"], 430, "RAPID HOOVES!", PINK))
                    G["rose"] = None
                elif R["y"] > 540:
                    G["rose"] = None

            # updates + collisions
            for b in G["bolts"]: b.update(dt)
            for e in G["enemies"]: e.update(dt, t)
            for f in G["floats"]: f.update(dt)
            G["floats"] = [f for f in G["floats"] if f.life > 0]

            dead_bolts, dead_enemies = set(), set()
            for bi, b in enumerate(G["bolts"]):
                if G["lamb"] and abs(b.x - G["lamb"]["x"]) < 24 and abs(b.y - G["lamb"]["y"]) < 20:
                    dead_bolts.add(bi)
                    G["score"] = max(0, G["score"] - 50)
                    G["floats"].append(FloatText(G["lamb"]["x"], 130, "-50 LAMB INCIDENT", DEMON))
                    G["raven"], G["raven_t"] = RAVEN_LAMB_SHOT, 5.0
                    G["lamb"], G["lamb_t"] = None, random.uniform(16, 26)
                    continue
                for ei, e in enumerate(G["enemies"]):
                    if b.rect.colliderect(e.rect):
                        dead_bolts.add(bi)
                        e.hp -= 1
                        if e.hp <= 0:
                            dead_enemies.add(ei)
                            G["score"] += e.points
                            G["floats"].append(FloatText(e.x, e.y, f"+{e.points}", GOLD))
                        break
            G["bolts"] = [b for i, b in enumerate(G["bolts"]) if i not in dead_bolts and b.y > -20]
            G["enemies"] = [e for i, e in enumerate(G["enemies"]) if i not in dead_enemies]

            leaked = [e for e in G["enemies"] if e.y > 505]
            if leaked:
                G["enemies"] = [e for e in G["enemies"] if e.y <= 505]
                G["lives"] -= len(leaked)
                G["raven"], G["raven_t"] = RAVEN_LEAK, 4.0
                if G["lives"] <= 0:
                    best = max(best, G["score"])
                    state = "over"

            # raven idle rotation
            G["raven_t"] -= dt
            if G["raven_t"] <= 0:
                G["raven"] = random.choice(RAVEN_IDLE)
                G["raven_t"] = 6.0

        # ------------------------------------------------------------ draw --
        draw_background(screen, stars, t)

        if state == "title":
            draw_death(screen, 130, 150, 1.15)
            draw_unicorn(screen, 660, 170, 1.1)
            draw_raven(screen, 668, 268, 1.1)
            title = F_TITLE.render("Hooves of Hex", True, IVORY)
            screen.blit(title, title.get_rect(center=(WIDTH / 2, 130)))
            sub = F_MED.render("The black goat has had ENOUGH of the haunting backlog.", True, PINK)
            screen.blit(sub, sub.get_rect(center=(WIDTH / 2, 196)))
            lines = [
                "Blast the descending dead back into the filing system.",
                "Ghosts 10 · Demons 20 · Skulls 30 (they take two hits, the divas)",
                "Do NOT shoot the white lamb. There will be a hearing.",
                "Catch the unicorn's golden rose for RAPID HOOVES.",
                "If three slip past you, the graveyard wins.",
            ]
            for i, ln in enumerate(lines):
                s = F_SMALL.render(ln, True, GREY if i else IVORY)
                screen.blit(s, s.get_rect(center=(WIDTH / 2, 268 + i * 30)))
            draw_goat(screen, WIDTH // 2, 452)
            go = F_BIG.render("Press ENTER to begin the nonsense", True, GOLD)
            if (t // 500) % 2 == 0:
                screen.blit(go, go.get_rect(center=(WIDTH / 2, 540)))
            ctl = F_SMALL.render("Move: ◀ ▶ or A / D · Fire: SPACE", True, GREY)
            screen.blit(ctl, ctl.get_rect(center=(WIDTH / 2, 572)))

        elif state in ("play", "over"):
            # unicorn + lamb + rose
            if G["unicorn"]:
                draw_unicorn(screen, G["unicorn"]["x"], G["unicorn"]["y"], 0.9, flip=G["unicorn"]["d"] < 0)
            if G["rose"]:
                pygame.draw.circle(screen, GOLD, (int(G["rose"]["x"]), int(G["rose"]["y"])), 8)
                pygame.draw.circle(screen, PINK_DEEP, (int(G["rose"]["x"]), int(G["rose"]["y"])), 4)
            if G["lamb"]:
                draw_lamb(screen, G["lamb"]["x"], G["lamb"]["y"] + math.sin(t * 0.006) * 3, flip=G["lamb"]["d"] < 0)
            for e in G["enemies"]:
                draw_ghost(screen, e.x, e.y, e.kind)
            for b in G["bolts"]:
                pygame.draw.rect(screen, GOLD, (b.x - 3, b.y - 10, 6, 16), border_radius=3)
                pygame.draw.circle(screen, IVORY, (int(b.x), int(b.y - 10)), 3)
            draw_goat(screen, int(G["px"]), 486, rapid=G["rapid"] > 0)
            for f in G["floats"]:
                s = F_MED.render(f.text, True, f.color)
                s.set_alpha(int(255 * max(0.0, f.life)))
                screen.blit(s, s.get_rect(center=(f.x, f.y)))
            # HUD
            pygame.draw.rect(screen, (10, 6, 18), (0, 0, WIDTH, 58))
            pygame.draw.line(screen, GOLD, (0, 58), (WIDTH, 58), 2)
            hud = F_MED.render(f"Score {G['score']}    Best {max(best, G['score'])}", True, IVORY)
            screen.blit(hud, (16, 14))
            for i in range(max(0, G["lives"])):
                pygame.draw.circle(screen, PINK_DEEP, (WIDTH - 30 - i * 26, 22), 8)
                pygame.draw.circle(screen, PINK_DEEP, (WIDTH - 38 - i * 26, 22), 8)
                pygame.draw.polygon(screen, PINK_DEEP, [(WIDTH - 46 - i * 26, 24), (WIDTH - 22 - i * 26, 24), (WIDTH - 34 - i * 26, 40)])
            if G["rapid"] > 0:
                rp = F_SMALL.render(f"RAPID HOOVES {G['rapid']:.0f}s", True, GOLD)
                screen.blit(rp, (16, 36))
            # Raven commentary bar
            draw_raven(screen, 34, 584, 0.9)
            rv = F_SMALL.render(f"Raven: “{G['raven']}”", True, (206, 196, 226))
            screen.blit(rv, (58, 572))

            if state == "over":
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((8, 4, 14, 205))
                screen.blit(overlay, (0, 0))
                draw_death(screen, WIDTH // 2, 128, 1.2)
                ov = F_TITLE.render("Filed Under: Dead", True, IVORY)
                screen.blit(ov, ov.get_rect(center=(WIDTH / 2, 268)))
                sc = F_BIG.render(f"Final score {G['score']} · Best {best}", True, GOLD)
                screen.blit(sc, sc.get_rect(center=(WIDTH / 2, 330)))
                q = F_MED.render("Death accepts your paperwork. The goat does not accept defeat.", True, PINK)
                screen.blit(q, q.get_rect(center=(WIDTH / 2, 378)))
                rs = F_BIG.render("Press R to haunt again", True, IVORY)
                if (t // 500) % 2 == 0:
                    screen.blit(rs, rs.get_rect(center=(WIDTH / 2, 448)))

        pygame.display.flip()

        if TITLETEST and frame == 20:
            pygame.image.save(screen, "title.png")
        if TITLETEST and frame >= 30:
            running = False
        if AUTOTEST and not shot_saved and frame > 140 and len(G["enemies"]) >= 2 and G["bolts"]:
            pygame.image.save(screen, "screenshot.png")
            shot_saved = True
        if AUTOTEST and frame == 330 and not shot_saved:
            pygame.image.save(screen, "screenshot.png")
            shot_saved = True
        if AUTOTEST and frame >= 360:
            running = False

        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
