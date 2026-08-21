@echo off
setlocal
cd /d "%~dp0"
echo ============================================================
echo  PIZZA HEN R7.5 - CHEATS TOOLBOX DIRECT + DEBUG OVERLAY OFF
echo  R7.4 feature base / R7.2 hardware-pass boot lineage
echo ============================================================
wsl bash -lc "cd '$(wslpath '%CD%')' && chmod +x ./build_v01_rebase_latest_toolbox.sh && ./build_v01_rebase_latest_toolbox.sh"
set RC=%ERRORLEVEL%
echo.
if %RC%==0 (
  echo BUILD FINISHED - check OUTPUT and BUILD_LOGS
) else (
  echo BUILD FAILED - send BUILD_LOGS and BUILD_RESULT to Kairos
)
pause
exit /b %RC%
