# PIZZA HEN v1.0 source-sync audit

Audit date: 2026-08-21

Canonical local checkpoint:
`PIZZA-HEN-v1.0-MULTILANGUAGE-CHEATRUNNER-DPIV2-12X-ETAHEN26B-PHU-KSTUFF-FW1220-CHEATRUNNER-GAME-OPTIONS-SHORTCUT_3.zip`

SHA-256:
`354cb861325400930eaaf91706382a54897efe9ae425a80126c9313eef08b79b`

## Results

- Canonical archive contains 1,670 files under its project root.
- No filename or scanned text reference to `R7.14` / `R714` was found in the canonical checkpoint.
- The archive contains the top-level GPL license plus third-party license files for bundled/upstream components.
- The existing `main` branch is not byte-identical to the canonical checkpoint and must not be treated as the final v1.0 source tree yet.

Selected Git blob SHA comparison:

| Path | Canonical checkpoint | Current `main` | Status |
| --- | --- | --- | --- |
| `Source Code/CMakeLists.txt` | `fde04335a8eca5e919cac48afa439751a9c163b1` | `08f01ea37cc8864417e1fed80970e5fc241a452a` | differs |
| `Source Code/daemon/source/main.cpp` | `b7db1e37cfb0ba4a6299d4141a64184810120b31` | `24ae807a6c1d7f656e97bef2e95728fb1cc15504` | differs |
| `Source Code/shellui/src/HookFunctions.cpp` | `010fc101b44c185b671ce15df929481d65666019` | `1295f1d4473664756266f593e1e656325f8bcbd0` | differs |
| `build_pizzahen_multisdk.sh` | `32fa23a4e72956387dfc17fd2b0c1fdf587132ed` | `32fa23a4e72956387dfc17fd2b0c1fdf587132ed` | matches |
| `LICENSE` | `f288702d2fa16d3cdf0035b15a9fcbc552cd88e7` | `f288702d2fa16d3cdf0035b15a9fcbc552cd88e7` | matches |
| `CREDITS.md` | `0514f600ba686e0647490dd6b56d0300fb13c4f2` | `0514f600ba686e0647490dd6b56d0300fb13c4f2` | matches |

## Release gate

PR #3 must remain unmerged until the maintainer has manually synchronized the intended public source tree and re-verified the final release contents. This audit intentionally records only release-integrity metadata and does not replace hardware validation.
