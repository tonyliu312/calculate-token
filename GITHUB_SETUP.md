# GitHub仓库设置指南

## 创建GitHub仓库

1. 访问 https://github.com/new
2. 仓库名称：`calculate-token`
3. 描述：`Token计算工具 - 支持Qwen3和DeepSeek V3/V3.1系列模型`
4. 选择：Public 或 Private
5. **不要**勾选"Initialize this repository with a README"
6. 点击"Create repository"

## 推送代码到GitHub

在项目目录下运行以下命令：

```bash
# 1. 添加远程仓库（替换YOUR_USERNAME为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/calculate-token.git

# 2. 推送代码
git branch -M main
git push -u origin main
```

或者使用SSH：

```bash
git remote add origin git@github.com:YOUR_USERNAME/calculate-token.git
git branch -M main
git push -u origin main
```

## 已忽略的文件

以下文件/目录不会被提交：
- `tokenizers/` - Tokenizer文件（268MB，太大）
- `venv/` - Python虚拟环境
- `packages/` - Python依赖包（149MB，太大）
- `uploads/` - 上传的临时文件
- `__pycache__/` - Python缓存
- `dist/` - 打包输出
- `build/` - 构建临时文件

## 后续更新

```bash
git add .
git commit -m "更新说明"
git push
```

## 注意事项

1. **tokenizer文件太大**：已添加到.gitignore，不会提交
2. **依赖包**：已添加到.gitignore，用户需要自己下载
3. **README.md**：已包含使用说明

## 仓库结构

提交后的仓库将包含：
- 所有源代码文件（.py）
- Web界面文件（web/）
- 打包和安装脚本
- 文档文件（.md）
- requirements.txt
- .gitignore

**不包含**：
- tokenizers/（用户需要运行download_tokenizers.py下载）
- packages/（用户需要运行download_packages.bat下载）
- venv/（用户需要自己创建）

