@echo off
setlocal EnableExtensions
cd /d "%~dp0"
set "PAYLOAD=%CD%\OUTPUT\PIZZA-HEN-v0.1-FIX37-MENU-BRANDING-MARGHERITA.bin"
if not exist "%PAYLOAD%" (
  echo ERRORE: prima esegui RUN_BUILD_PIZZA_HEN_v0.1.bat
  pause
  exit /b 20
)
set /p PS5IP=Inserisci IP della PS5: 
set /p PS5PORT=Porta ELF loader [9021]: 
if "%PS5PORT%"=="" set "PS5PORT=9021"

echo Invio manuale di PIZZA HEN a %PS5IP%:%PS5PORT% ...
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command ^
  "$p=[IO.File]::ReadAllBytes('%PAYLOAD%');" ^
  "$c=[Net.Sockets.TcpClient]::new();" ^
  "$c.Connect('%PS5IP%',%PS5PORT%);" ^
  "$s=$c.GetStream();$s.Write($p,0,$p.Length);$s.Flush();$s.Dispose();$c.Dispose();" ^
  "Write-Host ('Inviati '+$p.Length+' byte')"
set "RC=%ERRORLEVEL%"
pause
exit /b %RC%
