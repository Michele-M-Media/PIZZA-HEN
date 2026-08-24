# 🍕 PIZZA HEN

**PIZZA HEN** is an experimental all-in-one PS5 homebrew environment maintained by **Michele Media**.

This project started from the GPLv3 etaHEN 2.5B source base and has been extensively reworked around a PIZZA HEN runtime, UI, service chain, Multi-SDK build policy, KStuff selector, frozen ShadowMount integration, Toolbox, Game Manager integration, cheats, plugin management, FTP, and debugging services.

> **Status:** v0.1 beta / pre-release  
> Some components are experimental, especially the App Plugin Manager lifecycle introduced from observed etaHEN 2.6B behavior.

## Highlights

- PIZZA HEN Toolbox available from a PS5 Media tile.
- Graphical boot selector:
  - KStuff Lite 1.09 — Modern Mode
  - KStuff DR 1.2 — Compatibility Mode
- Exactly one KStuff engine per boot session.
- ShadowMountPlus 1.6beta16 kept as a frozen/pristine upstream runtime asset.
- Automatic FTP service.
- Automatic ps5debug-NG service.
- Direct Game Manager integration with Itemzflow when `ITEM00001` is installed.
- Unified cheat repository support.
- Game Overlay GPU / CPU / RAM sections disabled by default.
- PIZZA HEN App Plugin Manager (beta) with `[DEFAULT]`, per-title sections, `?autoload`, runtime session state and persistent configuration.
- Capability-based Multi-SDK build discovery.

## Multi-SDK policy

PIZZA HEN must not require one named Payload SDK release.

Supported discovery aliases:

```text
PIZZA_HEN_SDK
PS5_PAYLOAD_SDK
PS5SDK
PAYLOAD_SDK
```

Future/alternate toolchains can be selected with:

```text
PIZZA_HEN_TOOLCHAIN_FILE=/absolute/path/to/toolchain.cmake
PIZZA_HEN_CMAKE_WRAPPER=/absolute/path/to/sdk-cmake-wrapper
```

See [`SDK_COMPATIBILITY.txt`](SDK_COMPATIBILITY.txt).

## Build

### Windows + WSL

Run:

```text
RUN_BUILD_PIZZA_HEN_v0.1.bat
```

### Linux / WSL / compatible host

```bash
./RUN_BUILD_PIZZA_HEN.sh
```

The build scripts perform SDK capability discovery and static regression gates before compiling.

## Runtime chain

```text
PIZZA-HEN
  -> local web selector
  -> KStuff Lite 1.09 OR KStuff DR 1.2
  -> ShadowMountPlus
  -> FTP
  -> ps5debug-NG
  -> PIZZA HEN runtime / Toolbox
```

## Game Manager

PIZZA HEN does **not** redistribute Itemzflow in this repository.

When Itemzflow is installed with title ID `ITEM00001`, the PIZZA HEN Toolbox can launch it directly as the Game Manager.

## App Plugin Manager

The current App Plugin Manager is **beta**.

Its configuration is stored under:

```text
/data/PIZZA_HEN/plugins/apps/plugins.ini
```

Example:

```ini
[DEFAULT]
/data/PIZZA_HEN/plugins/apps/global.sprx?autoload

[PPSA00001]
/data/PIZZA_HEN/plugins/apps/example.sprx?autoload
```

Disabling autoload prevents future automatic loads. A plugin already loaded inside an application is not forcibly hot-unloaded by the current beta implementation.

## Project data

Primary data root:

```text
/data/PIZZA_HEN
```

## License and upstream work

PIZZA HEN is distributed under the **GNU GPLv3** where applicable to the GPL-covered source base.

This project incorporates, derives from, integrates with, or preserves work from multiple open-source PS5 projects. Their authorship and licenses are not replaced by PIZZA HEN branding.

See [`CREDITS.md`](CREDITS.md), [`THIRD_PARTY.md`](THIRD_PARTY.md), and [`LICENSE`](LICENSE).

## Warning

This is experimental homebrew software. Use it only on hardware and software you are authorized to modify. Keep backups of important data.

---

**Project direction / PIZZA HEN branding:** Michele Media 🍕🐓


## CheatRunner 0.17 integration

The legacy PIZZA HEN/etaHEN cheat route is retired. The Toolbox now builds and launches the vendored CheatRunner v0.17 source on demand, embeds its upstream dashboard on port 9999, and deep-links the currently running Title ID when available. See `CHEATRUNNER_INTEGRATION.md`.


## R7.20.1 auto-launcher behavior correction
Homebrew Channel, APR EMU UPDATE and Game Compressor now disclose their launcher/tile behavior correctly. PIZZA HEN does not require a separate external PKG for these entries, but the upstream/runtime component may install, refresh or remove its own launcher tile. All PIZZA HEN-owned explanatory text remains 31-language.
