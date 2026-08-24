@echo off
setlocal
cd /d "%~dp0"
wsl bash -lc "cd "$(wslpath '%CD%')" && chmod +x build_v01_rebase_latest_toolbox.sh && ./build_v01_rebase_latest_toolbox.sh"
set RC=%ERRORLEVEL%
echo.
if not "%RC%"=="0" (
  echo PIZZA HEN R7.18 BUILD FAILED - exit %RC%
) else (
  echo PIZZA HEN R7.18 BUILD PASS
)
pause
exit /b %RC%
