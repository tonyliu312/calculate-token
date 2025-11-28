# Windows打包检查清单

## 在Mac/Linux上准备（已完成）

- [x] Python依赖包已下载到 `packages/` 目录
- [x] Tokenizer文件已下载到 `tokenizers/` 目录（11个模型）
- [x] 所有源代码文件已准备
- [x] 打包脚本已创建

## 需要在Windows机器上完成

### 1. 环境准备
- [ ] 安装Python 3.8-3.12
- [ ] 安装依赖（在线或离线）
- [ ] 验证环境：`python -c "import flask; import transformers; print('OK')"`

### 2. 文件准备
- [ ] 将整个项目文件夹复制到Windows机器
- [ ] 确认 `tokenizers/` 目录包含11个模型
- [ ] 确认 `web/` 目录存在

### 3. 执行打包
- [ ] 运行 `package_for_windows.bat` 或 `python build_windows.py`
- [ ] 等待打包完成（可能需要5-15分钟）
- [ ] 检查 `dist/TokenCalculator/` 目录

### 4. 测试
- [ ] 进入 `dist/TokenCalculator/` 目录
- [ ] 双击 `start.bat` 测试运行
- [ ] 验证浏览器能正常访问
- [ ] 测试token计算功能

### 5. 分发准备
- [ ] 压缩 `dist/TokenCalculator/` 文件夹
- [ ] 创建使用说明文档
- [ ] 准备分发

## 快速打包命令

在Windows命令提示符中：

```cmd
REM 1. 进入项目目录
cd C:\path\to\calculate-token

REM 2. 安装依赖（如果有网络）
pip install -r requirements.txt

REM 3. 打包
python build_windows.py
```

## 文件清单

打包前确保以下文件存在：

- [x] `app.py` - Flask应用
- [x] `calculate_tokens.py` - 核心逻辑
- [x] `web/` - Web界面
- [x] `tokenizers/` - Tokenizer文件（11个模型）
- [x] `build_windows.py` - 打包脚本
- [x] `requirements.txt` - 依赖列表
- [x] `TokenCalculator.spec` - PyInstaller spec文件

