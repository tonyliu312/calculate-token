# Windows打包指南

由于在Mac/Linux上无法直接打包Windows可执行程序，需要在Windows机器上进行打包。

## 准备工作

### 1. 在Mac/Linux上准备文件

确保以下文件已准备好：

- ✅ `packages/` - Python依赖包（149MB）
- ✅ `tokenizers/` - Tokenizer文件（273MB）
- ✅ 所有项目源代码文件

### 2. 复制到Windows机器

将整个项目文件夹复制到Windows机器。

## 在Windows机器上打包

### 步骤1：安装Python

1. 下载并安装Python 3.8-3.12
2. 验证安装：打开命令提示符，运行 `python --version`

### 步骤2：安装依赖

#### 方法A：在线安装（如果有网络）

```cmd
pip install -r requirements.txt
```

#### 方法B：离线安装（无网络）

```cmd
install_offline.bat
```

### 步骤3：验证环境

```cmd
python -c "import flask; import transformers; print('环境OK')"
```

### 步骤4：运行打包脚本

```cmd
python build_windows.py
```

或者使用spec文件：

```cmd
pyinstaller TokenCalculator.spec
```

### 步骤5：检查输出

打包完成后，在 `dist/TokenCalculator/` 目录下会生成：

```
TokenCalculator/
├── TokenCalculator.exe    # 主程序
├── start.bat              # 启动脚本
├── web/                    # Web界面文件
├── tokenizers/            # Tokenizer文件
└── [其他依赖文件]
```

### 步骤6：测试

1. 进入 `dist/TokenCalculator/` 目录
2. 双击 `start.bat`
3. 浏览器应自动打开 http://localhost:5000

## 打包参数说明

如果使用 `pyinstaller` 命令直接打包：

```cmd
pyinstaller --name=TokenCalculator ^
    --onedir ^
    --add-data="web;web" ^
    --add-data="tokenizers;tokenizers" ^
    --hidden-import=transformers ^
    --hidden-import=torch ^
    --hidden-import=flask ^
    --hidden-import=calculate_tokens ^
    --collect-all=transformers ^
    --collect-all=torch ^
    --collect-all=tokenizers ^
    app.py
```

## 常见问题

### Q: 打包失败，提示找不到模块？

A: 确保已安装所有依赖：
```cmd
pip install -r requirements.txt
```

### Q: 打包后的应用无法启动？

A: 检查：
1. 是否在Windows系统上运行
2. 是否有杀毒软件拦截
3. 查看控制台错误信息

### Q: 打包后的应用提示找不到tokenizer？

A: 确保：
1. `tokenizers/` 目录存在且包含所有模型
2. 打包时使用了 `--add-data="tokenizers;tokenizers"` 参数

### Q: 文件太大？

A: 可以：
1. 只打包需要的模型（修改 `calculate_tokens.py` 中的 `MODELS` 字典）
2. 使用 `--exclude-module` 排除不需要的模块

## 文件大小参考

- **完整打包**：约500MB-1GB
- **最小配置**（只包含几个常用模型）：约300-500MB

## 分发

打包完成后，将整个 `TokenCalculator` 文件夹：
1. 压缩成zip文件
2. 复制到目标Windows机器
3. 解压后双击 `start.bat` 运行

