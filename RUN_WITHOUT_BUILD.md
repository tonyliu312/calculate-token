# 直接运行Python项目（无需打包）

如果bat脚本有编码问题，可以直接使用Python运行项目，无需打包。

## 快速开始

### 1. 安装Python依赖

**有网络时**：
```cmd
pip install -r requirements.txt
```

**无网络时**（使用离线包）：
```cmd
python -m pip install --upgrade pip --no-index --find-links=packages
python -m pip install -r requirements.txt --no-index --find-links=packages
```

### 2. 运行应用

**方法1：直接运行Python脚本**
```cmd
python app.py
```

**方法2：使用简化的bat脚本**
```cmd
run_app.bat
```

### 3. 访问Web界面

浏览器打开：http://localhost:5000

如果5000端口被占用，应用会自动尝试其他端口，查看控制台输出。

## 文件结构要求

确保项目目录包含：
```
calculate-token/
├── app.py                 # Flask应用
├── calculate_tokens.py    # 核心逻辑
├── web/                   # Web界面
│   ├── templates/
│   └── static/
├── tokenizers/            # Tokenizer文件（必需）
│   ├── qwen3-*/
│   └── deepseek-*/
└── requirements.txt       # 依赖列表
```

## 验证安装

运行以下命令验证环境：

```cmd
python -c "import flask; import transformers; print('OK')"
```

## 常见问题

### Q: 提示找不到模块？

A: 确保已安装依赖：
```cmd
pip install -r requirements.txt
```

### Q: 提示找不到tokenizer？

A: 确保 `tokenizers/` 目录存在且包含模型文件。

### Q: 端口被占用？

A: 可以指定端口：
```cmd
set PORT=5001
python app.py
```

## 优势

- ✅ 无需打包，直接运行
- ✅ 文件更小（不需要Python运行时）
- ✅ 更容易调试和更新
- ✅ 不依赖bat脚本编码

## 与打包版本的对比

| 特性 | 直接运行Python | 打包版本 |
|------|---------------|---------|
| 文件大小 | 小（只需源代码） | 大（500MB-1GB） |
| 需要Python | 是 | 否 |
| 启动速度 | 快 | 较慢 |
| 更新 | 容易 | 需要重新打包 |
| 分发 | 需要Python环境 | 可直接分发 |

## 推荐使用场景

- **开发测试**：直接运行Python
- **生产分发**：打包成exe（如果目标机器没有Python）

