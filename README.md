# Token计算工具

一个用于计算文本在不同大模型tokenizer下token数量的工具，支持Qwen2.5系列和DeepSeek系列模型。提供命令行工具和Web界面两种使用方式。

## 功能特性

- 🌐 **Web界面**：简约美观的Web界面（openrouter/chat风格），支持文本输入和文件上传
- 📊 **多模型支持**：支持17个主流模型的tokenizer
- 💾 **离线运行**：支持预下载tokenizer，完全离线运行
- 🪟 **Windows打包**：可打包成Windows可执行程序，双击即可运行
- 📈 **详细结果**：显示token数量、字符/Token比率、分词预览等

## 支持的模型

### Qwen3系列（7个模型）
- qwen3-0.6b, qwen3-1.7b, qwen3-4b, qwen3-8b, qwen3-14b, qwen3-32b, qwen3-30b-a3b

### DeepSeek系列（4个模型）
- deepseek-v3, deepseek-v3-base
- deepseek-v3.1, deepseek-v3.1-base

## 安装

### 1. 克隆或下载项目

```bash
git clone <repository-url>
cd calculate-token
```

### 2. 安装依赖

#### 在线安装（有网络连接）

```bash
pip install -r requirements.txt
```

#### 离线安装（无网络连接）

如果Windows机器无法联网，请参考 [OFFLINE_INSTALL.md](OFFLINE_INSTALL.md) 进行离线安装。

**⚠️ 重要提示**：当前 `packages/` 目录中的包是针对Python 3.11的。如果你的Python版本是3.8，请使用 `download_packages_py38.bat` 重新下载。

**快速步骤：**
1. 在有网络的机器上运行 `download_packages.bat`（Python 3.11）或 `download_packages_py38.bat`（Python 3.8）下载所有依赖包
2. 将 `packages/` 目录、`requirements.txt` 和 `install_offline.bat` 复制到离线Windows机器
3. 在Windows机器上运行 `install_offline.bat`

### 3. 下载tokenizer（可选，用于离线运行）

```bash
python download_tokenizers.py
```

这将下载所有17个模型的tokenizer文件到`tokenizers/`目录。首次运行需要网络连接，下载完成后即可离线使用。

## 使用方法

### Web界面（推荐）

#### 开发模式

```bash
python app.py
```

然后在浏览器中访问 `http://localhost:5000`

#### Windows打包版本

1. **打包应用**（在有网络的环境中）：
   ```bash
   python build_windows.py
   ```

2. **复制到Windows机器**：
   - 将 `dist/TokenCalculator` 整个文件夹复制到Windows机器
   - 双击 `start.bat` 启动应用
   - 浏览器会自动打开 `http://localhost:5000`

#### Web界面功能

- **文本输入**：直接在文本框中输入或粘贴文本
- **文件上传**：支持上传文本文件（.txt, .md, .py, .js, .html, .css, .json等）
- **模型选择**：可以选择一个或多个模型进行计算
- **结果展示**：
  - Token数量统计
  - 字符/Token比率
  - 分词结果预览（前100个token）

### 命令行工具

```bash
# 从文件读取
python calculate_tokens.py -f input.txt

# 直接输入文本
python calculate_tokens.py -t "Hello, world! 你好，世界！"

# 指定特定模型
python calculate_tokens.py -t "Hello" --models qwen2.5-7b deepseek-chat-7b

# 从标准输入读取
echo "Hello, world!" | python calculate_tokens.py

# 列出所有支持的模型
python calculate_tokens.py --list-models
```

## 项目结构

```
calculate-token/
├── app.py                    # Flask Web应用
├── calculate_tokens.py        # 核心计算逻辑
├── download_tokenizers.py     # Tokenizer下载脚本
├── build_windows.py           # Windows打包脚本
├── start.bat                  # Windows启动脚本
├── web/                       # Web界面文件
│   ├── templates/
│   │   └── index.html        # 主页面
│   └── static/
│       ├── css/
│       │   └── style.css     # 样式文件
│       └── js/
│           └── main.js       # 前端交互逻辑
├── tokenizers/                # 预下载的tokenizer文件（运行download_tokenizers.py后生成）
├── requirements.txt           # Python依赖
└── README.md                  # 本文件
```

## 打包说明

### ⚠️ 重要提示

**在Mac/Linux上无法直接打包Windows程序**，需要在Windows机器上进行打包。

### Windows打包步骤

#### 准备工作（已在Mac上完成）

- ✅ Python依赖包已下载（`packages/` - 149MB）
- ✅ Tokenizer文件已下载（`tokenizers/` - 268MB，11个模型）

#### 在Windows机器上打包

1. **复制文件到Windows**：
   - 将整个项目文件夹复制到Windows机器

2. **安装Python和依赖**：
   ```cmd
   REM 如果有网络
   pip install -r requirements.txt
   
   REM 如果无网络（离线安装）
   install_offline.bat
   ```

3. **执行打包**：
   ```cmd
   REM 方法1：使用批处理脚本（推荐）
   package_for_windows.bat
   
   REM 方法2：使用Python脚本
   python build_windows.py
   
   REM 方法3：使用spec文件
   pyinstaller TokenCalculator.spec
   ```

4. **测试和分发**：
   - 打包完成后，在 `dist/TokenCalculator/` 目录下会生成可执行文件
   - 双击 `start.bat` 测试运行
   - 将整个 `TokenCalculator` 文件夹压缩后分发

详细说明请参考：
- `WINDOWS_BUILD_README.md` - 快速打包指南
- `build_windows_guide.md` - 详细打包说明
- `DISTRIBUTION.md` - 分发和使用指南

### 打包注意事项

- **文件大小**：完整打包后约500MB-1GB（取决于tokenizer文件大小）
- **离线运行**：打包前必须运行 `download_tokenizers.py` 下载tokenizer，否则无法离线运行
- **首次运行**：如果未下载tokenizer，应用会尝试从网络下载（需要网络连接）

## 技术栈

- **后端**：Flask (Python)
- **前端**：原生HTML/CSS/JavaScript
- **AI模型**：Transformers (HuggingFace)
- **打包工具**：PyInstaller

## 常见问题

### Q: 为什么打包后的文件这么大？

A: 因为包含了：
- Python运行时环境
- Transformers库及其依赖
- 所有17个模型的tokenizer文件
- PyTorch库（如果使用CPU版本会小一些）

### Q: 可以只打包部分模型吗？

A: 可以。修改 `download_tokenizers.py` 中的 `MODELS` 字典，只下载需要的模型，然后重新打包。

### Q: 如何减小打包文件大小？

A: 
1. 只下载需要的模型tokenizer
2. 使用CPU版本的PyTorch（如果不需要GPU）
3. 使用PyInstaller的UPX压缩（需要安装UPX）

### Q: 打包后的应用无法启动？

A: 检查：
1. 是否在Windows系统上运行
2. 是否有杀毒软件拦截
3. 查看错误日志（如果有控制台窗口）

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
