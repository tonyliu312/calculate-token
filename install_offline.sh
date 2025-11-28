#!/bin/bash
# 离线安装Python依赖包（Linux/Mac）

echo "========================================"
echo "离线安装Python依赖包"
echo "========================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.8或更高版本"
    exit 1
fi

echo "检测到Python版本:"
python3 --version
echo

# 检查packages目录是否存在
if [ ! -d "packages" ]; then
    echo "错误: 未找到packages目录"
    echo "请确保packages目录存在并包含所有依赖包"
    exit 1
fi

echo "开始安装依赖包..."
echo

# 升级pip
python3 -m pip install --upgrade pip --no-index --find-links=packages

# 安装所有依赖
python3 -m pip install -r requirements.txt --no-index --find-links=packages

if [ $? -ne 0 ]; then
    echo
    echo "安装失败！请检查错误信息"
    exit 1
fi

echo
echo "========================================"
echo "安装完成！"
echo "========================================"

