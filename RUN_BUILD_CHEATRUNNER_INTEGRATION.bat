@echo off
setlocal
cd /d "%~dp0"
echo ============================================================
echo  PIZZA HEN v1.0 - MULTILANGUAGE + ONION + CHEATRUNNER 0.17
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
