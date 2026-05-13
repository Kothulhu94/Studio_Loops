@echo off
setlocal EnableExtensions

set "ROOT=%~dp0.."
pushd "%ROOT%" || exit /b 1
call "%ROOT%\run_gemma_e4b_vulkan.bat"
set "EXIT_CODE=%ERRORLEVEL%"
popd
exit /b %EXIT_CODE%
