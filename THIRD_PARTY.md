# Third-party components

PIZZA HEN contains or references third-party source code and frozen runtime assets.

Each third-party component remains governed by its own license and copyright notices. Do not assume the root GPLv3 license changes the license of independently licensed components.

The public Git repository intentionally does **not** include the Itemzflow PKG backend. Install Itemzflow separately from its official project.

Frozen runtime inputs used by the PIZZA HEN pipeline are kept under `ThirdParty/` where required by the current build/verification flow. Their upstream identity and hashes are preserved by the project tests.

Before redistributing a release binary or third-party binary asset, verify the corresponding upstream redistribution terms.

## CheatRunner v0.17

PIZZA HEN integrates CheatRunner v0.17 by maj0r as the active cheat backend inside the Toolbox.
Upstream commit: `9c75165182bedb9c21e9b58a1468caeb8a3fdb0f`.
The upstream runtime source is vendored under `Source Code/third_party/CheatRunner-0.17` and remains GPLv3 under its own `LICENSE`.
`PIZZA_UPSTREAM_SHA256_MANIFEST.txt` records every file from the supplied source archive. PIZZA HEN adds only the two missing deterministic CMake helper generators under `tools/`, documented in `tools/PIZZA_HEN_INTEGRATION_NOTE.md`.
CheatRunner retains its own runtime path `/data/cheatrunner`, local HTTP service on port 9999, dashboard, API, trainer formats and credits.


## ELF Loader 0.24

PIZZA HEN R7.15 uses the user-supplied ps5-payload-dev elfldr 0.24 prebuilt as the Toolbox Services ELF Loader backend on TCP 9021. The matching upstream source snapshot `ps5-elfldr-0.24-148b71c.zip` is preserved under `ThirdParty/`. Its upstream LICENSE is preserved in that source tree.

## APR Emu Updater 1.4

PIZZA HEN R7.15 embeds the user-supplied `apr_emu_updater.elf` as an on-demand Toolbox entry named `APR EMU UPDATE`. The supplied 1.4 archive and README are preserved under `ThirdParty/`; the supplied archive did not contain a separate LICENSE file, so redistribution terms must be verified with the upstream project before public redistribution. Runtime data and update behavior remain owned by APR Emu Updater.

## PS5 Game Compressor 1.0.4

PIZZA HEN R7.20 embeds the user-supplied `game-compressor.elf` as an on-demand top-level Toolbox entry named `Game Compressor`. The matching source archive `PS5-Game-Compressor-1.0.4.zip` is preserved under `ThirdParty/PS5-Game-Compressor-1.0.4-USER-SUPPLIED-FROZEN/` together with an extracted audit copy. Upstream credits identify Juma Sayeh as creator. The PIZZA HEN integration does not install the optional `PSGC50001` launcher tile: it launches the payload directly and opens its native web UI on TCP 5910. The supplied source snapshot contains no root LICENSE file, so redistribution terms must be verified with the upstream project before public redistribution.

## R7.22 frozen user-supplied payloads
- PS5 Web File Manager 1.5 — upstream: owendswang/ps5-web-file-manager. Frozen ELF SHA-256 `9a7d7e5c685900d7f916cdc08cb6f7ea7e9cf5a4576f2799157b3f251deedf3c`. PIZZA derives a no-launcher variant by disabling only the launcher-install entry point.
- ps5-linux-loader 2.4 — upstream: ps5-linux/ps5-linux-loader. Frozen and embedded unchanged, SHA-256 `51382795b486f7c5a3681648d457d129088311fc3f9601aeaff78dc72fafcf1d`.
- Pegasus DL 1.7.0 — upstream: pegasus-ps5/pegasus-dl. Frozen ELF SHA-256 `cb2a4b3c248323f2432ce118cb1bf4975146035239ce9b571a9bdb51b3fee226`. PIZZA derives a no-launcher variant with startup auto-install and manual launcher install disabled.
- Spectrum Library 1.4.2 — upstream: Phoenixx1202/Spectrum-Library. Frozen ELF SHA-256 `54755ce62d99be610afe364e26de05eaa9e2d92192cda525790a563c6296261f`. Public repository exposes the README but not matching source; PIZZA keeps the original frozen and applies a SHA/preimage-gated no-tile derivative that neutralizes the installer worker.

## R7.23 user-supplied Payload Repository source

The user-supplied archive `Nuovo Archivio WinRAR(1).rar` and its `json/payloads.json` catalog are frozen under `ThirdParty/Payload-Repository-USER-SUPPLIED-FROZEN/`. R7.23 uses that catalog only as metadata for the PIZZA HEN Payload/Plugin repository. The source contains 83 entries; the PIZZA generator accepts 79 `.elf` entries and excludes 4 `.bin` entries because the current Plugin Manager install path is intentionally ELF-only. Individual payload files remain third-party works and retain their own upstream redistribution terms. PIZZA HEN preserves the supplied download URL and SHA-256 for each accepted entry and verifies the ELF magic and checksum before installation.


## R7.25 user-supplied media payloads
- **SVT Play v0.2** — frozen ELF SHA-256 `5bdf25142512f25dc6269bd7c90a914001fcef5e731125a74aa23c1a8d91810f`. R7.25 does not execute its BREW10002 installer; it uses the embedded `webAppUri` only.
- **ProsperoPlayer 1.0** — frozen ELF SHA-256 `40b9955273982cd563e1b16bd428ea6a9c399e7d4bc55b220fe223948572cdad`; public project reference `KINGDKAK/ProsperoPlayer`.
- **PS-Play 2.1** — frozen ELF SHA-256 `e3392379d5bc6ca4e44cb0d2a1d8921083b2c3ea480725f68378831874542d8d`; public project reference `MounirHero/PS-Play`.
- **BFplayer standalone 0.1.0-alpha.44** — frozen ELF SHA-256 `0d028deb145d6fc9a5b55d43a45e072919178fbb261c66cd914ebcfb0b3b05c0`; public project reference `ItsBlurf/BFplayer`.
- The three optional service ELFs are preserved byte-for-byte and are copied to the managed payload directory only after explicit user INSTALL.

## R7.25.2.16 PoorDS4 0.1.0-rc38

PIZZA HEN integrates the user-supplied PoorDS4 RC38 release by ItsBlurf as a dedicated **Tools → PoorDS4** entry. The integration preserves the three upstream release ELFs byte-for-byte: `PoorDS4rc38.elf`, `PoorDS4-status.elf`, and `PoorDS4-stop.elf`. PIZZA HEN only deploys and launches those original files; it does not patch their controller bridge, status logic, firmware admission checks, cleanup, or stop behavior. The matching user-supplied source archive and SHA256SUMS are frozen under `ThirdParty/PoorDS4-0.1.0-rc38-USER-SUPPLIED-FROZEN/`. Upstream identifies PoorDS4 as a focused wireless-DS4 derivative of Ghostcontrol and licenses the project under GPL-3.0-or-later.

