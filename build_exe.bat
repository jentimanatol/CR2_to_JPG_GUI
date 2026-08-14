@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo           Build CR2 to JPG Converter EXE
echo ============================================================
echo.

set "PYTHON="
where py.exe >nul 2>&1
if not errorlevel 1 set "PYTHON=py"
if not defined PYTHON (
    where python.exe >nul 2>&1
    if not errorlevel 1 set "PYTHON=python"
)

if not defined PYTHON (
    echo ERROR: Python was not found.
    pause
    exit /b 1
)

%PYTHON% --version
echo.
echo Installing build dependencies...
%PYTHON% -m pip install --upgrade pip
%PYTHON% -m pip install -r requirements-build.txt
if errorlevel 1 goto :error

echo.
echo Building EXE...
%PYTHON% -m PyInstaller --clean --noconfirm CR2_to_JPG.spec
if errorlevel 1 goto :error

echo.
echo ============================================================
echo Build completed successfully.
echo EXE: %CD%\dist\CR2-to-JPG-Converter.exe
echo ============================================================
echo.
pause
exit /b 0

:error
echo.
echo ERROR: Build failed.
pause
exit /b 1
