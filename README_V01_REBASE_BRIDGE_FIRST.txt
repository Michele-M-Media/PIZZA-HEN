PIZZA HEN - V0.1 BASE + LATEST TOOLBOX + DEBUG SERVICES RAW V0.1 BRIDGE

GOAL OF THIS BRANCH
- Start from PIZZA-HEN v0.1 source as the runtime base.
- Keep the original v0.1 etaHEN/PIZZA ShellUI, daemon, util, XML resources and pizzahen-toolbox-open helper unchanged.
- Replace only the Media Toolbox web page with the latest PIZZA HEN Toolbox UI.
- Add the latest pizzahen-api.elf as a separate helper for the latest web Toolbox.
- Move the ORIGINAL v0.1 Toolbox connection behind the Debug Services button.

DEBUG SERVICES PATH IN THIS BRANCH
Media tile -> latest toolbox-launcher.html -> Debug Services ->
/data/PIZZA_HEN/bin/pizzahen-toolbox-open.elf -> BREW_ENABLE_TOOLBOX ->
UNCHANGED v0.1 daemon -> UNCHANGED v0.1 ShellUI injection -> toolbox_online ->
UNCHANGED v0.1 ItemzLaunchByUri(debug_settings) -> UNCHANGED v0.1 etaHEN/PIZZA Toolbox XML.

IMPORTANT
- No Debug Services marker.
- No OnionHEN route.
- No debug_settings_old.
- No new ShellUI control path.
- No Mono/GMRS changes.
- No DPI/DPIv2 changes.
- The old etaHEN/PIZZA Toolbox from v0.1 is intentionally NOT edited yet.
- This is a bridge proof branch. The latest web Toolbox UI is present, but newer actions whose daemon/util backends did not exist in v0.1 are NOT claimed functional yet. Those are ported only after the original Debug Services connection is hardware-proven.
- KStuff Lite 1.10 current input is preserved in the bootstrapper path; v0.1 ShellUI/etaHEN text is intentionally left untouched for this bridge proof.
