# 快速开始指南

## 开发环境使用

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动Web应用

```bash
python app.py
```

访问 `http://localhost:5000`

### 3. 使用命令行工具

```bash
python calculate_tokens.py -t "Hello, world!"
```

## 打包为Windows应用

### 1. 下载Tokenizer（需要网络）

```bash
python download_tokenizers.py
```

### 2. 打包应用

```bash
python build_windows.py
```

### 3. 分发

将 `dist/TokenCalculator` 文件夹复制到Windows机器，双击 `start.bat` 运行。

## 功能说明

### Web界面

- ✅ 文本输入
- ✅ 文件上传
- ✅ 模型选择（多选）
- ✅ Token数量统计
- ✅ 分词结果预览

### 命令行工具

- ✅ 文件输入
- ✅ 文本输入
- ✅ 标准输入
- ✅ 模型选择
- ✅ 结果表格输出

## 支持的模型

- **Qwen2.5系列**：11个模型
- **DeepSeek系列**：6个模型

详见 `README.md`

