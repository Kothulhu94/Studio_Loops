@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ============================================================
REM Gemma 26B-A4B Q4_XS Vulkan launcher for KoboldCPP
REM Expected layout:
REM   %~d0\Studio_Loop\koboldcpp.exe
REM   %~d0\Studio_Loop\models\*.gguf
REM ============================================================

set "ROOT=%~dp0"
if not exist "%ROOT%koboldcpp.exe" set "ROOT=%~d0\Studio_Loop\"

set "KOBOLD_EXE=%ROOT%koboldcpp.exe"
set "MODEL_DIR=%ROOT%models"

REM Prefer exact 26B-A4B Q4_XS naming, then fallback to any 26B Q4_XS GGUF.
set "MODEL_FILE="

for %%F in ("%MODEL_DIR%\*26B*A4B*Q4_XS*.gguf") do (
    if exist "%%~fF" set "MODEL_FILE=%%~fF"
)

if not defined MODEL_FILE (
    for %%F in ("%MODEL_DIR%\*26B*Q4_XS*.gguf") do (
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
    echo ERROR: No 26B-A4B Q4_XS GGUF model found in:
    echo %MODEL_DIR%
    echo.
    echo Expected something like:
    echo *26B*A4B*Q4_XS*.gguf
    echo or
    echo *26B*Q4_XS*.gguf
    pause
    exit /b 1
)

echo ============================================================
echo Launching KoboldCPP - Gemma 26B-A4B Q4_XS Vulkan
echo Model: %MODEL_FILE%
echo ============================================================

"%KOBOLD_EXE%" ^
  --model "%MODEL_FILE%" ^
  --usevulkan ^
  --gpulayers 99 ^
  --threads 8 ^
  --contextsize 8192 ^
  --blasbatchsize 512 ^
  --host 127.0.0.1 ^
  --port 5001 ^
  --skiplauncher

pause
