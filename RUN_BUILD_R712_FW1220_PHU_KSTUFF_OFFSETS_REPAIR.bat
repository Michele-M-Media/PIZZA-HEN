@echo off
setlocal
cd /d "%~dp0"
echo ============================================================
echo  PIZZA HEN R7.12 - FW 12.20+ PHU/KStuff offsets repair
echo ============================================================
wsl bash -lc "cd '$(wslpath '%CD%')' && chmod +x ./build_v01_rebase_latest_toolbox.sh && ./build_v01_rebase_latest_toolbox.sh"
set RC=%ERRORLEVEL%
echo.
if not "%RC%"=="0" (
  echo BUILD FAILED - exit %RC%
) else (
  echo BUILD PASS - see OUTPUT and BUILD_LOGS
)
pause
exit /b %RC%
