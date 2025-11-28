# 部署指南 - Web服务模式

## 🚀 快速启动

### Windows

```cmd
python app.py
```

或使用启动脚本：
```cmd
start_server.bat
```

### Linux/Mac

```bash
python3 app.py
```

或使用启动脚本：
```bash
./start_server.sh
```

## 🌐 访问服务

启动后，可以通过以下方式访问：

- **本地访问**: http://localhost:5001
- **局域网访问**: http://<服务器IP>:5001
- **外网访问**: http://<公网IP>:5001（需要配置防火墙和端口转发）

## ⚙️ 配置选项

### 环境变量

可以通过环境变量配置服务：

```cmd
REM Windows
set PORT=8080
set HOST=0.0.0.0
set DEBUG=true
python app.py
```

```bash
# Linux/Mac
export PORT=8080
export HOST=0.0.0.0
export DEBUG=true
python3 app.py
```

### 参数说明

- `PORT`: 服务端口（默认: 5001）
- `HOST`: 监听地址（默认: 0.0.0.0，允许外部访问）
- `DEBUG`: 调试模式（默认: false）

## 🔧 部署到生产环境

### 使用 Gunicorn (Linux/Mac)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 使用 Waitress (Windows)

```cmd
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

### 使用 systemd (Linux)

创建服务文件 `/etc/systemd/system/token-calculator.service`:

```ini
[Unit]
Description=Token Calculator Web Service
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/calculate-token
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl enable token-calculator
sudo systemctl start token-calculator
```

## 🔒 安全建议

### 1. 防火墙配置

**Windows防火墙**：
```cmd
netsh advfirewall firewall add rule name="Token Calculator" dir=in action=allow protocol=TCP localport=5000
```

**Linux (ufw)**：
```bash
sudo ufw allow 5000/tcp
```

### 2. 反向代理（推荐）

使用 Nginx 作为反向代理：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. HTTPS配置

使用 Let's Encrypt 获取SSL证书：

```bash
sudo certbot --nginx -d your-domain.com
```

## 📊 性能优化

### 1. 多进程部署

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 2. 使用缓存

可以添加Redis缓存tokenizer加载结果。

### 3. 负载均衡

使用Nginx进行负载均衡：

```nginx
upstream token_calculator {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}
```

## 🐳 Docker部署（可选）

创建 `Dockerfile`:

```dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
```

构建和运行：
```bash
docker build -t token-calculator .
docker run -p 5000:5000 token-calculator
```

## 📝 注意事项

1. **端口占用**: 如果5000端口被占用，设置 `PORT` 环境变量使用其他端口
2. **防火墙**: 确保防火墙允许访问服务端口
3. **tokenizer加载**: 首次启动需要加载tokenizer，可能需要一些时间
4. **内存使用**: 加载多个tokenizer会占用一定内存

## 🔍 故障排查

### 问题1：无法从外部访问

**解决**：
- 检查 `HOST` 是否设置为 `0.0.0.0`
- 检查防火墙设置
- 检查路由器端口转发

### 问题2：端口被占用

**解决**：
```cmd
REM Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### 问题3：服务启动慢

**解决**：
- 首次启动需要加载tokenizer，这是正常的
- 后续启动会快一些

