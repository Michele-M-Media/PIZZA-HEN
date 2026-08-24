# 🍕 PIZZA HEN v2.00

[Italiano](README_IT.md)

**PIZZA HEN** is an experimental all-in-one PS5 homebrew environment maintained by **Michele Media**.

The project keeps its own integration layer, runtime organization, Toolbox, service chain, build policy and branding while preserving the licenses and attribution of the upstream open-source projects it builds on.

> **Release status:** v2.00 public source checkpoint.  
> **Validation status:** the included v2.00 audit records a complete static I18N gate PASS. It does **not**, by itself, claim a fresh hardware PASS for this exact I18N-only checkpoint.

## v2.00 highlights

v2.00 is the **complete internationalization final-gate checkpoint** built on the hardware-working R7.25.2.16.1 runtime baseline.

- **31 locales** across the PIZZA HEN Toolbox with identical translation keysets.
- 31-locale coverage retained for the **KStuff selector**, **ShadowMount selector**, native **ShellUI locale table** and **service notifications**.
- **Arabic RTL** support preserved.
- Previously hard-coded Toolbox descriptions and status labels moved into the localization data.
- PoorDS4 and Fan Target / ps5-fan-control Toolbox UI localized across all 31 locales.
- Runtime behavior intentionally frozen while the I18N data layer was completed.
- All **91 ELF files** in the v2.00 checkpoint remain byte-identical to the R7.25.2.16.1 baseline.
- All **127 named JavaScript functions** in `toolbox_launcher.html` remain byte-identical to that baseline.
- Package Installer scan/install functions remain frozen.
- `debug_services_launcher.html` remains byte-for-byte frozen at its restored hardware-working bridge.

Full audit: [`V2_00_COMPLETE_I18N_AUDIT.txt`](V2_00_COMPLETE_I18N_AUDIT.txt)

## Main capabilities

PIZZA HEN brings the project components into one PS5-oriented environment:

- PIZZA HEN Toolbox and Media-tile workflow.
- Multiple KStuff paths through the graphical selector.
- ShadowMount selection, including the established stable/experimental paths and the supported skip path for compatible workflows.
- Integrated web service / Homebrew Channel path.
- FTP and ps5debug-NG services.
- ELF Loader service with runtime-state validation.
- Package Installer / DPIv2 integration.
- CheatRunner integration and cheat workflow.
- PIZZA HEN Payload Repository / Plugin Manager workflow.
- Fan-control integration.
- Remote Play helper service.
- Web File Manager, Linux Loader and Game Download integrations.
- SVT Play and optional media-player services.
- Additional user-supplied service payload integrations preserved according to the project freeze rules.

Not every component supports every firmware. Actual compatibility depends on the selected KStuff, ShadowMount and service/backend path.

## Runtime model

The primary PIZZA HEN data root is:

```text
/data/PIZZA_HEN
```

The project is designed around a selector-driven boot/runtime chain rather than forcing every optional component to start automatically:

```text
PIZZA HEN
  -> KStuff selector
  -> selected KStuff path
  -> ShadowMount selector / supported skip path
  -> PIZZA HEN Media / Toolbox environment
  -> websrv + selected services and tools
```

Several later integrations intentionally use **NO-PKG / NO-TILE** behavior so that PIZZA HEN can expose the underlying service or WebUI without installing an additional launcher application.

## Build

### Windows + WSL

Use the v2.00 final-gate wrapper:

```text
RUN_BUILD_V200_I18N_ONLY_FINAL_GATE_FIX.bat
```

### Linux / WSL / compatible host

The current release path is built through:

```bash
chmod +x build_v01_rebase_latest_toolbox.sh
./build_v01_rebase_latest_toolbox.sh
```

Some build-script filenames retain historical names for compatibility even though the repository checkpoint is v2.00.

PIZZA HEN keeps a capability-based **Multi-SDK** discovery policy rather than requiring one hard-coded Payload SDK release. See [`SDK_COMPATIBILITY.txt`](SDK_COMPATIBILITY.txt).

## v2.00 static validation

The published audit records:

- complete-I18N gate: **24/24 PASS**;
- **58 Python static tests PASS** across the build-script batches;
- Toolbox JavaScript syntax: PASS;
- Debug Services launcher JavaScript syntax: PASS;
- ShadowMount selector JavaScript syntax: PASS;
- KStuff selector JavaScript syntax: PASS;
- main build script Bash syntax: PASS.

The audit deliberately labels this checkpoint **STATIC-PASS** until a build/hardware result is separately recorded.

## Frozen third-party assets

PIZZA HEN does not rewrite text generated internally by frozen third-party ELF binaries. Where a component is tracked as frozen or user-supplied, its binary is preserved according to the project rules instead of being silently modified for branding or translation.

See:

- [`CREDITS.md`](CREDITS.md)
- [`THIRD_PARTY.md`](THIRD_PARTY.md)
- [`LICENSE`](LICENSE)

## Changelog and release notes

- [`CHANGELOG.md`](CHANGELOG.md)
- [`RELEASE_NOTES_v2.00.md`](RELEASE_NOTES_v2.00.md)

## Project direction

Project direction, integration work and PIZZA HEN branding: **Michele Media**.

PIZZA HEN is not affiliated with or endorsed by Sony Interactive Entertainment. This software is experimental homebrew; use it only in environments where you understand and accept the risks.
