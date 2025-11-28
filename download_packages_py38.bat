@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo Download Python 3.8 Dependencies for Windows
echo ========================================
echo.

REM Create packages directory
if not exist "packages" mkdir packages

echo Downloading packages for Python 3.8...
echo This may take some time...
echo.

REM Download Python 3.8 packages
echo Downloading Python 3.8 packages...
pip download -r requirements.txt -d packages --platform win_amd64 --only-binary=:all: --python-version 3.8 --no-deps

if errorlevel 1 (
    echo Python 3.8 packages download failed
) else (
    echo Python 3.8 packages downloaded successfully
)
echo.

REM Download universal dependencies
echo Downloading universal dependencies...
pip download -r requirements.txt -d packages --platform win_amd64 --only-binary=:all:

echo.
echo ========================================
echo Download completed!
echo ========================================
echo.
echo Package directory size:
dir packages | find "File(s)"
echo.
echo Next steps:
echo 1. Copy packages directory to offline Windows machine
echo 2. Run install_offline.bat to install dependencies
echo.
pause

