# HTML5 Game Integrator

Portable Windows helper for preparing lightweight HTML5 game bundles.

## Current workflow

The tool can now optionally accept a host JavaScript file and package it together with the game while preserving that host file byte-for-byte.

- Select an optional host `.js` file.
- Select a game folder, ZIP, or `index.html`.
- The host JavaScript is copied unchanged.
- SHA-256 is checked before and after the copy.
- The game receives the lightweight runtime layer.
- Default frame cap: 20 FPS.
- Optional Gamepad API mapping.
- Optional fullscreen-friendly styling.
- Optional countdown timer, default 50 minutes.
- A separate generic `mmi_game_addon.js` module is included in the bundle.
- A manifest records the host file hash and confirms `hostModified=false`.
- The source files are never overwritten.

## Output structure

A typical bundle contains:

- `host/<original-name>.js` — unchanged copy of the selected host script.
- `game/` — prepared HTML5 game.
- `addon/mmi_game_addon.js` — separate UI/game overlay module.
- `MM_BUNDLE.json` — build metadata and host SHA-256.
- `HOST_SCRIPT_UNCHANGED.txt` — integrity note.

## Use

1. Double-click `Launch.bat`.
2. Optionally select a host JavaScript file.
3. Select the HTML5 game.
4. Choose the output ZIP.
5. Keep 20 FPS or choose another value.
6. Keep the 50 minute timer or change/disable it.
7. Press **BUILD HOST + GAME BUNDLE**.

## Controller mapping

Default standard mapping:

- D-pad / left stick: arrow keys
- South face button (Cross/A): Enter
- Start/Options: Space

## Scope

The host script is intentionally not rewritten or patched. The game remains a separate UI module in the same bundle. This utility does not alter exploit, jailbreak, kernel, or security-bypass logic.

Only package games/assets you have permission to redistribute.
