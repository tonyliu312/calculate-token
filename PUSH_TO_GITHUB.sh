#!/bin/bash
# 推送到GitHub的脚本

echo "=========================================="
echo "推送到GitHub"
echo "=========================================="
echo ""
echo "请先确保："
echo "1. 已在GitHub上创建了仓库：calculate-token"
echo "2. 已替换下面的YOUR_USERNAME为你的GitHub用户名"
echo ""
read -p "请输入你的GitHub用户名: " username

if [ -z "$username" ]; then
    echo "错误: 用户名不能为空"
    exit 1
fi

echo ""
echo "添加远程仓库..."
git remote add origin https://github.com/${username}/calculate-token.git 2>/dev/null || \
git remote set-url origin https://github.com/${username}/calculate-token.git

echo "设置主分支..."
git branch -M main

echo "推送到GitHub..."
git push -u origin main

echo ""
echo "完成！"
echo "访问: https://github.com/${username}/calculate-token"
