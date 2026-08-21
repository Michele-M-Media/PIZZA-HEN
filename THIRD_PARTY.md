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
