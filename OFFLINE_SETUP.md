# 离线环境完整准备指南

本文档提供完整的离线环境准备步骤，确保在无法联网的Windows机器上能够运行Token计算工具。

## 准备工作清单

在**有网络的机器**上完成以下准备工作：

### 1. Python虚拟环境（可选但推荐）

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 升级pip
pip install --upgrade pip setuptools wheel
```

### 2. 下载Python依赖包

#### 方法A：使用脚本（推荐）

**Windows:**
```cmd
download_packages.bat
```

**Linux/Mac:**
```bash
./download_packages.sh
```

#### 方法B：手动下载

```bash
# 下载Python 3.11的包（推荐）
pip download -r requirements.txt -d packages --platform win_amd64 --only-binary=:all: --python-version 3.11

# 如果需要支持多个Python版本，可以下载多个版本
for version in 3.9 3.10 3.11 3.12; do
    pip download -r requirements.txt -d packages --platform win_amd64 --only-binary=:all: --python-version $version --no-deps
done
```

### 3. 下载Tokenizer文件

```bash
python download_tokenizers.py
```

这将下载所有17个模型的tokenizer文件到 `tokenizers/` 目录。

### 4. 验证下载的文件

检查以下目录和文件：

- ✅ `packages/` - 包含所有依赖包（约150-300MB）
- ✅ `tokenizers/` - 包含所有tokenizer文件（约200-500MB）
- ✅ `requirements.txt` - 依赖列表
- ✅ `install_offline.bat` - 离线安装脚本

## 复制到离线Windows机器

将以下内容复制到U盘或其他存储设备：

```
离线安装包/
├── packages/                    # Python依赖包（必需）
│   └── *.whl                    # 所有wheel文件
├── tokenizers/                  # Tokenizer文件（必需）
│   └── [模型目录]/
├── requirements.txt             # 依赖列表（必需）
├── install_offline.bat          # 安装脚本（必需）
├── app.py                       # Flask应用（如果要在源码环境运行）
├── calculate_tokens.py          # 核心逻辑（如果要在源码环境运行）
├── web/                         # Web界面（如果要在源码环境运行）
└── start.bat                    # 启动脚本（如果要在源码环境运行）
```

## 在离线Windows机器上安装

### 步骤1：安装Python（如果未安装）

1. 下载Python 3.8+安装包（从有网络的机器）
2. 在Windows机器上安装Python
3. 验证安装：`python --version`

### 步骤2：安装Python依赖

1. 将 `packages/` 目录、`requirements.txt` 和 `install_offline.bat` 复制到Windows机器
2. 打开命令提示符，进入包含这些文件的目录
3. 运行：
   ```cmd
   install_offline.bat
   ```

### 步骤3：验证安装

```cmd
python -c "import transformers; import torch; import flask; print('安装成功！')"
```

### 步骤4：运行应用

#### 方式A：使用源码运行

1. 将所有项目文件复制到Windows机器
2. 确保 `tokenizers/` 目录存在
3. 运行：
   ```cmd
   python app.py
   ```

#### 方式B：使用打包后的应用

1. 在有网络的机器上打包应用（参考 `PACKAGING.md`）
2. 将打包后的 `TokenCalculator` 文件夹复制到Windows机器
3. 双击 `start.bat` 运行

## 文件大小参考

| 项目 | 大小 | 说明 |
|------|------|------|
| packages/ | 150-300MB | Python依赖包 |
| tokenizers/ | 200-500MB | Tokenizer文件 |
| Python安装包 | 30-50MB | Python 3.11安装程序 |
| 打包后的应用 | 500MB-1GB | 完整可执行程序 |
| **总计** | **约1-2GB** | 完整离线环境 |

## 常见问题排查

### 问题1：安装依赖时提示找不到包

**原因：** Python版本不匹配

**解决：**
1. 检查Python版本：`python --version`
2. 重新下载对应版本的包
3. 或使用 `--no-binary=:all:` 下载源码包

### 问题2：某些包安装失败

**原因：** 缺少编译工具或依赖

**解决：**
1. 确保下载的是Windows wheel文件（.whl）
2. 检查是否有对应的Python版本包
3. 尝试手动安装失败的包

### 问题3：运行时提示找不到模块

**原因：** 依赖未正确安装

**解决：**
1. 重新运行 `install_offline.bat`
2. 检查虚拟环境是否激活（如果使用）
3. 验证安装：`pip list`

### 问题4：Tokenizer加载失败

**原因：** tokenizer文件缺失或路径错误

**解决：**
1. 确保 `tokenizers/` 目录存在且包含所有模型
2. 检查目录结构是否正确
3. 运行 `python download_tokenizers.py` 重新下载

## 完整工作流程总结

### 在有网络的机器上：

1. ✅ 创建虚拟环境（可选）
2. ✅ 运行 `download_packages.bat` 下载依赖包
3. ✅ 运行 `download_tokenizers.py` 下载tokenizer
4. ✅ 验证所有文件存在
5. ✅ 复制到存储设备

### 在离线Windows机器上：

1. ✅ 安装Python（如需要）
2. ✅ 运行 `install_offline.bat` 安装依赖
3. ✅ 验证安装
4. ✅ 运行应用或使用打包版本

## 快速检查清单

在开始之前，确认：

- [ ] 有网络的机器已准备好
- [ ] Python 3.8+ 已安装（在有网络的机器上）
- [ ] 有足够的存储空间（至少2GB）
- [ ] 有U盘或其他存储设备
- [ ] Windows机器已准备好（或知道如何准备）

## 技术支持

如遇到问题，请检查：

1. `OFFLINE_INSTALL.md` - 详细安装说明
2. `PACKAGING.md` - 打包说明
3. `README.md` - 项目文档

