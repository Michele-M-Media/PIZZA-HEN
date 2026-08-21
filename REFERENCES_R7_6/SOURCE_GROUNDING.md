# R7.6 source grounding

This repair uses the user-supplied binaries unchanged:

- kstuff-toggle-1.elf SHA256 `9009b96f36721a1b4c305735038d70cd72d596c553156bfa2a27e60a68ae2dee`
- kstuff-toggle-2.elf SHA256 `ae8c39e79f731b5b0515b8487ff7986cf9a626e760881dacc107bd888f3694c6`
- kstuff-toggle-3.elf SHA256 `0e87e92959791d9edf04c314802fcf18ccf37db74ae353d434a0062557f85093`
- klogsrv-ps5.elf SHA256 `e828ec144231f81547cb58bc7d2c396fa984be0c2295f31364b58017816dcceb`
- phu_overlay.elf SHA256 `8e20deefb9100705be8352dc6acb47241c6a044b93dc3f578f93c424789b2622`
- fan_target_65c.elf SHA256 `0bedeb564947530d09d1dfb27df63c2a09eaa7f51faf3ddcc90b3fb2870e6312`
- fan_target_70c.elf SHA256 `a9ad8502123799d58f8ddd9882d842f524c4ecc3ea6743a73c6dcdffd0bf30e0`
- fan_target_75c.elf SHA256 `4b52e09c48ebed1f369221c290e8ec4a9fdb2a477b7b7f44a1b8646958d9f69b`
- fan_target_80c.elf SHA256 `ccf2e709218f31cd9e6a0705c99646b8f030b877687df8377982a2f6ca10216e`
- fan_target_85c.elf SHA256 `c37019c351c1c5b05b43adbac29d85bfd25f8c0ab9d94371cacab1945d8e0fd0`

## CheatRunner review

The supplied CheatRunner 0.17 source does **not** contain the game OptionMenu/createJson/BootHelper/manifest-resource chain requested for the PS5 game Options menu. Its ShellUI payload hooks `Sce.PlayStation.Core.Input.GamePad.GetData` for the controller hotkey. Therefore CheatRunner is not embedded and is not a runtime dependency of PIZZA HEN.

The game Options -> `★ PIZZA HEN Cheats` -> native cheat menu path is restored from the already-present etaHEN/PIZZA ShellUI source: `OptionMenu.createJson` -> `etaHEN?Cheats_not_open` -> `BootHelper.Boot` -> Debug Settings resource request -> `GetManifestResourceStream_Hook` -> `generate_cheats_xml`.

The consumer hooks are installed by the existing lazy Shell service only after the Toolbox is opened. The automatic post-KStuff preload remains disabled to preserve the R7.5.1 anti-freeze change.

## Local payload/plugin manager

The R7.3 local control surface (`SCANSIONA`, `AGGIORNA LISTA`, `PLUGIN FOLDER`, `PAYLOAD FOLDER`) is restored. Payload Manager repository/download controls remain alongside it. Start/Stop/Auto Start still use the existing PIZZA HEN PluginManager and util IPC handlers.
