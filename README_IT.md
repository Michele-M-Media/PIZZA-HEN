# 🍕 PIZZA HEN v2.00 — Italiano

[English](README.md)

**PIZZA HEN** è un ambiente homebrew sperimentale all-in-one per PS5, mantenuto da **Michele Media**.

Il progetto mantiene un proprio layer di integrazione, organizzazione runtime, Toolbox, catena di servizi, politica di build e branding, preservando allo stesso tempo licenze e attribuzioni dei progetti open source upstream utilizzati.

> **Stato release:** checkpoint sorgente pubblico v2.00.  
> **Stato validazione:** l'audit incluso nella v2.00 registra il PASS completo del gate statico I18N. Da solo **non** equivale a un nuovo hardware-PASS per questo specifico checkpoint I18N-only.

## Novità principali della v2.00

La v2.00 è il checkpoint **complete internationalization final gate** costruito sulla baseline runtime R7.25.2.16.1 già usata come riferimento hardware funzionante.

- **31 lingue/locali** nella Toolbox PIZZA HEN con keyset di traduzione identici.
- Copertura a 31 locali mantenuta per **selector KStuff**, **selector ShadowMount**, tabella locale nativa **ShellUI** e **notifiche dei servizi**.
- Supporto **RTL arabo** preservato.
- Descrizioni e label di stato precedentemente hard-coded spostate nei dati di localizzazione.
- UI Toolbox di PoorDS4 e Fan Target / ps5-fan-control localizzata in tutti i 31 locali.
- Runtime intenzionalmente congelato durante il completamento del layer I18N.
- Tutti i **91 file ELF** del checkpoint v2.00 restano byte-identici alla baseline R7.25.2.16.1.
- Tutte le **127 funzioni JavaScript nominate** di `toolbox_launcher.html` restano byte-identiche alla baseline.
- Le funzioni di scan/install del Package Installer restano congelate.
- `debug_services_launcher.html` rimane byte-per-byte sul bridge ripristinato e protetto dalle regressioni hardware.

Audit completo: [`V2_00_COMPLETE_I18N_AUDIT.txt`](V2_00_COMPLETE_I18N_AUDIT.txt)

## Funzioni principali

PIZZA HEN riunisce in un unico ambiente PS5 i principali componenti del progetto:

- Toolbox PIZZA HEN e workflow tramite contenuti Media.
- Più percorsi KStuff selezionabili dal selector grafico.
- Selector ShadowMount con percorsi stabile/sperimentale e skip supportato per i workflow compatibili.
- Web service integrato / Homebrew Channel.
- Servizi FTP e ps5debug-NG.
- ELF Loader con verifica dello stato runtime.
- Package Installer / integrazione DPIv2.
- CheatRunner e relativo workflow cheat.
- PIZZA HEN Payload Repository / Plugin Manager.
- Controllo ventola.
- Servizio helper Remote Play.
- Web File Manager, Linux Loader e Game Download.
- SVT Play e player multimediali opzionali.
- Ulteriori payload/servizi forniti dall'utente preservati secondo le regole di freeze del progetto.

Non tutti i componenti supportano tutti i firmware. La compatibilità reale dipende dal percorso KStuff, ShadowMount e backend/servizio selezionato.

## Modello runtime

La root dati principale è:

```text
/data/PIZZA_HEN
```

La catena è basata su selector e servizi scelti dall'utente, senza forzare l'avvio automatico di ogni componente opzionale:

```text
PIZZA HEN
  -> selector KStuff
  -> percorso KStuff selezionato
  -> selector ShadowMount / skip supportato
  -> ambiente Media / Toolbox PIZZA HEN
  -> websrv + servizi e strumenti selezionati
```

Diverse integrazioni recenti usano intenzionalmente un comportamento **NO-PKG / NO-TILE**, esponendo il servizio o la WebUI senza installare applicazioni launcher aggiuntive.

## Build

### Windows + WSL

Usare il wrapper final-gate v2.00:

```text
RUN_BUILD_V200_I18N_ONLY_FINAL_GATE_FIX.bat
```

### Linux / WSL / host compatibile

Il percorso di build corrente usa:

```bash
chmod +x build_v01_rebase_latest_toolbox.sh
./build_v01_rebase_latest_toolbox.sh
```

Alcuni nomi degli script mantengono denominazioni storiche per compatibilità anche se il checkpoint del repository è v2.00.

PIZZA HEN usa una politica **Multi-SDK** basata sul rilevamento delle capacità, senza imporre una singola release hard-coded del Payload SDK. Vedi [`SDK_COMPATIBILITY.txt`](SDK_COMPATIBILITY.txt).

## Validazione statica v2.00

L'audit pubblicato registra:

- complete-I18N gate: **24/24 PASS**;
- **58 test statici Python PASS** nelle batch richiamate dallo script di build;
- sintassi JavaScript Toolbox: PASS;
- sintassi JavaScript Debug Services launcher: PASS;
- sintassi JavaScript selector ShadowMount: PASS;
- sintassi JavaScript selector KStuff: PASS;
- sintassi Bash dello script di build principale: PASS.

L'audit classifica intenzionalmente questo checkpoint come **STATIC-PASS** finché un risultato build/hardware non viene registrato separatamente.

## Asset third-party congelati

PIZZA HEN non riscrive il testo generato internamente dagli ELF third-party congelati. Quando un componente è marcato frozen o user-supplied, il binario viene preservato secondo le regole del progetto invece di essere modificato silenziosamente per branding o traduzione.

Vedi:

- [`CREDITS.md`](CREDITS.md)
- [`THIRD_PARTY.md`](THIRD_PARTY.md)
- [`LICENSE`](LICENSE)

## Changelog e note di rilascio

- [`CHANGELOG.md`](CHANGELOG.md)
- [`RELEASE_NOTES_v2.00.md`](RELEASE_NOTES_v2.00.md)

## Direzione del progetto

Direzione del progetto, integrazione e branding PIZZA HEN: **Michele Media**.

PIZZA HEN non è affiliato né approvato da Sony Interactive Entertainment. È software homebrew sperimentale: usalo solo in ambienti in cui comprendi e accetti i rischi.
