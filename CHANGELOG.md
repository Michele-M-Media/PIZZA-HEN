# PIZZA HEN Changelog

## v2.00 — Complete I18N Final Gate / GitHub Source Checkpoint

**Published:** 2026-08-25

v2.00 promotes the R7.25.2.16.1 line into the public GitHub source checkpoint while keeping the runtime frozen and completing the project-wide PIZZA HEN internationalization layer.

### I18N

- Toolbox coverage expanded to **31 locales** with identical translation keysets.
- Existing KStuff selector, ShadowMount selector, native ShellUI locale table and service-notification locale table remain at 31 locales.
- Arabic RTL support preserved.
- Previously hard-coded Toolbox descriptions/status labels moved into explicit I18N mappings.
- PoorDS4 Toolbox UI localized across all 31 locales.
- Fan Target / ps5-fan-control Toolbox UI localized across all 31 locales.

### Runtime preservation

- All **91 ELF files** remain byte-identical to the R7.25.2.16.1 baseline.
- All **127 named JavaScript functions** in `toolbox_launcher.html` remain byte-identical to the baseline.
- Package Installer `scanPkgs`, `loadPkgCatalog` and `installPkg` function hashes remain frozen.
- Debug Services launcher remains byte-identical to the restored hardware-working bridge.
- No service launch/stop, `/hbldr`, websrv, Package Installer, PoorDS4, Fan Control, KStuff, ShadowMount, Storage, Themes Avatar, CheatRunner or payload-manager runtime logic was changed for the I18N final gate.

### Validation recorded by the checkpoint

- Complete-I18N gate: **24/24 PASS**.
- **58 Python static tests PASS** across the build-script batches.
- Toolbox JavaScript syntax: PASS.
- Debug Services launcher JavaScript syntax: PASS.
- ShadowMount selector JavaScript syntax: PASS.
- KStuff selector JavaScript syntax: PASS.
- Main release build-script Bash syntax: PASS.

The bundled audit labels the exact checkpoint **STATIC-PASS** until a WSL compile/hardware result is recorded separately.

### GitHub publication

- Clean v2.00 source snapshot first published to `main` in commit `9b800c4cffbbb7f6baa5e045cc77430b3bf5d11e`.
- Legacy build/log/checkpoint clutter was removed from the public snapshot while required regression fixtures and third-party notices were retained.
- README and release documentation were refreshed after publication without changing runtime source or ELF assets.

---

## Development history

### R7.25.2 — Remote Play Service Switch

- Remote Play moved to the same managed ON/OFF service-switch model used by the working media-player rows.
- User-supplied `ps5-remoteplay-get-pin` v0.1.1 preserved byte-for-byte.
- No autostart, PKG or tile added.

### R7.25.1 — Media Player Services correction

- ProsperoPlayer 1.0, PS-Play 2.1 and BFplayer standalone alpha.44 exposed as normal Services switches.
- Removed the custom install/delete staging and player conflict blocker.
- No player is started by the bootstrapper; users choose START/STOP from Services.
- SVT Play remains a direct Web App entry.

### R7.25 — SVT Play + Optional Media Players

- Added top-level SVT Play using the Web App URI from the supplied asset without creating an SVT launcher PKG/tile.
- Added optional media-player integrations and completed their PIZZA HEN localization coverage.

### R7.23.2 — Remote Play Direct Injection

- Updated the embedded Remote Play helper to the supplied v0.1.1 ELF while preserving it byte-for-byte.
- Direct `/hbldr` injection path was used before the later managed-service revision.

### R7.23.1 — Remote Play PIN Notification Repair

- Prevented PIZZA success feedback from masking the upstream PIN / Account ID notification.

### R7.23 — PIZZA HEN Payload Repository

- Replaced the legacy remote payload index with a PIZZA HEN-owned built-in catalog generated from the supplied JSON source.
- Accepted ELF entries require safe filenames, ELF magic and matching SHA-256 before installation.
- Repository feedback integrated with the 31-locale translation system.

### R7.22.1 — Remote Play + Tools naming repair

- Added real runtime verification to the managed Remote Play path used at that stage.
- Renamed Toolbox `Settings` to localized `Tools` / `Strumenti`.
- Preserved NO-PKG / NO-TILE behavior.

### R7.22 — Web File Manager + Linux Loader + Game Download

- Added Web File Manager integration with the launcher-installer path disabled in the PIZZA-derived ELF.
- Added Linux Loader with firmware gating from the supplied upstream support list.
- Added Pegasus DL and Spectrum Library under Game Download with managed/TCP state validation.
- Added all PIZZA-controlled strings for these integrations to all 31 locales.

### R7.20.2 — Full Toolbox NO-PKG / NO-TILE integration

- Homebrew Channel keeps the websrv WebUI while disabling upstream automatic launcher installation.
- APR EMU UPDATE and Game Compressor keep their useful runtime/WebUI functions while PIZZA disables launcher/tile creation paths.
- Frozen upstream inputs remain untouched; PIZZA variants are generated through gated derivation where required.

### R7.19 — Six user-supplied Services + full 31-language integration

- Added AirPSX and PS5Upload as resident Services with real TCP-state switches.
- Added PS5 FW Spoof, NP Fake Signin, WebKit Autoloader Installer and PS5 App Dumper as managed service/task switches.
- Added localized START/STOP/FAIL feedback.
- No new R7.19 payload auto-starts at boot.

### R7.18 — KStuff Base + ShadowMount skip

- Added the user-supplied KStuff Base path for its supported source profiles.
- Added the explicit `Do not launch ShadowMountPlus` selector path for compatible dump-installer workflows.
- Stable/experimental ShadowMount assets remained unchanged.

### R7.16 — Homebrew Channel

- Added the top-level Homebrew Channel using the existing websrv 0.34 WebUI.
- No Launcher PKG is required by the PIZZA integration.

### R7.15.2 — ELF Loader runtime-state repair

- ELF Loader state moved from generic process tracking to actual TCP-listener state on port 9021.
- START/STOP remained real actions; no cosmetic forced-ON state was added.

### R7.6.3 — Hidden legacy Toolbox hosts restore

- Restored the required hidden DOM hosts without reintroducing unsafe boot-time ShellUI injection.
- Preserved plugin scan, KlogSrv, Fan Target, overlay, KStuff and payload-manager code paths.

### R7.6.1 — Plugin Scan / Service Runtime Repair

- Restored the intended util startup behavior.
- Published plugin catalog aliases under the PIZZA HEN runtime roots.
- Kept the direct ELF launch path used to avoid the observed WebKit initialization failure.

### v1.0 development line

- KStuff Lite 1.10 update and alternate KStuff path work.
- CheatRunner v0.17 integration as the Toolbox cheat backend.
- DPIv2 12.20+ MetaInfo compatibility repair based on the observed call shape.
- Onion-derived multi-firmware Debug Services / ShellCore routing work.
- Multi-language UI and Multi-SDK build-discovery foundation.

### v0.1-beta

Initial public beta checkpoint with PIZZA HEN identity, Toolbox, KStuff selector, ShadowMount baseline, automatic core services, Media launcher and the first public service/UI integration.
