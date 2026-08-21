# 🍕 PIZZA HEN v1.0

**PIZZA HEN** is an all-in-one PS5 homebrew environment maintained by **Michele Media**.

This public v1.0 checkpoint is based on the hardware-tested PIZZA HEN line with the Multi-SDK runtime, KStuff selector, ShadowMount integration, PIZZA HEN Toolbox, CheatRunner 0.17, DPIv2, FTP, ps5debug-NG, package-install support, multilingual UI and multi-firmware routing.

## Release status

**v1.0 — public release checkpoint**

Hardware validation for the DPIv2 12.x path is confirmed on **firmware 12.20 through 12.70**. The Game Options CheatRunner shortcut contained in this checkpoint should be treated as **experimental** and is not required for the main PIZZA HEN feature set.

## Highlights

- PIZZA HEN Toolbox from the PS5 Media area.
- Graphical KStuff selector:
  - KStuff Lite 1.10
  - KStuff DR 1.2
- One KStuff engine per boot session.
- ShadowMountPlus 1.6beta16 preserved as the frozen upstream runtime baseline.
- CheatRunner 0.17 integrated in the Toolbox.
- DPIv2 package-install path with the 12.20+ MetaInfo repair.
- Automatic FTP and ps5debug-NG service chain.
- Multi-language UI following the PS5 system locale.
- Multi-SDK / capability-based build discovery.
- Multi-firmware ShellCore / Debug Services routing derived from the project's Onion/etaHEN compatibility work.

## DPIv2 firmware validation

The v1.0 release checkpoint includes the DPIv2 12.x repair based on the etaHEN 2.6B call shape for firmware 12.20+.

**Hardware-confirmed range for this path: 12.20 → 12.70.**

See [`DPIV2_12X_ETAHEN26B_METAINFO_REPAIR.md`](DPIV2_12X_ETAHEN26B_METAINFO_REPAIR.md).

## Build

### Windows + WSL

For the exact public v1.0 checkpoint, run:

```text
RUN_BUILD_R713_CHEATRUNNER_GAME_OPTIONS_SHORTCUT.bat
```

### Linux / WSL

```bash
./RUN_BUILD_PIZZA_HEN.sh
```

The build system performs SDK discovery and regression gates before compiling.

## Multi-SDK policy

PIZZA HEN does not require one hard-coded Payload SDK release. Supported discovery aliases include:

```text
PIZZA_HEN_SDK
PS5_PAYLOAD_SDK
PS5SDK
PAYLOAD_SDK
```

Optional overrides:

```text
PIZZA_HEN_TOOLCHAIN_FILE=/absolute/path/to/toolchain.cmake
PIZZA_HEN_CMAKE_WRAPPER=/absolute/path/to/sdk-cmake-wrapper
```

See [`SDK_COMPATIBILITY.txt`](SDK_COMPATIBILITY.txt).

## CheatRunner 0.17

The legacy cheat route has been replaced by the vendored CheatRunner v0.17 backend. The Toolbox can start CheatRunner on demand, use its local dashboard/API on port 9999 and deep-link the active Title ID when available.

See [`CHEATRUNNER_INTEGRATION.md`](CHEATRUNNER_INTEGRATION.md).

## Project data

Primary runtime root:

```text
/data/PIZZA_HEN
```

## Third-party work and license

PIZZA HEN derives from and integrates multiple open-source PS5 projects. Upstream authorship and licensing remain intact.

GPL-covered inherited/modified source remains under **GNU GPLv3**. Independently licensed components retain their own licenses.

See:

- [`LICENSE`](LICENSE)
- [`CREDITS.md`](CREDITS.md)
- [`THIRD_PARTY.md`](THIRD_PARTY.md)

## Safety / usage

Use this software only on hardware and software you are authorized to modify. Keep backups of important data. This project is provided without warranty.

---

**Project direction / PIZZA HEN branding:** Michele Media 🍕🐓
