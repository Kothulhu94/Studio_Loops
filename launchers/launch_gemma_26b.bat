@echo off
setlocal EnableExtensions

set "ROOT=%~dp0.."
pushd "%ROOT%" || exit /b 1
call "%ROOT%\run_gemma_26b_a4b_iq4xs_vulkan_quality_FIXED.bat"
set "EXIT_CODE=%ERRORLEVEL%"
popd
exit /b %EXIT_CODE%
