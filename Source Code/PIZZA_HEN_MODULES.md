# PIZZA HEN v0.1 module baseline

- **Identity layer:** original PIZZA HEN dashboard name, icon and startup notification.
- **Game Manager:** visible Toolbox module that launches the installed Itemzflow backend through Title ID `ITEM00001`.
- **Kstuff Control:** external normal Kstuff Lite v1.09 baseline at `/data/PIZZA_HEN/kstuff.elf`, with legacy `/data/etaHEN/kstuff.elf` fallback and embedded fallback.
- **Primary data root:** `/data/PIZZA_HEN`.
- **Compatibility note:** internal etaHEN-derived symbols remain untouched in v0.1 to reduce regression risk. They are implementation details, not visible branding.
