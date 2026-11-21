# Taste samples / 2026-11-21

## GitHub exploration

- [PixelFX](https://github.com/patch-gg/pixelfx): effect source, export tooling, and license reviewed. Its [live gallery](https://patch-gg.github.io/pixelfx/) is a useful place to choose more effects. We use exported PNG/JSON animations in Python.
- [pygame-ce](https://github.com/pygame-community/pygame-ce): the Python multimedia foundation, with an examples directory for further learning. The project uses its drawing, input, timing, rectangle, font, and image APIs.

The design choice is to compare three small variations of the same room. Foundry has 90 px/s movement and 720 px/s² gravity; Neon Relay has 130 and 760; Moonbase has 95 and 400. A fixed 60 Hz simulation keeps these comparisons consistent across rendering speeds. Start a jump a little before a platform so the hero clears its edge.

## What to compare

1. Is Foundry's jump satisfying or too heavy?
2. Is Neon Relay's speed fun or difficult to control?
3. Does Moonbase's longer airtime help aiming or slow the game down?
4. Which palette and impact animation should we keep?

All three use original geometric scenery, a placeholder robot, stationary targets, and the same platform arrangement. No Mega Man assets or tutorial game code are included. These are taste samples rather than completed roadmap milestones for combat or level progression.

## Asset provenance and reproduction

PixelFX source commit: `5294518ce7c72e48b6100a744596e0acf57f2826`.

Exported effects: `impacts/bullet-impact`, `impacts/hit-spark`, and `impacts/shield-block`. Assets retain their default palettes and original frame sizes, durations, and pivots. Seed: 7. Actor rendering disabled. No exported images were edited.

From the project root, with that checkout at `.cache/pixelfx` and Node 18+:

```sh
node .cache/pixelfx/tools/render.mjs impacts/bullet-impact impacts/hit-spark impacts/shield-block --sheet --no-actor --seed 7 --out assets/effects
```

The exporter writes a contact sheet plus a transparent sprite sheet and JSON per effect. The game uses the sprite sheet and JSON; contact sheets are included for inspection. Node is only needed to regenerate assets.

PixelFX copyright and attribution are preserved in [the MIT license](licenses/PixelFX-LICENSE.txt) and [upstream notices](licenses/PixelFX-NOTICE.md). The gallery's separate font is not included. The game uses pygame's bundled default font.

## Validation

Six automated checks cover all three jump profiles, no airborne re-jump, wall/ceiling collision, reachable platforms, projectile hits/cooldowns/cleanup, and exported animation loading/end times. Preview renders provide a separate visual check. Keyboard play feel remains for us to judge together.
