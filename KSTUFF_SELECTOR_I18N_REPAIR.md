# PIZZA HEN v1.0 — KStuff Selector i18n repair

Targeted delta on top of `MULTILANGUAGE-ONION-DEEP-AUDIT-COMPILE-GATE-REPAIR`.

- `bootstrapper/assets/kstuff_selector.html`: all user-visible selector/status/footer strings now follow the same 31-locale PS5 WebView/OS locale policy already used by Toolbox and Debug Services.
- `bootstrapper/assets/kstuff_selector.js`: alternate websrv carousel labels use the same locale policy.
- Arabic uses RTL, consistent with the existing R7.7 layer.
- Engine names, authors, `/hbldr` route, selector ELF, one-engine-per-session behavior and boot order are unchanged.
- No KStuff, ShadowMount, Onion routing or ShellCore runtime code was changed.
