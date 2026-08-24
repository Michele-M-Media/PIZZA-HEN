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


## R7.2 CE-108262 repair
Automatic R6 ShellUI preload has been removed. Daemon startup files are restored byte-for-byte to R5; R7.1 UTIL service backend remains. See READ_THIS_R7_2_CE108262.txt.


## CheatRunner 0.17 integration

The legacy PIZZA HEN/etaHEN cheat route is retired. The Toolbox now builds and launches the vendored CheatRunner v0.17 source on demand, embeds its upstream dashboard on port 9999, and deep-links the currently running Title ID when available. See `CHEATRUNNER_INTEGRATION.md`.

## DPIv2 12.20+ — etaHEN 2.6B MetaInfo repair
La build mantiene congelato il percorso DPIv2 gia usato fino a 12.00. Solo per le installazioni URL su 12.20+ il `MetaInfo` passato a `sceAppInstUtilInstallByPackage` viene azzerato e valorizzato esclusivamente in `uri`, replicando il call-shape osservato nel binario etaHEN 2.6B appena fornito. Debug Services/Onion, porta 12800 e upload PKG restano invariati. Vedi `DPIV2_12X_ETAHEN26B_METAINFO_REPAIR.md`.

