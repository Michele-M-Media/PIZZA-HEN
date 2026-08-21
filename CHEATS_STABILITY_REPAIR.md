# PIZZA HEN v1.0 — Cheats stability repair

Observed hardware symptom: PPSA31246 was identified correctly, but the cheat surface could not determine the installed `contentVersion`.

Repairs:
- restores R7.5 direct owned Toolbox route for Game Options Cheats (TID + live PID);
- adds source-proven installed PS5 metadata roots `/user/appmeta/<TID>/param.json` and `/user/app/<TID>/sce_sys/param.json` while retaining etaHEN roots;
- parse errors are real lookup failures, not pseudo-version strings;
- fixes etaHEN-derived monitor lifecycle (joinable monitor, cache invalidation ordering, preview-only state, stale-title guard);
- fixes invalid `cheat_index == cheats.size()` access.

Unchanged: Onion Debug routing, ShellCore, KStuff, ShadowMountPlus, cheat file-format parsers and exact version matching. Hardware validation is required.
