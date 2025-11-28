#!/usr/bin/env python3
"""
Windows打包脚本 - 使用PyInstaller打包应用
"""

import os
import sys
import shutil
from pathlib import Path

try:
    import PyInstaller.__main__
except ImportError:
    print("错误: 请先安装PyInstaller")
    print("运行: pip install pyinstaller")
    sys.exit(1)


def build_app():
    """打包应用"""
    print("=" * 80)
    print("开始打包Windows应用")
    print("=" * 80)
    
    # 获取项目根目录
    project_root = Path(__file__).parent
    dist_dir = project_root / "dist"
    build_dir = project_root / "build"
    
    # 清理旧的构建文件
    if dist_dir.exists():
        print("清理旧的dist目录...")
        shutil.rmtree(dist_dir)
    if build_dir.exists():
        print("清理旧的build目录...")
        shutil.rmtree(build_dir)
    
    # 确定路径分隔符（Windows使用分号，Unix使用冒号）
    import platform
    sep = ';' if platform.system() == 'Windows' else ':'
    
    # PyInstaller参数
    pyinstaller_args = [
        'app.py',  # 主程序
        '--name=TokenCalculator',  # 可执行文件名
        '--onedir',  # 单文件夹模式
        # '--windowed',  # Windows下不显示控制台（注释掉以便看到日志）
        f'--add-data=web{sep}web',  # 包含web目录
        f'--add-data=tokenizers{sep}tokenizers',  # 包含tokenizers目录
        '--hidden-import=transformers',  # 确保包含transformers
        '--hidden-import=torch',  # 确保包含torch
        '--hidden-import=flask',  # 确保包含flask
        '--hidden-import=calculate_tokens',  # 确保包含核心模块
        '--collect-all=transformers',  # 收集transformers的所有子模块
        '--collect-all=torch',  # 收集torch的所有子模块
        '--collect-all=tokenizers',  # 收集tokenizers的所有子模块
        '--noconfirm',  # 覆盖输出目录
        '--clean',  # 清理临时文件
    ]
    
    # 检查tokenizers目录是否存在
    tokenizers_dir = project_root / "tokenizers"
    if not tokenizers_dir.exists() or not any(tokenizers_dir.iterdir()):
        print("\n警告: tokenizers目录不存在或为空")
        print("请先运行 download_tokenizers.py 下载tokenizer文件")
        response = input("是否继续打包（将无法离线运行）? (y/n): ")
        if response.lower() != 'y':
            print("取消打包")
            sys.exit(1)
    else:
        print(f"找到tokenizers目录: {tokenizers_dir}")
        print(f"包含 {len(list(tokenizers_dir.iterdir()))} 个项目")
    
    print("\n开始打包（这可能需要几分钟）...")
    print("-" * 80)
    
    try:
        # 运行PyInstaller
        PyInstaller.__main__.run(pyinstaller_args)
        
        print("\n" + "=" * 80)
        print("打包完成！")
        print("=" * 80)
        
        # 检查输出
        exe_dir = dist_dir / "TokenCalculator"
        if exe_dir.exists():
            exe_file = exe_dir / "TokenCalculator.exe"
            if exe_file.exists():
                print(f"\n可执行文件位置: {exe_file}")
                print(f"输出目录: {exe_dir}")
                print(f"\n文件大小: {get_size(exe_dir)}")
                
                # 创建启动脚本
                create_start_script(exe_dir)
                
                print("\n下一步:")
                print("1. 将整个 TokenCalculator 文件夹复制到Windows机器")
                print("2. 双击 start.bat 启动应用")
                print("3. 浏览器会自动打开 http://localhost:5000")
            else:
                print("错误: 未找到可执行文件")
                sys.exit(1)
        else:
            print("错误: 输出目录不存在")
            sys.exit(1)
    
    except Exception as e:
        print(f"\n打包失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def get_size(path):
    """获取目录大小（人类可读格式）"""
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total += os.path.getsize(filepath)
    
    # 转换为MB或GB
    if total < 1024 * 1024:
        return f"{total / 1024:.2f} KB"
    elif total < 1024 * 1024 * 1024:
        return f"{total / (1024 * 1024):.2f} MB"
    else:
        return f"{total / (1024 * 1024 * 1024):.2f} GB"


def create_start_script(exe_dir):
    """创建Windows启动脚本"""
    start_script = exe_dir / "start.bat"
    
    script_content = """@echo off
chcp 65001 >nul
echo ========================================
echo Token计算工具
echo ========================================
echo.
echo 正在启动应用...
echo.

REM 启动应用
start "" "TokenCalculator.exe"

REM 等待应用启动
timeout /t 3 /nobreak >nul

REM 打开浏览器
start http://localhost:5000

echo.
echo 应用已启动！
echo 浏览器将自动打开 http://localhost:5000
echo.
echo 按任意键关闭此窗口（应用将继续运行）
pause >nul
"""
    
    with open(start_script, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"\n已创建启动脚本: {start_script}")


if __name__ == "__main__":
    build_app()

