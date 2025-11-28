@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo Windows Build Script
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

echo Checking dependencies...
python -c "import flask; import transformers; import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        echo Try offline install: install_offline.bat
        pause
        exit /b 1
    )
)

if not exist "tokenizers" (
    echo Error: tokenizers directory not found
    pause
    exit /b 1
)

echo.
echo Starting build...
echo.

python build_windows.py

if errorlevel 1 (
    echo.
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed!
echo ========================================
echo.
echo Output directory: dist\TokenCalculator
echo.
pause
