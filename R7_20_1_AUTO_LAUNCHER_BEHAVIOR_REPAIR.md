# PIZZA HEN R7.20.1 — Auto-launcher behavior repair

This changeset corrects the model/metadata used for three top-level Toolbox entries without changing their upstream runtime logic.

- **Homebrew Channel / websrv 0.34:** PIZZA HEN still navigates directly to `/index.html`. Hardware testing shows that opening the channel can install/refresh the Homebrew Launcher tile automatically. This is now described as an upstream/runtime side effect, not as “no PKG/no tile”.
- **APR EMU UPDATE / APR Emu Updater 1.4:** its own upstream README states that the payload serves a WebUI and puts a tile on the PS5 home screen. PIZZA HEN launches the ELF; the updater owns the tile.
- **Game Compressor 1.0.4:** upstream source calls `gc_launcher_start()` once the web server is ready. Its app installer uses AppInstUtil and manages the `PSGC50001` launcher tile. PIZZA HEN launches the ELF and opens TCP 5910; Game Compressor owns the tile.

Policy: PIZZA HEN does not ship or manually dispatch a separate external PKG for these entries unless a future integration explicitly requires it. A payload may still install/update/remove its own launcher tile internally.

All corrected PIZZA HEN-owned descriptions/status text are localized in all 31 supported locales.
