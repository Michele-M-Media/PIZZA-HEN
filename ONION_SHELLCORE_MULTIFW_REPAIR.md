# PIZZA HEN v1.0 — Onion Debug Services + ShellCore Multi-Firmware Repair

Baseline: `PIZZA-HEN-v1.0-MULTILANGUAGE.zip`.

## Source-grounded changes

- Restored the previous FIX70.49 PS5 Payload SDK runtime kernel/libhijacker resolver (`offsets.hpp`, `offsets.cpp`, `KProc` runtime proc offsets).
- Restored FIX70.49 ShellCore capability handling: old `/data` byte-pattern patch is applied only where an existing pattern is known; modern firmware does **not** receive invented offsets/patterns.
- Ported OnionHEN 0.0.10 Debug Settings route policy into ShellUI: standard route through 10.60, `debug_settings_old` from 11.00+.
- Ported OnionHEN BootHelper rewrite behavior and both 11.6+/12.x Settings-internal navigator guards (`UpdateNavigationState`, `DebugSettingsModule.GetModel`).
- Direct Toolbox/Debug Services shortcuts now use the firmware-selected route instead of hardcoded `debug_settings`.
- RNPS/Hermes string-length mutation disabled; route/navigation selects the legacy XML host instead.
- Daemon Toolbox auto-start uses the same Onion policy.

## Validation boundary

Static/source validation can prove the route and resolver are wired consistently. A 12.xx PS5 test is still required before marking this build hardware-PASS.
