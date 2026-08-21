# 🍕 PIZZA HEN v1.0 — Italiano

**PIZZA HEN** è un ambiente homebrew all-in-one per PS5 mantenuto da **Michele Media**.

Questa è la baseline pubblica **v1.0**, scelta dopo la validazione hardware del progetto con Toolbox, selector KStuff, ShadowMount, CheatRunner 0.17, DPIv2, FTP, ps5debug-NG, build Multi-SDK, interfaccia multilingua e routing multi-firmware.

## Stato release

**v1.0 — checkpoint pubblico.**

Il percorso **DPIv2 12.x è confermato su hardware dal firmware 12.20 al 12.70**. La scorciatoia CheatRunner nel menu Game Options presente in questo checkpoint va invece considerata **sperimentale** e non è necessaria per il funzionamento principale di PIZZA HEN.

## Funzioni principali

- PIZZA HEN Toolbox nell'area Media della PS5.
- Selector grafico KStuff:
  - KStuff Lite 1.10
  - KStuff DR 1.2
- Un solo motore KStuff per sessione.
- ShadowMountPlus 1.6beta16 mantenuto come baseline upstream congelata.
- CheatRunner 0.17 integrato nella Toolbox.
- DPIv2 con repair MetaInfo per firmware 12.20+.
- FTP e ps5debug-NG automatici.
- UI multilingua basata sulla lingua di sistema PS5.
- Build Multi-SDK / capability-based.
- Routing ShellCore / Debug Services multi-firmware.

## Compatibilità DPIv2

Per il ramo DPIv2 12.x di questa release la validazione hardware è confermata su:

**12.20 → 12.70**

Vedi [`DPIV2_12X_ETAHEN26B_METAINFO_REPAIR.md`](DPIV2_12X_ETAHEN26B_METAINFO_REPAIR.md).

## Build

Windows + WSL:

```text
RUN_BUILD_R713_CHEATRUNNER_GAME_OPTIONS_SHORTCUT.bat
```

Linux / WSL:

```bash
./RUN_BUILD_PIZZA_HEN.sh
```

## Licenza e crediti

Il codice derivato GPL mantiene la **GNU GPLv3**. I componenti di terze parti conservano le rispettive licenze e attribuzioni.

Vedi `LICENSE`, `CREDITS.md` e `THIRD_PARTY.md`.

## Nota

Usare il software solo su hardware e software che si è autorizzati a modificare. Fare sempre un backup dei dati importanti.

---

**Project direction / branding:** Michele Media 🍕🐓
