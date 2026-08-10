# Changelog

## v0.1-beta

Initial public beta checkpoint.

### Core
- PIZZA HEN identity, data root and Toolbox.
- Graphical KStuff Lite 1.09 / KStuff DR 1.2 boot selector.
- Single-KStuff-per-boot ownership.
- Frozen pristine ShadowMountPlus 1.6beta16 integration.
- Automatic ftpsrv and ps5debug-NG chain.
- Media tile launcher and safe Toolbox reopen behavior.

### Toolbox
- PIZZA HEN UI/branding cleanup.
- Unified cheats sources.
- Direct Itemzflow Game Manager integration.
- Overlay GPU/CPU/RAM sections disabled by default.
- Redundant legacy PS5Debug setting removed from UI.

### etaHEN 2.6B observed delta
- App Plugin Manager beta.
- `[DEFAULT]` and per-title plugin sections.
- `?autoload` persistence.
- Session lifecycle/status tracking.
- PS4/PS5 FPS section naming/update.

### Build
- Capability-based Multi-SDK discovery.
- Current, legacy and override toolchain paths.
- Standard-library-only host regression tests.

### Known beta limitation
- App plugins already loaded into a running app are not forcibly hot-unloaded when autoload is disabled.
