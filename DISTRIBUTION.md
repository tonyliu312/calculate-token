# 分发指南

## 打包好的文件结构

打包完成后，`dist/TokenCalculator/` 目录包含：

```
TokenCalculator/
├── TokenCalculator.exe    # 主程序（必需）
├── start.bat              # 启动脚本（必需）
├── web/                   # Web界面文件（必需）
│   ├── templates/
│   └── static/
├── tokenizers/            # Tokenizer文件（必需）
│   ├── qwen3-*/
│   ├── deepseek-*/
│   └── models_index.json
├── _internal/             # Python运行时和依赖（必需）
└── [其他系统文件]
```

## 分发步骤

### 1. 压缩打包

在Windows机器上，将 `dist/TokenCalculator/` 整个文件夹压缩：

- 使用7-Zip或WinRAR压缩成 `.zip` 或 `.7z` 文件
- 文件名建议：`TokenCalculator-v1.0-windows.zip`

### 2. 文件大小

- **压缩前**：约500MB-1GB
- **压缩后**：约200-400MB（取决于压缩算法）

### 3. 分发方式

- U盘复制
- 网络传输
- 云盘分享

### 4. 在目标Windows机器上使用

1. **解压文件**
   - 解压到任意目录（如 `C:\TokenCalculator\`）

2. **运行应用**
   - 双击 `start.bat`
   - 或直接运行 `TokenCalculator.exe`

3. **访问界面**
   - 浏览器会自动打开 http://localhost:5000
   - 如果没有自动打开，手动访问该地址

## 系统要求

- **操作系统**：Windows 10/11（64位）
- **内存**：建议4GB以上
- **磁盘空间**：至少1GB可用空间
- **网络**：不需要（完全离线运行）

## 注意事项

1. **首次运行**：可能需要几秒钟加载tokenizer
2. **防火墙**：Windows防火墙可能会询问是否允许网络访问，选择"允许"
3. **杀毒软件**：某些杀毒软件可能会误报，需要添加信任
4. **端口占用**：如果5000端口被占用，应用会自动尝试其他端口

## 故障排除

### 问题1：双击start.bat没有反应

**解决**：
1. 右键点击 `start.bat`，选择"以管理员身份运行"
2. 检查是否有错误提示
3. 尝试直接运行 `TokenCalculator.exe`

### 问题2：浏览器无法访问

**解决**：
1. 检查应用是否正在运行（查看任务管理器）
2. 尝试访问 http://127.0.0.1:5000
3. 检查防火墙设置

### 问题3：提示缺少DLL文件

**解决**：
1. 安装 Visual C++ Redistributable
2. 下载地址：https://aka.ms/vs/17/release/vc_redist.x64.exe

### 问题4：应用启动后立即关闭

**解决**：
1. 在命令提示符中运行 `TokenCalculator.exe` 查看错误信息
2. 检查 `tokenizers/` 目录是否完整
3. 检查是否有足够的磁盘空间

## 更新说明

如果需要更新应用：

1. 停止正在运行的应用
2. 替换 `TokenCalculator.exe` 和 `web/` 目录
3. 如果tokenizer有更新，替换 `tokenizers/` 目录
4. 重新启动应用

## 卸载

直接删除整个 `TokenCalculator` 文件夹即可，不会在系统中留下任何痕迹。

