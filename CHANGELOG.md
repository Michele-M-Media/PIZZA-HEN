# PIZZA HEN Changelog

## v1.0 — public release checkpoint

- Promoted the hardware-tested PIZZA HEN line to v1.0.
- KStuff Lite updated to 1.10; KStuff DR 1.2 retained as the alternate selector choice.
- ShadowMountPlus 1.6beta16 remains the frozen upstream runtime baseline.
- CheatRunner 0.17 integrated as the Toolbox cheat backend and launched on demand.
- DPIv2 12.20+ `MetaInfo` path aligned with the observed etaHEN 2.6B call shape.
- DPIv2 12.x path hardware-confirmed on firmware **12.20 through 12.70**.
- Multi-language PS5-locale UI and capability-based Multi-SDK build discovery retained.
- Onion-derived multi-firmware Debug Services / ShellCore routing retained.
- Game Options CheatRunner shortcut remains experimental and is not part of the v1.0 compatibility claim.

## R7.6.3 — Hidden legacy Toolbox hosts restore

- Restored the R7.2 DOM panels for System Options, Rest Mode Options, Controller Shortcuts, Extras / Firmware Backends, Homebrew Store and PS5 webMAN Games.
- Preserved the CE-108262 rollback: Toolbox open does not auto-run ShellUI injection.
- Preserved plugin scan, KlogSrv, Fan Target, PHU/Pizza Overlay, KStuff Toggle and Payload Manager code paths.

## R7.6.1 — Plugin Scan / Service Runtime Repair

- Restores util startup behavior to the pre-Payload-Manager path; Payload Repository remains on-demand only.
- Plugin scan publishes the same catalog to `/data` and `/user/data` runtime aliases.
- Web Toolbox reads either catalog alias.
- Direct ELF launch path avoids the PS5 WebKit `Cannot access uninitialized variable` failure observed on hardware.

## v0.1-beta

Initial public beta checkpoint with PIZZA HEN identity, Toolbox, KStuff selector, ShadowMountPlus baseline, automatic services, Media launcher, Multi-SDK build discovery and the first public UI/service integration.
