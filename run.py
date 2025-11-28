#!/usr/bin/env python3
"""
简化的启动脚本 - 直接运行Python应用
"""

import os
import sys
from pathlib import Path

# 检查必要的目录
tokenizers_dir = Path(__file__).parent / 'tokenizers'
web_dir = Path(__file__).parent / 'web'

if not tokenizers_dir.exists():
    print("警告: tokenizers目录不存在")
    print("应用将尝试从网络下载tokenizer（需要网络连接）")

if not web_dir.exists():
    print("错误: web目录不存在")
    sys.exit(1)

# 导入并运行Flask应用
if __name__ == '__main__':
    from app import app
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print("=" * 60)
    print("Token计算工具")
    print("=" * 60)
    print(f"启动Flask应用，端口: {port}")
    print(f"访问地址: http://localhost:{port}")
    print("=" * 60)
    print()
    
    try:
        app.run(host='0.0.0.0', port=port, debug=debug)
    except OSError as e:
        if "Address already in use" in str(e) or "address already in use" in str(e):
            print(f"端口 {port} 被占用，尝试使用端口 {port + 1}")
            app.run(host='0.0.0.0', port=port + 1, debug=debug)
        else:
            raise

