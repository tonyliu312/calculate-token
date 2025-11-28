# 打包说明

本文档详细说明如何将Token计算工具打包成Windows可执行程序。

## 前置要求

1. **Python环境**：Python 3.8+
2. **网络连接**：首次打包需要下载tokenizer文件
3. **Windows系统**：最终打包产物在Windows上运行

## 打包步骤

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 下载Tokenizer（重要！）

在打包前，必须先下载所有tokenizer文件，否则打包后的应用无法离线运行：

```bash
python download_tokenizers.py
```

这个过程可能需要一些时间，因为需要下载17个模型的tokenizer文件。下载完成后，`tokenizers/` 目录会包含所有必要的文件。

### 3. 打包应用

```bash
python build_windows.py
```

打包过程会：
- 使用PyInstaller打包Python应用
- 包含所有依赖库
- 包含web界面文件
- 包含tokenizer文件
- 生成Windows可执行程序

### 4. 打包输出

打包完成后，在 `dist/TokenCalculator/` 目录下会生成：

```
TokenCalculator/
├── TokenCalculator.exe    # 主程序
├── start.bat              # 启动脚本
├── web/                    # Web界面文件
│   ├── templates/
│   └── static/
├── tokenizers/            # Tokenizer文件
└── [其他依赖文件]
```

### 5. 分发和使用

1. 将整个 `TokenCalculator` 文件夹复制到目标Windows机器
2. 双击 `start.bat` 启动应用
3. 浏览器会自动打开 `http://localhost:5000`

## 文件大小说明

完整打包后的文件大小约为：

- **最小配置**（只包含几个常用模型）：约300-500MB
- **完整配置**（包含所有17个模型）：约500MB-1GB

文件大小主要取决于：
- Python运行时环境
- Transformers和PyTorch库
- Tokenizer文件数量

## 优化建议

### 减小文件大小

1. **只下载需要的模型**：
   - 编辑 `download_tokenizers.py`
   - 修改 `MODELS` 字典，只保留需要的模型
   - 重新下载和打包

2. **使用CPU版本的PyTorch**：
   - 如果不需要GPU支持，可以使用CPU版本的PyTorch
   - 在 `requirements.txt` 中指定：`torch==2.0.0+cpu`

3. **使用UPX压缩**（可选）：
   - 安装UPX：https://upx.github.io/
   - 在打包脚本中添加 `--upx-dir` 参数

### 只打包部分模型示例

编辑 `download_tokenizers.py`：

```python
# 只保留常用模型
MODELS = {
    "qwen2.5-7b": "Qwen/Qwen2.5-7B",
    "deepseek-chat-7b": "deepseek-ai/deepseek-chat-7b-v1.5",
    "deepseek-coder-6.7b": "deepseek-ai/deepseek-coder-6.7b-instruct",
}
```

## 常见问题

### Q: 打包失败，提示找不到模块？

A: 确保已安装所有依赖：
```bash
pip install -r requirements.txt
```

### Q: 打包后的应用无法启动？

A: 检查：
1. 是否在Windows系统上运行
2. 是否有杀毒软件拦截
3. 查看是否有错误日志

### Q: 打包后的应用提示找不到tokenizer？

A: 确保在打包前运行了 `download_tokenizers.py`，并且 `tokenizers/` 目录不为空。

### Q: 如何查看打包后的应用日志？

A: 在 `build_windows.py` 中，注释掉 `--windowed` 参数，这样会显示控制台窗口，可以看到日志输出。

## 技术细节

### PyInstaller配置

打包脚本使用以下关键配置：

- `--onedir`：单文件夹模式，便于分发
- `--add-data`：包含web和tokenizers目录
- `--collect-all`：收集所有相关子模块
- `--hidden-import`：确保关键模块被包含

### 路径处理

打包后的应用需要特殊处理路径：

- 使用 `sys.frozen` 检测是否在打包环境中
- 使用 `sys.executable` 获取可执行文件所在目录
- 所有相对路径都基于可执行文件目录

## 测试

打包完成后，建议在干净的Windows环境中测试：

1. 复制到测试机器
2. 确保没有安装Python
3. 双击 `start.bat` 启动
4. 测试所有功能是否正常

