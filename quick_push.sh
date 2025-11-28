#!/bin/bash
# 快速推送到GitHub

echo "检查GitHub CLI..."
if command -v gh &> /dev/null; then
    echo "使用GitHub CLI创建仓库并推送..."
    gh repo create calculate-token --public --source=. --remote=origin --push
else
    echo "GitHub CLI未安装，请手动操作："
    echo ""
    echo "1. 在GitHub上创建仓库: https://github.com/new"
    echo "   仓库名: calculate-token"
    echo ""
    echo "2. 然后运行:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/calculate-token.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
fi
