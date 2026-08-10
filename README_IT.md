# 🍕 PIZZA HEN — README Italiano

**PIZZA HEN** è un ambiente homebrew sperimentale all-in-one per PS5, mantenuto da **Michele Media**.

La base sorgente deriva da etaHEN 2.5B GPLv3, ma il progetto è stato riorganizzato con runtime, branding, Toolbox, selector KStuff, integrazione ShadowMount, servizi automatici, Game Manager, cheats, App Plugin Manager e politica di build Multi-SDK propri.

## Stato

**v0.1 beta / pre-release.** Le funzioni più recenti, in particolare il lifecycle dell'App Plugin Manager, vanno considerate ancora beta.

## Funzioni principali

- Icona PIZZA HEN Toolbox nei Contenuti multimediali.
- Selector grafico KStuff Lite 1.09 / KStuff DR 1.2.
- Un solo KStuff per sessione.
- ShadowMountPlus 1.6beta16 preservato come runtime upstream congelato.
- FTP automatico.
- ps5debug-NG automatico.
- Game Manager diretto su Itemzflow se `ITEM00001` è installato.
- Repository cheats unificati.
- Overlay GPU / CPU / RAM disattivato di default.
- App Plugin Manager beta con `[DEFAULT]`, sezioni Title ID e `?autoload`.
- Build Multi-SDK senza dipendenza obbligatoria da una singola release.

## Build

Windows + WSL: `RUN_BUILD_PIZZA_HEN_v0.1.bat`  
Linux / WSL / host compatibile: `./RUN_BUILD_PIZZA_HEN.sh`

Per la policy SDK completa vedi `SDK_COMPATIBILITY.txt`.

## Nota Itemzflow

Il PKG di Itemzflow non viene redistribuito nel repository. Va installato separatamente dalla fonte ufficiale. PIZZA HEN usa `ITEM00001` per l'integrazione diretta del Game Manager.

## Licenza

Il codice GPL derivato mantiene la GNU GPLv3 e le attribuzioni upstream. Vedi `LICENSE`, `CREDITS.md` e `THIRD_PARTY.md`.

**Project direction / branding:** Michele Media 🍕🐓
