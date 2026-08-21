# HTML5 Game Integrator

Portable Windows helper for preparing lightweight HTML5 games as self-contained ZIP packages.

## What it does

- Select a game folder or ZIP.
- Finds the game's `index.html`.
- Adds a lightweight runtime layer.
- Optional FPS cap (default: 20 FPS).
- Optional Gamepad API mapping for common controllers.
- Optional fullscreen-friendly styling.
- Optional countdown timer overlay (enabled by default at 50 minutes).
- Timer duration is configurable from 1 to 180 minutes.
- Creates a new ZIP; the source is never overwritten.

## Use

1. Double-click `Launch.bat`.
2. Select the game folder or ZIP.
3. Choose the output ZIP.
4. Keep 20 FPS or choose another value.
5. Leave the countdown enabled for the default 50 minutes, or choose another duration.
6. Press **BUILD GAME PACKAGE**.

## Controller mapping

Default standard mapping:

- D-pad / left stick: arrow keys
- South face button (Cross/A): Enter
- Start/Options: Space

This keeps compatibility with many keyboard-driven HTML5 games.

## Countdown timer

When enabled, the generated game package shows a small countdown in the top-right corner. The default is 50:00. When it reaches zero it remains at 00:00 and changes color; it does not forcibly stop or close the game.

## Scope

This utility is intentionally a generic web-game packager. It does not alter exploit, jailbreak, kernel, or security-bypass logic. It prepares the game/UI portion only.

## Notes

Game compatibility varies. Games that hard-code physics directly to frame count may not behave correctly with a frame cap. For those, use their original timing or a more suitable FPS value.

Only package games/assets you have permission to redistribute.