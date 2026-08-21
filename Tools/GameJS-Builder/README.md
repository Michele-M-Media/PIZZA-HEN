# GameJS Builder

Portable Windows helper that converts a **self-contained HTML5 game** into one standalone `game.js` overlay.

## What it generates

The output `game.js` embeds the selected HTML game and exposes a generic browser API:

- `MMGame.start()`
- `MMGame.stop()`
- `MMGame.show()`
- `MMGame.hide()`
- `MMGame.isRunning()`

Optional/default runtime features:

- 20 FPS target cap
- Gamepad API mapping
- fullscreen overlay
- 50 minute visible countdown timer
- auto-start when `game.js` is loaded

Default controller mapping:

- D-pad / left stick -> Arrow keys
- Cross/A -> Enter
- Options/Start -> Space

## Use

1. Double-click `Launch.bat`.
2. Select a self-contained `.html` game.
3. Choose the output path for `game.js`.
4. Keep the default 20 FPS / controller / fullscreen / 50 minute timer settings or change them.
5. Press **BUILD GAME.JS**.

The source HTML is never overwritten.

## Important limitation

This builder is intentionally **host-independent**. It does not inspect, patch, rewrite, or infer insertion points inside any exploit/jailbreak script, including `p2jb.js`.

It only prepares the game-side JavaScript so it can be tested as a normal browser script. Whether another script can run at the same time depends on the browser/event-loop behavior of that environment.

## Input note

For reliable single-file output, use an HTML game that is already self-contained (no external images, audio, CSS, or JavaScript files). The standalone Pac-Man-style test game from this repository is suitable for this workflow if exported as one self-contained HTML file.
