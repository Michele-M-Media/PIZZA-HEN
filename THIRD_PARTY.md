# Third-party components

PIZZA HEN contains or references third-party source code and frozen runtime assets.

Each third-party component remains governed by its own license and copyright notices. Do not assume the root GPLv3 license changes the license of independently licensed components.

The public Git repository intentionally does **not** include the Itemzflow PKG backend. Install Itemzflow separately from its official project.

Frozen runtime inputs used by the PIZZA HEN pipeline are kept under `ThirdParty/` where required by the current build/verification flow. Their upstream identity and hashes are preserved by the project tests.

Before redistributing a release binary or third-party binary asset, verify the corresponding upstream redistribution terms.
