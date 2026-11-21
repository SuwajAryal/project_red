import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import unittest
import pygame as pg
from game import Animation, Playground, STYLES, DT


class PhysicsTests(unittest.TestCase):
    def test_jump_lands_for_every_style(self):
        for style in range(3):
            world = Playground(style)
            world.step(jump=True)
            self.assertLess(world.player.bottom, 157)
            for _ in range(180):
                world.step()
            self.assertEqual(world.player.bottom, 157)
            self.assertTrue(world.grounded)

    def test_no_midair_jump(self):
        a, b = Playground(), Playground()
        a.step(jump=True)
        b.step(jump=True)
        a.step(jump=True)
        b.step()
        self.assertEqual(a.vy, b.vy)

    def test_wall_and_ceiling(self):
        world = Playground()
        world.solids = [pg.FRect(40, 0, 10, 180)]
        for _ in range(10):
            world.step(direction=1)
        self.assertEqual(world.player.right, 40)
        world = Playground()
        world.solids.append(pg.FRect(0, 120, 70, 8))
        world.step(jump=True)
        for _ in range(4):
            world.step()
        self.assertGreaterEqual(world.player.top, 128)

    def test_projectiles_hit_once_and_expire(self):
        world = Playground()
        world.targets = [pg.FRect(60, 140, 10, 15)]
        world.step(shoot=True)
        for _ in range(100):
            world.step()
        self.assertEqual(world.hits, 1)
        self.assertFalse(world.shots)
        world.step(shoot=True)
        world.step(shoot=True)
        self.assertEqual(len(world.shots), 1)
        for _ in range(150):
            world.step()
        self.assertFalse(world.shots)
        self.assertFalse(world.effects)

    def test_each_platform_is_reachable(self):
        # Simulate a jump from each preceding surface at a fixed horizontal input.
        for style in range(3):
            for start, target in [((50, 137), 1), ((113, 104), 2), ((185, 76), 3)]:
                world = Playground(style)
                world.player.topleft = start
                landed = False
                for tick in range(120):
                    direction = 1 if world.player.centerx < world.solids[target].centerx else 0
                    world.step(direction, jump=tick == 0)
                    if world.grounded and world.player.bottom == world.solids[target].top:
                        landed = True
                        break
                self.assertTrue(landed, (style, target))

    def test_exported_animations_load_and_end(self):
        pg.init()
        pg.display.set_mode((320, 180))
        surface = pg.Surface((320, 180), pg.SRCALPHA)
        for style in STYLES:
            animation = Animation(style[-1])
            self.assertGreater(len(animation.frames), 1)
            self.assertGreater(animation.duration, 0)
            animation.draw(surface, (160, 90), .1)
            surface.fill((0, 0, 0, 0))
            animation.draw(surface, (160, 90), animation.duration)
            self.assertEqual(pg.mask.from_surface(surface).count(), 0)
        pg.quit()


if __name__ == '__main__':
    unittest.main()

