# CheatRunner 🎮

[![Latest release](https://img.shields.io/github/v/release/notmaj0r/CheatRunner?label=Release&logo=github&color=blue)](https://github.com/notmaj0r/CheatRunner/releases/latest)
[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Join our Discord Server](https://img.shields.io/badge/Discord-Join%20our%20Server-5865F2?logo=discord&logoColor=white)](https://discord.gg/E4g6fEqp46)

**CheatRunner** is a PS5 web-based cheat trainer for **already-jailbroken PS5 consoles**.

It provides a local web dashboard to:

- list installed games and apps;
- launch installed titles from a browser;
- load local cheat files from the PS5 filesystem;
- use `.mc4`, `.shn`, and `.json` trainers;
- apply local XML patches manually from the dashboard;
- optionally download cheat files from configured cheat sources;
- enable/disable supported cheats from your browser;
- inspect logs, diagnostics, and cheat debug information.

---

## ❤️ Support

CheatRunner is free and open-source. If you find it useful, feel free to support the project.

<a href="https://ko-fi.com/maj0r"><img src="https://storage.ko-fi.com/cdn/kofi3.png?v=3" alt="Support me on Ko-fi" height="36"></a>
<a href="https://buymeacoffee.com/maj0r"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy me a coffee" height="36"></a>


---

## ⚠️ Disclaimer

CheatRunner is **not a jailbreak**, **not an exploit**, and **not a tool for stock/retail consoles**.

It only works when your PS5 is already jailbroken and already has the required homebrew/payload environment running.

CheatRunner does **not** provide:

- jailbreaks or kernel exploits;
- game backups or game content;
- piracy features;
- PSN bypasses;
- online services.

It is a local homebrew tool for testing trainers on your own already-jailbroken console.

Use it at your own risk.

Runtime cheat memory writes can crash the game, break a session, corrupt your savegame, softlock the title, or behave differently depending on the game version/update.

**Always back up your save files before using any cheats.**

---

## ✨ Features

- PS5 web dashboard.
- Installed games/apps list.
- PS5 / PS4 / Apps filters.
- Favorites and Recent tabs — star games to pin them; recently launched/opened titles are tracked automatically. Synced console-side, so they're identical on every device that opens the dashboard.
- First-run onboarding with a quick system check and one-click setup profiles.
- App title names from `app.db` when SQLite support is enabled.
- Launch installed games/apps from the browser.
- Local cheat loading from `/data/cheatrunner/cheats`.
- `.mc4`, `.shn`, and `.json` cheat/trainer support.
- Manual local PS-Game-Patch XML listing and application are supported.
- Version-aware patch selection — matches `AppVer` fields; mask-version patches apply regardless of game version.
- Optional remote cheat downloads from configured cheat sources.
- ON/OFF trainer toggles where supported.
- Runtime restore where possible.
- Crash-suspect detection — mods that crash the game are flagged and blocked from re-enabling automatically; suspects persist across CheatRunner restarts.
- Autoload profiles — save your currently-enabled cheats and/or currently-applied patches for a game, and CheatRunner re-applies them automatically the next time that game launches, with an on-screen notification.
- Version-aware cheat selection with candidate selector and manual override.
- Per-title address mode override (Auto / Absolute / Relative) for SHN and MC4 files.
- Address learning cache — resolved SHN/MC4 addresses reused on subsequent applies.
- Settings panel — address resolution, safety timers, log level, and advanced toggles, all configurable from the dashboard, with one-click presets (Safe / Max Compatibility / Debug), live search, reset-to-defaults, and a dark theme picker.
- Config hot-reload — edits to `config.ini` on the PS5 (FTP/SSH) are picked up automatically within ~500 ms, no restart required.
- Controller hotkey — hold two buttons (L2 + R3 by default, configurable) to open the dashboard from the XMB, or jump straight to the running game's trainer. Off by default; enable it from Settings once you've confirmed it's stable on your firmware.
- Logs panel with a Copy Logs button.
- Shutdown Payload button for testing and cleanup.

---

## 🔄 Updating CheatRunner

**Before updating to a new CheatRunner version, please follow these steps:**

1. Go to `/data/cheatrunner` and delete **everything** except the `cheats` and `patches` folders.
   - Keep both folders — there is **no need** to delete them.
   - Do this **before** using the new CheatRunner version, **not after**.
2. Delete the old **CheatRunner PKG** (home-screen tile) from your PS5.
3. Clear your browser cache: **Settings → System → Browser → Clear Cache**.

---

## 🚀 Running

### Payload loader (direct ELF)

Send `CheatRunner.elf` to your already-jailbroken PS5 using your preferred payload loader.

Then open the dashboard in your browser:

```text
http://<PS5-IP>:9999
```

Example:

```text
http://192.168.1.100:9999
```

### Homebrew Launcher

CheatRunner ships as a Homebrew Launcher-compatible package (`CheatRunner.zip`).

1. Transfer `CheatRunner.zip` to your PC.
2. Extract the zip **directly into `/data/homebrew/`** on your PS5 via FTP.
   The result must be:

   ```text
   /data/homebrew/CheatRunner/
   ├── CheatRunner.elf
   ├── homebrew.js
   └── sce_sys/
       └── icon0.png
   ```

3. Open the Homebrew Launcher on your PS5. **CheatRunner** will appear as an app.
4. Launch it, then open the dashboard in your browser:

   ```text
   http://<PS5-IP>:9999
   ```

---

## 🧪 Notes

CheatRunner is still experimental.

Some cheats may:

- work correctly;
- fail to apply;
- mismatch the game version;
- crash the game;
- require a specific game update;
- behave differently after relaunching the game.

When reporting bugs, include:

- CheatRunner logs (Copy Logs button);
- game title ID;
- game version/update;
- cheat file used;
- which cheat was enabled/disabled;
- what happened before the issue.

---

## 📁 Local Cheats

CheatRunner is local-first. Local cheat files remain the primary workflow.

### Search paths (scanned in order)

```text
/data/cheatrunner/cheats   ← primary path
/data/etaHEN/cheats        ← etaHEN cross-compatibility
/data/elf-arsenal/cheats   ← elf-arsenal cross-compatibility
```

Recommended sub-folders inside the primary path:

```text
/data/cheatrunner/cheats/mc4
/data/cheatrunner/cheats/shn
/data/cheatrunner/cheats/json
```

Example files:

```text
/data/cheatrunner/cheats/mc4/PPSA30803_01.200.000.mc4
/data/cheatrunner/cheats/mc4/PPSA30803.mc4
/data/cheatrunner/cheats/shn/CUSA00000.shn
/data/cheatrunner/cheats/json/CUSA00000.json
```

### Version-aware selection

CheatRunner matches cheat files by title ID and game version:

- **Exact match** (`CUSA00000_01.09.json`) — selected automatically when the running game reports that version.
- **Generic** (`CUSA00000.json`, no version in filename) — used as fallback when no exact match exists.
- **Wrong version** — loaded as a last resort when no exact or generic file exists; the cheat menu shows a version-mismatch warning banner and a `WRONG VER` badge. The candidate selector lets you force-switch or download a better match.

### Per-title address mode

For SHN and MC4 cheat files an **Address Mode** selector appears above the mod list: `Auto` (default), `Absolute`, or `Relative`. Use this to override address resolution for a specific game if cheats land at the wrong address. The preference is saved per title ID.

### Address learning cache

Resolved SHN/MC4 addresses are cached to `/data/cheatrunner/addr_cache.json`. On the second apply of the same cheat file, the cached address is used directly — no re-probing needed. The cache is invalidated automatically when the cheat file changes on disk.

---

## 📁 Local Patches

CheatRunner supports **PS-Game-Patch** XML patches.

Patch search paths (scanned in this order):

```text
/data/cheatrunner/patches/xml_prospero   ← PS5-native patches
/data/cheatrunner/patches/xml            ← PS4 BC / general patches
/data/elf-arsenal/patches/xml            ← elf-arsenal cross-compatibility
```

---

## 🔁 Autoload Profiles

Autoload profiles let CheatRunner automatically re-apply your cheats and/or patches every time you launch a game — no need to open the dashboard and toggle them on again.

**Important:** an autoload profile only saves the cheats/patches that are **currently ON/applied at the moment you save it**. It does not save the whole cheat or patch file — only the specific mods you had turned on, or the specific patches you had applied, at that time.

### Setting up autoload for cheats

1. Open a game's trainer from the dashboard and enable the cheats you want.
2. Go to the **Cheats** tab and click **Save Autoload Profile**.
3. Next time you launch that game, CheatRunner automatically re-applies those same cheats and shows an on-screen notification.
4. To stop autoloading, open the Cheats tab again and click **Clear Autoload Profile**.

### Setting up autoload for patches

1. Open a game's trainer from the dashboard and apply the patches you want.
2. Go to the **Patches** tab and click **Save Autoload Profile**.
3. Next time you launch that game, CheatRunner automatically re-applies those same patches and shows an on-screen notification.
4. To stop autoloading, open the Patches tab again and click **Clear Autoload Profile**.

Cheat and patch autoload profiles are independent — you can save one, both, or neither for any given game.

---

## 🎮 Controller Hotkey

Hold two controller buttons together to open CheatRunner.

- From the **XMB**, it opens the dashboard's main page.
- **In-game**, it jumps straight to that game's trainer instead of the main page.

Default combo is **L2 + R3**, held for 800ms. Both buttons and the hold duration are configurable from **Settings → Hotkey**.

### Enabling the hotkey

The hotkey is **off by default** — it hooks into SceShellUI, and on some PS5 firmwares (seen on 4.xx) that hook can crash the XMB. Turn it on from **Settings → Hotkey → Enable hotkey** once you've confirmed it's stable on your firmware. The rest of CheatRunner works fully without it; you'd just open the dashboard from a browser bookmark instead of L2+R3.

---

## 🛠️ Building

CheatRunner is built with `ps5-payload-sdk`.

Recommended project layout:

```text
CheatRunner/
├── CheatRunnerPayload/
│   ├── src/
│   ├── CMakeLists.txt
│   └── build-cheatrunner.ps1
└── PS5-Payload-dev/
    └── sdk-master/
```

The build script searches for the SDK in this order:

```text
1. PS5_PAYLOAD_SDK environment variable
2. ../PS5-Payload-dev/sdk-master
3. ../ps5-payload-sdk
```

Build on Windows:

```powershell
cd CheatRunnerPayload
.\build-cheatrunner.ps1 -Clean -Sqlite
```

SQLite note:

- If `src/third_party/sqlite3.c` and `src/third_party/sqlite3.h` exist, bundled SQLite can be enabled.
- Use `-Sqlite` to force-enable SQLite support.
- Use `-NoSqlite` to disable SQLite explicitly.

Output:

```text
build/CheatRunner.elf
```

---

## 🤝 Credits

CheatRunner exists thanks to the PS4/PS5 homebrew and research community.

Special thanks to:

- **[ELF Arsenal](https://git.etawen.dev/soniciso/elf-arsenal) & VoidShell** for project ideas and implementations;
- **[ps5-payload-dev](https://github.com/ps5-payload-dev)**: [sdk](https://github.com/ps5-payload-dev/sdk), [elfldr](https://github.com/ps5-payload-dev/elfldr), [websrv](https://github.com/ps5-payload-dev/websrv), [pacbrew-repo](https://github.com/ps5-payload-dev/pacbrew-repo);
- **TeeKay87** for the [HEN-Cheats-Collection](https://github.com/TeeKay87/HEN-Cheats-Collection) project;
- **etaHEN** for the [PS5_Cheats](https://github.com/etaHEN/PS5_Cheats) project;
- **[etaHEN](https://github.com/etaHEN/etaHEN)** — the SceShellUI injection/hooking approach is adapted from it;
- **GoldHEN** for the [GoldHEN_Cheat_Repository](https://github.com/GoldHEN/GoldHEN_Cheat_Repository) project;
- **RDX-Sci01** for the [HEN-PPSA-Cheats](https://github.com/RDX-Sci01/HEN-PPSA-Cheats) project;
- **illusionyy** for the [PS-Game-Patch](https://github.com/illusionyy/ps-game-patch) and the [ps-patch-system](https://github.com/illusionyy/ps-patch-system) projects;
- everyone testing, reporting logs, and helping improve the project.

---

## 📜 License

CheatRunner is licensed under the **GNU General Public License v3.0**.

See the `LICENSE` file for the full license text.

```text
GNU General Public License v3.0
```
