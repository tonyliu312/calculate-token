# Windows打包快速指南

## ⚠️ 重要说明

**在Mac/Linux上无法直接打包Windows可执行程序**，需要在Windows机器上进行打包。

## 📦 已准备好的文件

所有必要的文件已准备完成：

- ✅ **Python依赖包** (`packages/`): 149MB - 已下载Windows平台的包
- ✅ **Tokenizer文件** (`tokenizers/`): 273MB - 11个模型已下载
- ✅ **源代码文件**: 所有Python和Web文件
- ✅ **打包脚本**: `build_windows.py` 和 `package_for_windows.bat`
- ✅ **PyInstaller配置**: `TokenCalculator.spec`

## 🚀 在Windows机器上打包（3步）

### 步骤1：复制文件到Windows

将整个项目文件夹复制到Windows机器，确保包含：
- `packages/` 目录
- `tokenizers/` 目录
- 所有 `.py` 文件
- `web/` 目录
- `requirements.txt`

### 步骤2：安装Python和依赖

#### 如果有网络：

```cmd
REM 安装Python 3.8-3.12（如果未安装）

REM 安装依赖
pip install -r requirements.txt
```

#### 如果无网络（离线安装）：

```cmd
REM 运行离线安装脚本
install_offline.bat
```

### 步骤3：执行打包

**方法A：使用批处理脚本（推荐）**

```cmd
package_for_windows.bat
```

**方法B：使用Python脚本**

```cmd
python build_windows.py
```

**方法C：使用spec文件**

```cmd
pyinstaller TokenCalculator.spec
```

## 📁 打包输出

打包完成后，在 `dist/TokenCalculator/` 目录下会生成：

```
TokenCalculator/
├── TokenCalculator.exe    # 主程序
├── start.bat              # 启动脚本（双击运行）
├── web/                   # Web界面
├── tokenizers/            # Tokenizer文件
└── _internal/             # Python运行时
```

## ✅ 测试打包结果

1. 进入 `dist/TokenCalculator/` 目录
2. 双击 `start.bat`
3. 浏览器应自动打开 http://localhost:5000
4. 测试token计算功能

## 📤 分发

1. 将 `dist/TokenCalculator/` 整个文件夹压缩成zip
2. 复制到目标Windows机器
3. 解压后双击 `start.bat` 运行

## 📋 文件大小

- **打包后文件夹**: 约500MB-1GB
- **压缩后**: 约200-400MB

## 🔧 故障排除

### 打包失败？

1. 检查Python版本：`python --version`（需要3.8-3.12）
2. 检查依赖：`pip list | findstr "flask transformers"`
3. 检查tokenizers目录：`dir tokenizers`

### 打包后的应用无法运行？

1. 查看控制台错误信息
2. 检查 `tokenizers/` 目录是否完整
3. 检查是否有杀毒软件拦截

## 📚 详细文档

- `build_windows_guide.md` - 详细打包指南
- `DISTRIBUTION.md` - 分发和使用说明
- `BUILD_CHECKLIST.md` - 打包检查清单

## 💡 提示

- 打包过程可能需要5-15分钟，请耐心等待
- 首次打包会下载一些额外的依赖，需要网络连接
- 如果只需要部分模型，可以修改 `calculate_tokens.py` 中的 `MODELS` 字典

