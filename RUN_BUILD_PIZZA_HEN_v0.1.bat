@echo off
setlocal EnableExtensions
cd /d "%~dp0"
echo ============================================================
echo  PIZZA HEN FIX44 - ETAHEN 2.6B DELTA UPDATE
echo ============================================================
where wsl.exe >nul 2>nul || (echo ERRORE: WSL non trovato.& pause& exit /b 20)
for /f "usebackq delims=" %%I in (`wsl.exe -e wslpath -a "%CD%"`) do set "WSL_DIR=%%I"
if not defined WSL_DIR (echo ERRORE: conversione percorso WSL fallita.& pause& exit /b 21)
wsl.exe -e bash "%WSL_DIR%/build_pizzahen_multisdk.sh"
set "RC=%ERRORLEVEL%"
echo.
if not "%RC%"=="0" (echo BUILD FALLITA - codice %RC%& echo Controlla BUILD_LOGS.) else (echo BUILD COMPLETATA.& echo Payload: OUTPUT\PIZZA-HEN-v0.1-FIX45-PLUGIN-MANAGER-LIFECYCLE.bin)
pause
exit /b %RC%
