@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo Install Python Dependencies Offline
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

if not exist "packages" (
    echo Error: packages directory not found
    pause
    exit /b 1
)

echo Installing dependencies...
echo.

python -m pip install --upgrade pip --no-index --find-links=packages

python -m pip install -r requirements.txt --no-index --find-links=packages

if errorlevel 1 (
    echo.
    echo Installation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation completed!
echo ========================================
echo.
pause
