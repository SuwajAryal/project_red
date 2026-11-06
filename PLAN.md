# Project Red — starting plan

## Goal
Build a small, original 2D action-platformer in Python, inspired by the running, jumping, and shooting we loved in Mega Man. This is a fun learning project: make something playable early, understand each feature, and improve it together.

**Current stage:** planning only. No playable game or dependencies installed yet.

## First playable version
One short industrial training level with a robot hero, platforms, a basic blaster, one enemy type, health, restart, and an exit. Aim for a few minutes of play.
Use original characters, names, level layouts, and artwork.

Proposed controls: A/D or arrows to move, Space to jump, J to shoot, R to restart, Escape to pause.
Start with colored rectangles so movement can be tuned before artwork.

## Technical direction
- Python 3.12+ and pygame-ce (imported as pygame), with a local virtual environment.
- Windows first; keep paths portable.
- A 320 × 180 logical canvas, scaled by whole numbers for crisp pixels.
- Target 60 updates per second; separate input, simulation, and rendering.
- Simple rectangle collisions and a small tile grid; add abstractions only when needed.
- PNG sprite sheets and JSON animation metadata for effects.
- Pin tested dependency versions when the runnable prototype is added.

Reference: [pygame-ce documentation](https://pyga.me/docs/).

## Milestones and learning goals

### 1. A window and a moving hero
- [ ] Set up Python environment and dependency file.
- [ ] Open a window, draw a floor and hero, and handle quitting.
- [ ] Walk left/right, jump, fall, and land without passing through the floor.
- [ ] Keep movement consistent and prevent jumping again while airborne.
Learn: variables, functions, input events, the game loop, velocity, and collision.
Done when: the hero can move and jump repeatedly and the window closes cleanly.

### 2. A tiny platforming playground
- [ ] Add walls, several platforms, and a fall/reset zone.
- [ ] Separate horizontal and vertical collision handling.
- [ ] Tune acceleration, jump height, and optional short jump buffering.
Learn: coordinates, rectangles, lists, and separating responsibilities.
Done when: a short route is traversable without clipping or getting stuck.

### 3. Shooting and danger
- [ ] Fire in the facing direction with a short cooldown.
- [ ] Add one patrolling enemy, projectile hits, and health.
- [ ] Add brief invulnerability after damage, death, and restart.
- [ ] Remove expired/off-screen projectiles.
Learn: objects, timers, state machines, and collection management.
Done when: enemies can be defeated and the player can lose and restart.

### 4. A complete small level
- [ ] Build a short scrolling level with a checkpoint and exit.
- [ ] Add health display, pause, and a victory screen.
- [ ] Make restarting restore all gameplay state.
Learn: cameras, level data, UI, and game states.
Done when: a complete start-to-finish playthrough works.

### 5. PixelFX and visual personality
- [ ] Export and test one impact effect before importing more.
- [ ] Add shot impacts, enemy explosions, and a respawn effect.
- [ ] Add original hero/enemy sprites and simple tiles.
- [ ] Add sound with documented sources; tune visual feedback.
Learn: animation frames, elapsed time, pivots, transparency, and asset attribution.
Done when: effects align with hits and animations play at their intended speed.

### 6. Share a first demo
- [ ] Document setup and controls, add a screenshot, and make a tagged release.
- [ ] Test a clean install and a full playthrough.
- [ ] Package a Windows build if useful after source-based play works.

## PixelFX workflow
Source: [patch-gg/pixelfx](https://github.com/patch-gg/pixelfx).

PixelFX's runtime is JavaScript. For this Python game, use its exported transparent PNG sprite sheets and Aseprite-style JSON, rather than trying to import JavaScript into Python. Its documented export example is:

```sh
node tools/render.mjs ice/frost-nova --sheet
```

Run this inside a separately prepared PixelFX checkout during the graphics milestone. Node is an asset-authoring tool; players should only need the Python game and exported assets.

The Python animation loader should read frame rectangles and durations and account for pivot placement, looping, and facing direction. Test transparency and color appearance in-game. PixelFX mainly supplies effects; it does not replace our hero, tiles, or level design.

Before copying assets or adapted code, record the upstream commit, effect names, export options, and any edits. Review and preserve the applicable LICENSE and NOTICE.md in third-party credits. No upstream assets are included at the planning stage.

## Proposed layout (create as needed)
```text
README.md
PLAN.md
requirements.txt
src/project_red/
    __main__.py
    game.py
    player.py
    level.py
    enemies.py
    effects.py
assets/
    sprites/
    effects/
    tiles/
    sounds/
docs/
    learning-log.md
    third-party-credits.md
tests/
```

Start small; split files when their responsibilities become clear.

## How we will work
1. Pick one small feature.
2. Explain the idea and implement the smallest useful version.
3. Play it and adjust the feel together.
4. Record what we learned and commit the working step.

Use focused automated tests for collision, damage/cooldowns, and animation timing once those systems exist. Manually check movement, jumping under ceilings, wall collisions, pause/resume, repeated restart, and level completion.

## Later ideas
A boss, dash, charge shot, controller support, extra levels, and weapon upgrades can follow the first complete level. Multiplayer, a level editor, and procedural worlds are outside the first demo.

## Next session
Implement milestone 1: open a window and make a placeholder hero run and jump.

