#!/bin/bash
# 下载Windows平台的Python依赖包（用于离线安装）

echo "========================================"
echo "下载Windows平台Python依赖包"
echo "========================================"
echo

# 创建packages目录
mkdir -p packages

# 支持的Python版本
PYTHON_VERSIONS=(3.9 3.10 3.11 3.12)

echo "将下载以下Python版本的包: ${PYTHON_VERSIONS[@]}"
echo "这可能需要一些时间..."
echo

# 下载每个Python版本的包
for version in "${PYTHON_VERSIONS[@]}"; do
    echo "----------------------------------------"
    echo "下载 Python $version 的包..."
    echo "----------------------------------------"
    
    pip download -r requirements.txt \
        -d packages \
        --platform win_amd64 \
        --only-binary=:all: \
        --python-version $version \
        --no-deps
    
    if [ $? -eq 0 ]; then
        echo "✓ Python $version 的包下载完成"
    else
        echo "✗ Python $version 的包下载失败"
    fi
    echo
done

# 下载通用依赖（不依赖Python版本）
echo "----------------------------------------"
echo "下载通用依赖包..."
echo "----------------------------------------"

pip download -r requirements.txt \
    -d packages \
    --platform win_amd64 \
    --only-binary=:all:

echo
echo "========================================"
echo "下载完成！"
echo "========================================"
echo
echo "packages目录大小:"
du -sh packages/
echo
echo "包文件数量:"
ls -1 packages/*.whl | wc -l
echo
echo "下一步："
echo "1. 将packages目录复制到离线Windows机器"
echo "2. 运行 install_offline.bat 安装依赖"

