# 离线安装指南

本文档说明如何在无法联网的Windows机器上安装Python依赖包。

## 准备工作（在有网络的机器上）

### 1. 下载依赖包

在**有网络的机器**上（可以是Mac/Linux/Windows），运行以下命令下载所有Windows平台的依赖包：

```bash
# 创建packages目录
mkdir -p packages

# 下载所有依赖包（Windows平台）
pip download -r requirements.txt -d packages --platform win_amd64 --only-binary=:all: --python-version 3.11

# 如果Python版本不同，请调整--python-version参数
# 例如：--python-version 3.10 或 --python-version 3.9
```

### 2. 检查下载的包

下载完成后，`packages/` 目录应包含所有依赖包的 `.whl` 文件，例如：

```
packages/
├── transformers-4.57.3-py3-none-any.whl
├── torch-2.9.1-cp311-cp311-win_amd64.whl
├── flask-3.1.2-py3-none-any.whl
├── huggingface_hub-0.36.0-py3-none-any.whl
├── pyinstaller-6.17.0-py3-none-win_amd64.whl
└── ... (其他依赖包)
```

### 3. 复制到离线机器

将以下内容复制到U盘或其他存储设备：

- `packages/` 目录（所有依赖包）
- `requirements.txt` 文件
- `install_offline.bat` 文件（Windows安装脚本）

## 在离线Windows机器上安装

### 方法1：使用安装脚本（推荐）

1. 将 `packages/` 目录、`requirements.txt` 和 `install_offline.bat` 复制到Windows机器
2. 确保Python已安装（Python 3.8+）
3. 双击运行 `install_offline.bat`
4. 等待安装完成

### 方法2：手动安装

1. 打开命令提示符（CMD）或PowerShell
2. 进入包含 `packages/` 目录的文件夹
3. 运行以下命令：

```cmd
REM 升级pip
python -m pip install --upgrade pip --no-index --find-links=packages

REM 安装所有依赖
python -m pip install -r requirements.txt --no-index --find-links=packages
```

## Python版本兼容性

### 支持的Python版本

- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12

### 下载不同Python版本的包

如果目标机器使用不同版本的Python，需要下载对应版本的包：

```bash
# Python 3.10
pip download -r requirements.txt -d packages --platform win_amd64 --only-binary=:all: --python-version 3.10

# Python 3.9
pip download -r requirements.txt -d packages --platform win_amd64 --only-binary=:all: --python-version 3.9
```

### 下载多个Python版本（推荐）

为了兼容性，可以下载多个Python版本的包：

```bash
# 下载Python 3.9, 3.10, 3.11的包
for version in 3.9 3.10 3.11; do
    pip download -r requirements.txt -d packages --platform win_amd64 --only-binary=:all: --python-version $version
done
```

## 验证安装

安装完成后，验证是否安装成功：

```cmd
python -c "import transformers; import torch; import flask; print('所有依赖安装成功！')"
```

## 常见问题

### Q: 提示找不到某个包？

A: 可能的原因：
1. 下载的包版本与Python版本不匹配
2. 某些包没有Windows wheel文件，需要下载源码包

解决方案：
```bash
# 同时下载wheel和源码包
pip download -r requirements.txt -d packages --platform win_amd64 --no-binary=:all: --python-version 3.11
```

### Q: 安装时提示版本冲突？

A: 检查 `requirements.txt` 中的版本要求，可能需要调整版本范围。

### Q: 某些包安装失败？

A: 尝试：
1. 使用 `--no-deps` 参数跳过依赖检查（不推荐）
2. 手动安装失败的包
3. 检查Python版本是否兼容

## 完整离线环境准备清单

在打包应用前，确保准备好：

- [ ] Python 3.8+ 安装包（如果需要）
- [ ] 所有依赖包的wheel文件（`packages/` 目录）
- [ ] `requirements.txt` 文件
- [ ] `install_offline.bat` 安装脚本
- [ ] Tokenizer文件（运行 `download_tokenizers.py` 后生成）

## 文件大小估算

- **packages目录**：约200-300MB（包含所有依赖包）
- **tokenizers目录**：约200-500MB（17个模型的tokenizer）
- **Python安装包**：约30-50MB（如果需要）

总计：约500MB-1GB

