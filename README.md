# Token计算工具

一个用于计算文本在不同大模型tokenizer下token数量的工具，支持Qwen系列和DeepSeek系列模型。提供Web界面和命令行两种使用方式。

## 功能特性

- 🌐 **Web界面**：简约美观的Web界面，支持文本输入和文件上传
- 📊 **多模型支持**：支持26个主流模型的tokenizer（Qwen2.5、Qwen3和DeepSeek系列）
- 🎨 **高亮显示**：成对的括号和引号使用不同颜色高亮显示
- 📈 **详细结果**：显示token数量、字符/Token比率、分词预览等

## 支持的模型

### Qwen3系列
- qwen3-0.6b, qwen3-1.7b, qwen3-4b, qwen3-8b, qwen3-14b, qwen3-32b, qwen3-30b-a3b

### Qwen2.5系列
- qwen2.5-0.5b, qwen2.5-1.5b, qwen2.5-3b, qwen2.5-7b, qwen2.5-14b, qwen2.5-32b, qwen2.5-72b
- qwen2.5-coder-0.5b, qwen2.5-coder-1.5b, qwen2.5-coder-7b, qwen2.5-coder-32b

### DeepSeek系列
- deepseek-v3, deepseek-v3-base, deepseek-v3.1, deepseek-v3.1-base
- deepseek-chat-1.3b, deepseek-coder-1.3b, deepseek-coder-6.7b, deepseek-coder-33b

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 下载tokenizer

```bash
python download_tokenizers.py
```

### 3. 启动服务

```bash
# Windows
start_server.bat

# Linux/Mac
./start_server.sh

# 或直接运行
python app.py
```

### 4. 访问Web界面

浏览器打开：http://localhost:5001

## 命令行工具

```bash
# 从文件读取
python calculate_tokens.py -f input.txt

# 直接输入文本
python calculate_tokens.py -t "Hello, world! 你好，世界！"

# 指定特定模型
python calculate_tokens.py -t "Hello" --models qwen3-8b deepseek-v3

# 列出所有支持的模型
python calculate_tokens.py --list-models
```

## 项目结构

```
calculate-token/
├── app.py                    # Flask Web应用
├── calculate_tokens.py       # 核心计算逻辑
├── download_tokenizers.py    # Tokenizer下载脚本
├── start_server.bat          # Windows启动脚本
├── start_server.sh           # Linux/Mac启动脚本
├── run.py                    # Python启动脚本
├── web/                      # Web界面文件
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/style.css
│       └── js/main.js
├── tokenizers/               # 下载的tokenizer文件
├── requirements.txt          # Python依赖
└── README.md
```

## 配置选项

可以通过环境变量配置端口和主机：

```bash
# 修改端口
export PORT=8080
python app.py

# 允许外部访问
export HOST=0.0.0.0
python app.py
```

## 技术栈

- **后端**：Flask (Python)
- **前端**：原生HTML/CSS/JavaScript
- **AI模型**：Transformers (HuggingFace)

## 许可证

MIT License
