@echo off
setlocal EnableExtensions
cd /d "%~dp0"
where wsl.exe >nul 2>nul || (echo ERRORE: WSL non trovato.& pause& exit /b 20)
for /f "usebackq delims=" %%I in (`wsl.exe -e wslpath -a "%CD%"`) do set "WSL_DIR=%%I"
wsl.exe -e bash "%WSL_DIR%/build_pizzahen_multisdk.sh" --doctor
set "RC=%ERRORLEVEL%"
pause
exit /b %RC%
