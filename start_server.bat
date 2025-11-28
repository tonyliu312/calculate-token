@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo Token Calculator Web Server
echo ========================================
echo.
echo Starting web server...
echo.
python app.py
pause

