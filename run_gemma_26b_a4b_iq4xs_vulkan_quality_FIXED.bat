@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ============================================================
REM Gemma 4 26B-A4B IQ4_XS Vulkan launcher for KoboldCPP
REM Quality-first profile for ROG Ally X / AMD 890M unified memory.
REM
REM Expected layout:
REM   Studio_Loop\
REM     koboldcpp.exe
REM     models\gemma-4-26B-A4B-it-UD-IQ4_XS.gguf
REM
REM Notes for KoboldCPP 1.112.x:
REM   --quantkv must be q8_0, q5_1, q4_0, f16, or bf16.
REM   Flash attention is enabled by default when available.
REM   Use --noflashattention only if you need to disable it.
REM ============================================================

set "ROOT=%~dp0"
if not exist "%ROOT%koboldcpp.exe" set "ROOT=%~d0\Studio_Loop\"

set "KOBOLD_EXE=%ROOT%koboldcpp.exe"
set "MODEL_DIR=%ROOT%models"

set "MODEL_FILE="

for %%F in ("%MODEL_DIR%\*26B*A4B*IQ4_XS*.gguf") do (
    if exist "%%~fF" set "MODEL_FILE=%%~fF"
)

if not defined MODEL_FILE (
    for %%F in ("%MODEL_DIR%\*26B*A4B*Q4_XS*.gguf") do (
        if exist "%%~fF" set "MODEL_FILE=%%~fF"
    )
)

if not defined MODEL_FILE (
    for %%F in ("%MODEL_DIR%\*26B*XS*.gguf") do (
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
    echo ERROR: No Gemma 4 26B-A4B IQ4_XS/Q4_XS GGUF model found in:
    echo %MODEL_DIR%
    pause
    exit /b 1
)

echo ============================================================
echo Gemma 4 26B-A4B IQ4_XS Vulkan launcher
echo KoboldCPP: %KOBOLD_EXE%
echo Model:     %MODEL_FILE%
echo ============================================================
echo.
echo Close other heavy apps before continuing.
echo The first profile is the one to use if it loads.
echo.
pause

REM ------------------------------------------------------------
REM PROFILE 1: QUALITY-FIRST
REM Best chance of being meaningfully better than E4B.
REM Full Vulkan offload, 6K context, q8_0 KV.
REM ------------------------------------------------------------
call :launch "QUALITY-FIRST: all GPU, 6K ctx, q8_0 KV" 99 6144 128 q8_0
if "%ERRORLEVEL%"=="0" goto :done

REM ------------------------------------------------------------
REM PROFILE 2: STABLE QUALITY
REM Full Vulkan offload, smaller context, q8_0 KV.
REM ------------------------------------------------------------
call :launch "STABLE QUALITY: all GPU, 4K ctx, q8_0 KV" 99 4096 128 q8_0
if "%ERRORLEVEL%"=="0" goto :done

REM ------------------------------------------------------------
REM PROFILE 3: MEMORY SAFE
REM Full Vulkan offload, 4K context, q5_1 KV.
REM Lower memory than q8_0 but usually better than q4_0.
REM ------------------------------------------------------------
call :launch "MEMORY SAFE: all GPU, 4K ctx, q5_1 KV" 99 4096 64 q5_1
if "%ERRORLEVEL%"=="0" goto :done

REM ------------------------------------------------------------
REM PROFILE 4: LAST RESORT
REM Lower GPU layers. Slower. Use only if all-GPU profiles fail.
REM ------------------------------------------------------------
call :launch "LAST RESORT: partial GPU, 4K ctx, q5_1 KV" 28 4096 64 q5_1
if "%ERRORLEVEL%"=="0" goto :done

echo.
echo ============================================================
echo All profiles exited. If none loaded, reboot the Ally, close
echo background apps, then run this file again.
echo ============================================================
pause
exit /b 1

:launch
set "PROFILE_NAME=%~1"
set "GPU_LAYERS=%~2"
set "CTX_SIZE=%~3"
set "BATCH_SIZE=%~4"
set "KV_QUANT=%~5"

echo.
echo ============================================================
echo Trying profile: %PROFILE_NAME%
echo GPU layers:   %GPU_LAYERS%
echo Context size: %CTX_SIZE%
echo Batch size:   %BATCH_SIZE%
echo KV cache:     %KV_QUANT%
echo ============================================================

"%KOBOLD_EXE%" ^
  --model "%MODEL_FILE%" ^
  --usevulkan ^
  --gpulayers %GPU_LAYERS% ^
  --threads 8 ^
  --contextsize %CTX_SIZE% ^
  --batchsize %BATCH_SIZE% ^
  --quantkv %KV_QUANT% ^
  --defaultgenamt 1024 ^
  --host 127.0.0.1 ^
  --port 5001 ^
  --skiplauncher

set "KCPP_EXIT=%ERRORLEVEL%"
echo.
echo KoboldCPP exited with code %KCPP_EXIT% for profile: %PROFILE_NAME%
echo.
if not "%KCPP_EXIT%"=="0" (
    echo Press any key to try the next fallback profile.
    pause >nul
)
exit /b %KCPP_EXIT%

:done
echo.
echo KoboldCPP closed normally.
pause
exit /b 0
