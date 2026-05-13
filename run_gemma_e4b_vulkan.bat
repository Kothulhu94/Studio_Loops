@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM Open a secondary command prompt for the Studio Loop orchestrator
start "Studio Loop Terminal" cmd /k "cd /d %~dp0ai_harness && echo --- Studio Loop Terminal --- && echo Run: python .agent/orchestrator/studio_loop.py auto "Task""

REM ============================================================
REM Gemma E4B Vulkan launcher for KoboldCPP
REM Expected layout:
REM   %~d0\Studio_Loop\koboldcpp.exe
REM   %~d0\Studio_Loop\models\*.gguf
REM ============================================================

set "ROOT=%~dp0"
if not exist "%ROOT%koboldcpp.exe" set "ROOT=%~d0\Studio_Loop\"

set "KOBOLD_EXE=%ROOT%koboldcpp.exe"
set "MODEL_DIR=%ROOT%models"

REM Prefer Q4_K_M if present, otherwise use any E4B GGUF.
set "MODEL_FILE="

for %%F in ("%MODEL_DIR%\*E4B*Q4_K_M*.gguf") do (
    if exist "%%~fF" set "MODEL_FILE=%%~fF"
)

if not defined MODEL_FILE (
    for %%F in ("%MODEL_DIR%\*E4B*.gguf") do (
        if exist "%%~fF" set "MODEL_FILE=%%~fF"
    )
)

if not exist "%KOBOLD_EXE%" (
    echo ERROR: koboldcpp.exe not found:
    echo %KOBOLD_EXE%
    pause
    exit /b 1
)

if not defined MODEL_FILE (
    echo ERROR: No E4B GGUF model found in:
    echo %MODEL_DIR%
    echo.
    echo Expected something like:
    echo *E4B*.gguf
    pause
    exit /b 1
)

set "WATCH_SERVER=%ROOT%ai_harness\Loop_Central\loop_central_server.py"
set "KOBOLD_LOG=%ROOT%ai_harness\logs\loop_central\kobold.log"
if not exist "%ROOT%ai_harness\logs\loop_central" mkdir "%ROOT%ai_harness\logs\loop_central"

call :start_watch_ui "Gemma E4B Vulkan"
call :ensure_kobold_slot_free
if not "%ERRORLEVEL%"=="0" exit /b 1

echo ============================================================
echo Launching KoboldCPP - Gemma E4B Vulkan
echo Model: %MODEL_FILE%
echo ============================================================

powershell -Command "& '%KOBOLD_EXE%' --model '%MODEL_FILE%' --usevulkan --gpulayers 99 --threads 8 --contextsize 32768 --blasbatchsize 512 --host 127.0.0.1 --port 5001 --skiplauncher | Tee-Object -FilePath '%KOBOLD_LOG%' -Append"

set "KCPP_EXIT=%ERRORLEVEL%"
>>"%KOBOLD_LOG%" echo [%date% %time%] KoboldCPP exited with code %KCPP_EXIT%.
pause
exit /b %KCPP_EXIT%

:start_watch_ui
set "MODEL_LABEL=%~1"
if not exist "%WATCH_SERVER%" (
    echo WARNING: Loop_Central server not found at: %WATCH_SERVER%
    exit /b 0
)

where py >nul 2>nul
if "%ERRORLEVEL%"=="0" (
    start "Loop_Central" cmd /c "py -3 "%WATCH_SERVER%" --open --model-label "%MODEL_LABEL%" --model-path "%MODEL_FILE%" --kobold-port 5001 || pause"
    exit /b 0
)

where python >nul 2>nul
if "%ERRORLEVEL%"=="0" (
    start "Loop_Central" cmd /c "python "%WATCH_SERVER%" --open --model-label "%MODEL_LABEL%" --model-path "%MODEL_FILE%" --kobold-port 5001 || pause"
)
exit /b 0

:ensure_kobold_slot_free
powershell -NoProfile -Command "if (Get-Process koboldcpp -ErrorAction SilentlyContinue) { exit 0 } exit 1" >nul 2>nul
if not "%ERRORLEVEL%"=="0" exit /b 0

echo.
echo KoboldCPP is already running. Both Gemma launchers use port 5001.
echo Close the existing KoboldCPP process before launching this model?
choice /c YN /n /m "Close existing KoboldCPP and continue? [Y/N] "
if errorlevel 2 exit /b 1

taskkill /IM koboldcpp.exe /F >nul 2>nul
timeout /t 2 /nobreak >nul
exit /b 0
