# PIZZA HEN v1.0 — CheatRunner 0.17 integration

## Runtime architecture

- CheatRunner v0.17 commit `9c75165182bedb9c21e9b58a1468caeb8a3fdb0f` is vendored under `Source Code/third_party/CheatRunner-0.17`.
- PIZZA HEN builds `CheatRunner.elf` from that source and embeds it into the daemon output.
- Daemon deploys it to `/data/PIZZA_HEN/payloads/CheatRunner.elf`.
- It is **not** auto-started at boot. The Toolbox Cheats page launches it on demand through the existing `/hbldr` direct-ELF route.
- The Toolbox embeds the upstream dashboard from `http://127.0.0.1:9999/` and, if CheatRunner reports a running game, opens `#trainer=<TITLE_ID>`.
- CheatRunner keeps its upstream runtime/data paths (`/data/cheatrunner/...`) and API.

## Retired legacy path

- PIZZA HEN no longer replaces the game's `MENU_ID_CHECK_PATCH` with `★ PIZZA HEN Cheats`.
- `etaHEN?Cheats` / `etaHEN?Cheats_not_open` handlers are removed.
- Native `id_cheats` Debug Settings link is removed.
- Old PIZZA CheatManager cache thread is not started.
- Controller cheat shortcuts, if configured, open the Toolbox CheatRunner page directly.
- Existing old cheat files are not deleted automatically.

## Source archive build note

The supplied v0.17 source archive references two CMake helper scripts that are absent from that archive. PIZZA HEN adds deterministic build-time adapters under `third_party/CheatRunner-0.17/tools/`; they only generate the gzip asset headers and embedded hotkey-payload byte header expected by CheatRunner's own CMake. Runtime CheatRunner sources are not rewritten.
