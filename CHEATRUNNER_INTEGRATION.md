# PIZZA HEN v1.0 — CheatRunner 0.17 integration

## Runtime architecture

- CheatRunner v0.17 commit `9c75165182bedb9c21e9b58a1468caeb8a3fdb0f` is the integrated backend.
- PIZZA HEN builds `CheatRunner.elf` and embeds it into the daemon output.
- Daemon deploys it to `/data/PIZZA_HEN/payloads/CheatRunner.elf`.
- It is **not** auto-started at boot. The Toolbox Cheats page launches it on demand through the existing `/hbldr` direct-ELF route.
- The Toolbox embeds the upstream dashboard from `http://127.0.0.1:9999/` and, if CheatRunner reports a running game, opens `#trainer=<TITLE_ID>`.
- CheatRunner keeps its upstream runtime/data paths (`/data/cheatrunner/...`) and API.

## Retired legacy path

- The old PIZZA CheatManager cache thread is not started.
- Native legacy Debug Settings cheat links are retired.
- Controller cheat shortcuts, when configured, open the Toolbox CheatRunner page directly.
- Existing old cheat files are not deleted automatically.

## Source archive build note

The supplied v0.17 source archive references helper scripts that were absent from that archive. PIZZA HEN carries deterministic build-time adapters for the gzip asset headers and embedded hotkey-payload byte header expected by CheatRunner's own CMake. Runtime CheatRunner sources are not rewritten by those adapters.
