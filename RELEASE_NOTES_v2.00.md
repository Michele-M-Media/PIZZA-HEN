# PIZZA HEN v2.00 — Release Notes

PIZZA HEN v2.00 is the **Complete I18N Final Gate** source checkpoint.

The release is intentionally focused on completing the user-facing localization layer while preserving the runtime behavior of the R7.25.2.16.1 baseline.

## What changed

- Toolbox translation data completed across **31 locales**.
- KStuff selector, ShadowMount selector, native ShellUI locale table and service notifications remain covered across 31 locales.
- Arabic RTL behavior preserved.
- Previously hard-coded Toolbox descriptions/status labels moved into explicit localization mappings.
- PoorDS4 and Fan Target / ps5-fan-control Toolbox UI localized across all 31 locales.

## What did not change

The v2.00 I18N gate was designed to avoid runtime regressions:

- all **91 ELF files** remain byte-identical to the R7.25.2.16.1 baseline;
- all **127 named JavaScript functions** in `toolbox_launcher.html` remain byte-identical;
- Package Installer scan/catalog/install functions remain frozen;
- Debug Services launcher remains byte-identical to the restored bridge;
- no launch/stop behavior, `/hbldr`, websrv, Package Installer, KStuff, ShadowMount, Fan Control, PoorDS4, Storage, Themes Avatar, CheatRunner or payload-manager runtime logic was changed for this gate.

## Validation

The included audit records:

- **24/24** complete-I18N gate PASS;
- **58** Python static tests PASS;
- JavaScript syntax PASS for Toolbox, Debug Services and ShadowMount selector;
- KStuff selector JavaScript syntax PASS;
- release build-script Bash syntax PASS.

See [`V2_00_COMPLETE_I18N_AUDIT.txt`](V2_00_COMPLETE_I18N_AUDIT.txt) for the exact checkpoint statement.

### Validation wording

The audit deliberately describes the exact v2.00 checkpoint as **STATIC-PASS** until a WSL build/hardware result is recorded separately. This release note does not upgrade that status by assumption.

## Source checkpoint

The clean v2.00 source snapshot was first published to GitHub `main` as:

```text
9b800c4cffbbb7f6baa5e045cc77430b3bf5d11e
```

The documentation refresh that follows this snapshot changes presentation files only; it does not change the v2.00 runtime or bundled ELF assets.

## Major integrated areas

The v2.00 tree includes the current PIZZA HEN Toolbox, KStuff/ShadowMount selectors, Homebrew Channel/websrv path, FTP, ps5debug-NG, ELF Loader, Package Installer/DPIv2, CheatRunner, Payload Repository / Plugin Manager, Fan Control, Remote Play helper, Web File Manager, Linux Loader, Game Download, SVT Play and optional service integrations documented in the changelog.

Compatibility remains component- and firmware-dependent.

## License and credits

PIZZA HEN preserves the license and attribution requirements of the upstream and bundled projects. See:

- [`LICENSE`](LICENSE)
- [`CREDITS.md`](CREDITS.md)
- [`THIRD_PARTY.md`](THIRD_PARTY.md)

Project direction, integration and PIZZA HEN branding: **Michele Media**.
