"""Three tiny platformer taste samples. Run with: python game.py."""
import argparse
import json
import math
from pathlib import Path

import pygame as pg

ROOT = Path(__file__).resolve().parent
WIDTH, HEIGHT = 320, 180
DT = 1 / 60
# name, subtitle, background, accent, speed, jump velocity, gravity, effect
STYLES = [
    ('FOUNDRY', 'HEAVY STEEL / PRECISE JUMPS', '#171c2b', '#ffad66', 90, -235, 720, 'bullet-impact'),
    ('NEON RELAY', 'QUICK FEET / ELECTRIC NIGHTS', '#10172d', '#52efd3', 130, -245, 760, 'hit-spark'),
    ('MOONBASE', 'LOW GRAVITY / LONG AIRTIME', '#16182e', '#b8a0ff', 95, -185, 400, 'shield-block'),
]


class Animation:
    def __init__(self, name):
        folder = ROOT / 'assets' / 'effects' / 'impacts' / name
        data = json.loads((folder / f'{name}.json').read_text())
        sheet = pg.image.load(folder / f'{name}.png').convert_alpha()
        self.frames, self.ends = [], []
        total = 0
        for item in data['frames']:
            r = item['frame']
            self.frames.append(sheet.subsurface((r['x'], r['y'], r['w'], r['h'])))
            total += item['duration'] / 1000
            self.ends.append(total)
        self.duration = total
        self.pivot = data['meta']['pixelfx']['pivot']

    def draw(self, surface, position, age):
        for frame, end in zip(self.frames, self.ends):
            if age < end:
                surface.blit(frame, (position[0] - self.pivot[0], position[1] - self.pivot[1]))
                break


class Playground:
    def __init__(self, style=0):
        self.style = style
        self.solids = [pg.FRect(0, 157, 320, 23), pg.FRect(86, 124, 42, 8),
                       pg.FRect(155, 96, 44, 8), pg.FRect(237, 120, 51, 8)]
        self.player = pg.FRect(24, 137, 12, 20)
        self.vy = 0
        self.grounded = True
        self.facing = 1
        self.cooldown = 0
        self.shots = []
        self.effects = []
        self.targets = [pg.FRect(110, 110, 10, 14), pg.FRect(180, 82, 10, 14), pg.FRect(267, 106, 10, 14)]
        self.hits = 0
        self.time = 0

    def step(self, direction=0, jump=False, shoot=False):
        _, _, _, _, speed, impulse, gravity, _ = STYLES[self.style]
        self.time += DT
        self.cooldown = max(0, self.cooldown - DT)
        if direction:
            self.facing = direction
        self.player.x += direction * speed * DT
        for solid in self.solids:
            if self.player.colliderect(solid):
                if direction > 0:
                    self.player.right = solid.left
                elif direction < 0:
                    self.player.left = solid.right
        self.player.x = max(0, min(WIDTH - self.player.w, self.player.x))
        if jump and self.grounded:
            self.vy = impulse
        self.vy += gravity * DT
        self.player.y += self.vy * DT
        self.grounded = False
        for solid in self.solids:
            if self.player.colliderect(solid):
                if self.vy > 0:
                    self.player.bottom = solid.top
                    self.grounded = True
                else:
                    self.player.top = solid.bottom
                self.vy = 0
        if shoot and self.cooldown == 0:
            x = self.player.right if self.facing > 0 else self.player.left - 6
            self.shots.append([pg.FRect(x, self.player.y + 8, 6, 3), self.facing])
            self.cooldown = .18
        for shot in self.shots[:]:
            rect, facing = shot
            rect.x += facing * 230 * DT
            target = next((t for t in self.targets if rect.colliderect(t)), None)
            wall = any(rect.colliderect(s) for s in self.solids)
            if target is not None or wall or rect.right < 0 or rect.left > WIDTH:
                self.shots.remove(shot)
                if target is not None:
                    self.targets.remove(target)
                    self.hits += 1
                if target is not None or wall:
                    self.effects.append([rect.center, 0])
        for effect in self.effects:
            effect[1] += DT
        self.effects = [fx for fx in self.effects if fx[1] < 2]


def text(surface, font, message, xy, color='#dce4f3'):
    surface.blit(font.render(message, False, color), xy)


def draw(surface, world, animation, font, small, paused=False):
    name, subtitle, bg, accent, *_ = STYLES[world.style]
    surface.fill(bg)
    # Original geometric pixel artwork; no character or scenery assets copied.
    for i in range(22):
        x, y = (i * 73 + 17) % WIDTH, (i * 37 + 11) % 110 + 24
        pg.draw.rect(surface, '#44506a', (x, y, 1, 1))
    if world.style == 2:
        pg.draw.circle(surface, '#393556', (254, 59), 27)
        pg.draw.circle(surface, '#4b4269', (246, 52), 8)
        pg.draw.circle(surface, '#292a46', (263, 67), 6)
    for i in range(9):
        x, h = i * 41 - 13, 24 + (i * 19) % 43
        pg.draw.rect(surface, '#242c43', (x, 157 - h, 28, h))
        for y in range(162 - h, 150, 10):
            pg.draw.rect(surface, '#3a4861', (x + 6, y, 4, 2))
    for solid in world.solids:
        pg.draw.rect(surface, '#39445a', solid)
        pg.draw.rect(surface, accent, (solid.x, solid.y, solid.w, 2))
        for x in range(int(solid.x) + 5, int(solid.right), 12):
            pg.draw.line(surface, '#20283c', (x, solid.y + 4), (x + 4, solid.bottom - 1))
    for target in world.targets:
        pg.draw.rect(surface, '#26324b', target.inflate(4, 2))
        pg.draw.rect(surface, accent, target, 1)
        pg.draw.rect(surface, '#fff1d6', (target.x + 3, target.y + 4, 4, 3))
    p = world.player
    bob = int(math.sin(world.time * 14)) if world.grounded else 0
    pg.draw.rect(surface, '#0a0f1c', (p.x - 2, p.y - 1, 16, 22))
    pg.draw.rect(surface, accent, (p.x, p.y, 12, 8))
    pg.draw.rect(surface, '#e0fcff', (p.x + (6 if world.facing > 0 else 1), p.y + 2, 5, 3))
    pg.draw.rect(surface, '#7289ac', (p.x + 2, p.y + 9, 8, 7))
    pg.draw.rect(surface, accent, (p.x, p.y + 16 + bob, 5, 4))
    pg.draw.rect(surface, accent, (p.x + 7, p.y + 16 - bob, 5, 4))
    pg.draw.rect(surface, '#e0fcff', (p.x + (9 if world.facing > 0 else -3), p.y + 9, 6, 4))
    for shot, _ in world.shots:
        pg.draw.rect(surface, accent, shot.inflate(2, 2))
        pg.draw.rect(surface, '#ffffff', shot)
    for pos, age in world.effects:
        animation.draw(surface, pos, age)
    pg.draw.rect(surface, '#101523', (0, 0, 320, 28))
    text(surface, font, f'0{world.style + 1} / {name}', (8, 4), accent)
    text(surface, small, subtitle, (8, 17), '#8c9bb5')
    text(surface, small, f'TARGETS {world.hits}/3', (250, 8))
    pg.draw.rect(surface, '#101523', (0, 169, 320, 11))
    text(surface, small, '1-3 STYLE  A/D MOVE  SPACE JUMP  J FIRE  R RESET', (7, 171))
    if paused or world.hits == 3:
        pg.draw.rect(surface, '#101523', (57, 48, 206, 27))
        text(surface, font, 'PAUSED' if paused else 'ALL CLEAR / R TO REPLAY', (70, 57), accent)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sample', type=int, choices=(1, 2, 3), default=1)
    parser.add_argument('--screenshots', type=Path, help='Render all sample previews and exit')
    args = parser.parse_args()
    pg.init()
    screen = pg.display.set_mode((960, 540))
    pg.display.set_caption('Project Red | Taste Samples')
    canvas = pg.Surface((WIDTH, HEIGHT))
    font, small = pg.font.Font(None, 14), pg.font.Font(None, 12)
    animations = [Animation(style[-1]) for style in STYLES]
    if args.screenshots:
        args.screenshots.mkdir(parents=True, exist_ok=True)
        for i in range(3):
            world = Playground(i)
            world.effects = [[(250, 94), .1]]
            draw(canvas, world, animations[i], font, small)
            pg.image.save(pg.transform.scale(canvas, (960, 540)), args.screenshots / f'sample-{i + 1}.png')
        pg.quit()
        return
    world, clock = Playground(args.sample - 1), pg.time.Clock()
    running, paused, jump_pending, accumulator = True, False, False, 0
    while running:
        elapsed = min(clock.tick(120) / 1000, .1)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key in (pg.K_1, pg.K_2, pg.K_3, pg.K_r):
                    style = event.key - pg.K_1 if event.key != pg.K_r else world.style
                    world, paused, accumulator, jump_pending = Playground(style), False, 0, False
                elif event.key == pg.K_ESCAPE:
                    paused = not paused
                    accumulator, jump_pending = 0, False
                elif event.key == pg.K_SPACE and not paused:
                    jump_pending = True
        keys = pg.key.get_pressed()
        if not paused:
            accumulator += elapsed
            while accumulator >= DT:
                direction = int(keys[pg.K_d] or keys[pg.K_RIGHT]) - int(keys[pg.K_a] or keys[pg.K_LEFT])
                world.step(direction, jump_pending, keys[pg.K_j])
                jump_pending = False
                accumulator -= DT
        draw(canvas, world, animations[world.style], font, small, paused)
        pg.transform.scale(canvas, screen.get_size(), screen)
        pg.display.flip()
    pg.quit()


if __name__ == '__main__':
    main()
