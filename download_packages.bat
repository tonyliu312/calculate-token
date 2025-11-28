@echo off
chcp 65001 >nul
echo ========================================
echo 下载Windows平台Python依赖包
echo ========================================
echo.

REM 创建packages目录
if not exist "packages" mkdir packages

echo 将下载Python 3.9, 3.10, 3.11, 3.12版本的包
echo 这可能需要一些时间...
echo.

REM 下载Python 3.9的包
echo ----------------------------------------
echo 下载 Python 3.9 的包...
echo ----------------------------------------
pip download -r requirements.txt -d packages --platform win_amd64 --only-binary=:all: --python-version 3.9 --no-deps
if errorlevel 1 (
    echo Python 3.9 的包下载失败
) else (
    echo Python 3.9 的包下载完成
)
echo.

REM 下载Python 3.10的包
echo ----------------------------------------
echo 下载 Python 3.10 的包...
echo ----------------------------------------
pip download -r requirements.txt -d packages --platform win_amd64 --only-binary=:all: --python-version 3.10 --no-deps
if errorlevel 1 (
    echo Python 3.10 的包下载失败
) else (
    echo Python 3.10 的包下载完成
)
echo.

REM 下载Python 3.11的包
echo ----------------------------------------
echo 下载 Python 3.11 的包...
echo ----------------------------------------
pip download -r requirements.txt -d packages --platform win_amd64 --only-binary=:all: --python-version 3.11 --no-deps
if errorlevel 1 (
    echo Python 3.11 的包下载失败
) else (
    echo Python 3.11 的包下载完成
)
echo.

REM 下载Python 3.12的包
echo ----------------------------------------
echo 下载 Python 3.12 的包...
echo ----------------------------------------
pip download -r requirements.txt -d packages --platform win_amd64 --only-binary=:all: --python-version 3.12 --no-deps
if errorlevel 1 (
    echo Python 3.12 的包下载失败
) else (
    echo Python 3.12 的包下载完成
)
echo.

REM 下载通用依赖
echo ----------------------------------------
echo 下载通用依赖包...
echo ----------------------------------------
pip download -r requirements.txt -d packages --platform win_amd64 --only-binary=:all:

echo.
echo ========================================
echo 下载完成！
echo ========================================
echo.
echo 下一步：
echo 1. 将packages目录复制到离线Windows机器
echo 2. 运行 install_offline.bat 安装依赖
echo.
pause

