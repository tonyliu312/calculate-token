# Windows打包完整指南

## 📋 当前状态

✅ **所有准备工作已完成**：

- ✅ Python依赖包已下载（`packages/` - 149MB）
- ✅ Tokenizer文件已下载（`tokenizers/` - 268MB，包含11个模型）
- ✅ 打包脚本已创建
- ✅ 所有源代码文件已准备

## ⚠️ 重要提示

**在Mac/Linux上无法直接打包Windows可执行程序**，需要在Windows机器上进行打包。

## 🚀 快速开始（3步）

### 1️⃣ 复制到Windows机器

将整个项目文件夹复制到Windows机器，确保包含：
- `packages/` 目录（149MB）
- `tokenizers/` 目录（268MB）
- 所有 `.py` 文件
- `web/` 目录
- `requirements.txt`
- `build_windows.py`
- `package_for_windows.bat`

### 2️⃣ 在Windows上安装依赖

**有网络时**：
```cmd
pip install -r requirements.txt
```

**无网络时**：
```cmd
install_offline.bat
```

### 3️⃣ 执行打包

**最简单的方式**：
```cmd
package_for_windows.bat
```

或者：
```cmd
python build_windows.py
```

## 📦 打包输出

打包完成后，在 `dist\TokenCalculator\` 目录下会生成：

```
TokenCalculator/
├── TokenCalculator.exe    # 主程序（双击运行）
├── start.bat              # 启动脚本（推荐使用）
├── web/                   # Web界面文件
├── tokenizers/            # Tokenizer文件（11个模型）
└── _internal/             # Python运行时和依赖
```

## ✅ 测试

1. 进入 `dist\TokenCalculator\` 目录
2. 双击 `start.bat`
3. 浏览器会自动打开 http://localhost:5000
4. 测试功能是否正常

## 📤 分发

1. 将 `dist\TokenCalculator\` 文件夹压缩成zip
2. 复制到目标Windows机器
3. 解压后双击 `start.bat` 运行

**文件大小**：
- 打包后：约500MB-1GB
- 压缩后：约200-400MB

## 📚 相关文档

- `WINDOWS_BUILD_README.md` - 快速打包指南
- `build_windows_guide.md` - 详细打包说明
- `DISTRIBUTION.md` - 分发和使用指南
- `BUILD_CHECKLIST.md` - 打包检查清单
- `打包说明.txt` - 中文说明文档

## 🔧 常见问题

### Q: 打包需要多长时间？
A: 通常需要5-15分钟，取决于机器性能。

### Q: 打包后的文件有多大？
A: 约500MB-1GB（包含所有依赖和tokenizer）。

### Q: 可以只打包部分模型吗？
A: 可以，修改 `calculate_tokens.py` 中的 `MODELS` 字典，只保留需要的模型。

### Q: 打包失败怎么办？
A: 检查：
1. Python版本是否正确（3.8-3.12）
2. 依赖是否完整安装
3. tokenizers目录是否完整

## 💡 提示

- 首次打包会需要一些时间，请耐心等待
- 如果只需要常用模型，可以减少tokenizer数量以减小文件大小
- 打包后的应用完全离线运行，不需要网络连接

