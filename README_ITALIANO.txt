PIZZA HEN v0.1 FIX26 - FTP AFTER SHADOWMOUNT

CHECKPOINT CORRENTE
- FIX25 Browser KStuff Selector resta la baseline hardware PASS e non viene modificata.
- Dopo la scelta KStuff Lite 1.09 oppure KStuff DR 1.2, parte ShadowMountPlus 1.6beta16 pristine.
- FIX26 aggiunge come Payload #1 post-ShadowMount ftpsrv v0.21 upstream, porta TCP 2121.
- Il runtime ftpsrv fornito dall'utente viene incorporato invariato; il sorgente upstream e conservato in ThirdParty.
- Dopo l'avvio FTP PIZZA HEN verifica realmente la porta 2121 prima di avanzare.
- La pipeline si ferma intenzionalmente prima del Payload #2, che verra aggiunto nel checkpoint successivo.

PIPELINE FIX26
PIZZA-HEN.elf -> browser selector -> Lite 1.09 / DR 1.2 -> KStuff ready -> ShadowMount -> ftpsrv 0.21 -> FTP:2121 ready -> STOP Payload #2

------------------------------------------------------------

PIZZA HEN v0.1 FIX18 - ALL SHADOWMOUNT SCAN ROOTS + PIZZA HEN

Questa release parte dalla FIX11 confermata su hardware per kstuff e non modifica il percorso kstuff/libelfldr gia funzionante.

NOVITA FIX13
- Build dell INTERO PIZZA HEN con selezione SDK per capacita, senza dipendenza dal nome PAYLOAD_SDK_V042.
- Variabili accettate: PIZZA_HEN_SDK, PS5_PAYLOAD_SDK, PS5SDK, PAYLOAD_SDK.
- Rilevamento automatico su installazioni standard e alberi Windows/WSL.
- Preferenza per toolchain/prospero.cmake dei Payload SDK correnti; fallback compatibile a bin/prospero-cmake.
- Windows via WSL, Linux e macOS tramite lo stesso launcher POSIX.
- Compressione bootstrapper portabile via Python LZMA, eliminando stat -c/lzma come vincolo host.
- ShadowMountPlus 1.6beta16 modificato incluso e compilato con LO STESSO SDK selezionato per PIZZA HEN.
- Policy overlay: prima fakelib, solo se assente fallback fakelib2.
- SQLite ShadowMount rilevato automaticamente tra sqlite3 e sqlite.
- Runtime diagnostico: bootstrap -> kstuff (baseline FIX11 congelata) -> ShadowMountPlus -> stop prima del daemon.

IMPORTANTE
Multi-SDK significa compatibilita tra release/layout del PS5 Payload SDK tramite rilevamento delle capacita del toolchain. Non significa automaticamente compatibilita con ogni firmware PS5. Il target runtime di questa release resta retail 10.01.

WINDOWS
1. Mettere kstuff 1.09 normale in KSTUFF_INPUT (se non e gia disponibile).
2. Eseguire RUN_DOCTOR_PIZZA_HEN.bat per verificare SDK/toolchain.
3. Eseguire RUN_BUILD_PIZZA_HEN_v0.1.bat.
4. Output: OUTPUT\PIZZA-HEN-v0.1-FIX18-ALL-SCANROOTS-SHADOWMOUNT.bin

LINUX / macOS
Eseguire ./RUN_BUILD_PIZZA_HEN.sh dopo aver impostato PS5_PAYLOAD_SDK o PIZZA_HEN_SDK, oppure usare una installazione standard riconoscibile.

Non viene eseguito alcun invio automatico alla console.

FIX15: correzione link ShadowMount per SDK recenti: niente doppio SONAME libkernel_sys; import kernel/pthread/dl selezionati per capacita; NID MDBG extra risolto a runtime.


FIX18: The complete upstream ShadowMountPlus 1.6beta16 scan-root set is preserved. PIZZA_HEN roots are added, never substituted. /mnt/shadowmnt/pfsc and /mnt/shadowmnt remain always scanned. Custom scanpath entries add extra roots instead of deleting the defaults. manual.lst remains available for arbitrary explicit paths.


=== FIX30 — TOOLBOX COMPLETO etaHEN 2.5B ===
Il runtime etaHEN ereditato non termina più prima dei daemon: dopo la catena PIZZA HEN vengono avviati Utility Daemon, Main Daemon, Toolbox ShellUI e plugin/payload. Aggiunta icona PIZZA HEN Toolbox nei Contenuti multimediali (PZHN00001), cheats unificate FIX29, Discord RPC visibile e tutte le funzioni etaHEN 2.5B presenti nel sorgente mantenute. Vedi FIX30_FUNCTION_MATRIX.txt.
