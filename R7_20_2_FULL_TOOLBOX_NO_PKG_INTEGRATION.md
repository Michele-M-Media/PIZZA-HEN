# PIZZA HEN v1.0 R7.20.2 — Full Toolbox NO-PKG / NO-TILE Integration

This changeset integrates **Homebrew Channel**, **APR Emu Updater 1.4**, and **PS5 Game Compressor 1.0.4** with the same product policy used for CheatRunner: the feature/worker and WebUI remain available from PIZZA HEN, while automatic launcher-PKG / home-screen-tile creation is disabled.

## Source-grounded deltas

### Homebrew Channel / websrv 0.34
The frozen upstream `src/ps5/sys.c` calls `install_launcher()` from `sys_init()` after `sceAppInstUtilInitialize()`. PIZZA HEN keeps the frozen upstream ELF untouched and derives the runtime asset by replacing only the `sys_init -> install_launcher()` call at file offset `0x9C67` with five NOP bytes. websrv remains on TCP 8080 and `/index.html` remains the Homebrew Channel UI.

### APR Emu Updater 1.4
The user-supplied/upstream distribution does not include the C source for the updater, so no source code is invented. The frozen ELF is preserved and a deterministic, hash-gated derivative is generated from direct binary analysis. The derivative bypasses the startup tile-install thread, disables the `/api/tile/install` handler branch, disables the embedded `Reinstall tile` control, and hides the launcher-upload banner. APR APIs and the WebUI on TCP 6971 remain available.

### PS5 Game Compressor 1.0.4
The supplied source shows `on_ready()` calling `gc_launcher_start()`. PIZZA HEN preserves the frozen upstream ELF and derives the runtime asset by NOPing only that call at file offset `0x11944`. The compression worker and WebUI on TCP 5910 remain available; `PSGC50001` is not created by the integrated variant.

## Reproducibility
`TOOLS/build_integrated_no_tile_variants.py` validates every frozen input SHA-256, every patch preimage, and every derived SHA-256 before writing the three runtime assets. A changed upstream binary causes a hard failure rather than an unverified patch.

## I18N policy
All PIZZA HEN user-visible copy for these integrations is present in the existing 31 locales in this same changeset. Third-party WebUIs otherwise remain upstream except for APR's tile-specific controls described above.

## Safety / boot behavior
No new boot-time payload start is added, and the anti-CE-108262 rule remains in force: no boot-time ShellUI preload/injection and no boot-time `cmd_preload_toolbox_hooks()` call.
