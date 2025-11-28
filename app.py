#!/usr/bin/env python3
"""
Flask Web应用 - Token计算工具
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# 导入核心逻辑
from calculate_tokens import TokenCalculator, MODELS

# 设置模板和静态文件路径
# 在打包后的环境中，需要根据实际情况调整路径
if getattr(sys, 'frozen', False):
    # PyInstaller打包后的环境
    base_path = Path(sys.executable).parent
    template_dir = base_path / 'web' / 'templates'
    static_dir = base_path / 'web' / 'static'
else:
    # 开发环境
    base_path = Path(__file__).parent
    template_dir = base_path / 'web' / 'templates'
    static_dir = base_path / 'web' / 'static'

app = Flask(__name__, template_folder=str(template_dir), static_folder=str(static_dir))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = Path(__file__).parent / 'uploads'

# 确保上传目录存在
app.config['UPLOAD_FOLDER'].mkdir(exist_ok=True)

# 全局tokenizer计算器（延迟加载）
_calculator = None


def get_calculator():
    """获取或创建TokenCalculator实例（单例模式）"""
    global _calculator
    if _calculator is None:
        # 检查是否有本地tokenizer
        # 在打包后的环境中，__file__可能指向临时目录，需要使用sys.executable的目录
        if getattr(sys, 'frozen', False):
            # PyInstaller打包后的环境
            base_path = Path(sys.executable).parent
        else:
            # 开发环境
            base_path = Path(__file__).parent
        
        tokenizers_dir = base_path / 'tokenizers'
        local_mode = tokenizers_dir.exists() and any(tokenizers_dir.iterdir())
        
        if local_mode:
            print("使用本地tokenizer模式")
            _calculator = TokenCalculator(local_mode=True, tokenizers_dir=str(tokenizers_dir))
        else:
            print("使用在线tokenizer模式（需要网络连接）")
            _calculator = TokenCalculator(local_mode=False)
    
    return _calculator


@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')


@app.route('/api/models', methods=['GET'])
def get_models():
    """获取可用模型列表"""
    calculator = get_calculator()
    available_models = list(calculator.tokenizers.keys())
    
    models_info = []
    for model_key in available_models:
        models_info.append({
            'key': model_key,
            'name': MODELS.get(model_key, model_key),
            'available': True
        })
    
    # 添加未加载的模型
    for model_key in MODELS.keys():
        if model_key not in available_models:
            models_info.append({
                'key': model_key,
                'name': MODELS[model_key],
                'available': False
            })
    
    return jsonify({
        'success': True,
        'models': sorted(models_info, key=lambda x: x['key'])
    })


@app.route('/api/calculate', methods=['POST'])
def calculate_tokens():
    """计算token数量"""
    try:
        # 获取文本输入
        text = None
        
        # 检查是否有文件上传
        if 'file' in request.files:
            file = request.files['file']
            if file.filename:
                filename = secure_filename(file.filename)
                filepath = app.config['UPLOAD_FOLDER'] / filename
                file.save(str(filepath))
                
                # 读取文件内容
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        text = f.read()
                except UnicodeDecodeError:
                    # 尝试其他编码
                    try:
                        with open(filepath, 'r', encoding='gbk') as f:
                            text = f.read()
                    except:
                        return jsonify({
                            'success': False,
                            'error': '无法读取文件，请确保文件是UTF-8或GBK编码的文本文件'
                        }), 400
                finally:
                    # 删除临时文件
                    if filepath.exists():
                        filepath.unlink()
        
        # 如果没有文件，从表单获取文本
        if not text:
            text = request.form.get('text', '')
            if not text:
                # 尝试从JSON获取
                data = request.get_json()
                if data:
                    text = data.get('text', '')
        
        if not text:
            return jsonify({
                'success': False,
                'error': '请提供文本或上传文件'
            }), 400
        
        # 获取选中的模型
        selected_models = request.form.getlist('models')
        if not selected_models:
            # 尝试从JSON获取
            data = request.get_json()
            if data:
                selected_models = data.get('models', [])
        
        # 获取计算器
        calculator = get_calculator()
        
        # 如果指定了模型，只使用选中的模型
        if selected_models:
            # 过滤出可用的模型
            available_models = [m for m in selected_models if m in calculator.tokenizers]
            if not available_models:
                return jsonify({
                    'success': False,
                    'error': '所选模型都不可用'
                }), 400
            calculator.models = available_models
            # 重新加载指定的tokenizers
            calculator.tokenizers = {k: v for k, v in calculator.tokenizers.items() if k in available_models}
        
        # 计算tokens
        results = calculator.calculate_tokens(text)
        
        # 获取分词结果（前100个token作为预览）
        token_details = {}
        for model_key in results.keys():
            if results[model_key] >= 0:
                token_ids = calculator.get_token_ids(text, model_key)
                # 只取前100个token作为预览
                preview_ids = token_ids[:100]
                tokens = calculator.decode_tokens(preview_ids, model_key)
                token_details[model_key] = {
                    'total_tokens': len(token_ids),
                    'preview_tokens': tokens,
                    'preview_count': len(preview_ids)
                }
        
        # 构建响应
        response_data = {
            'success': True,
            'text_length': len(text),
            'text_preview': text[:200] + ('...' if len(text) > 200 else ''),
            'results': []
        }
        
        for model_key in sorted(results.keys()):
            token_count = results[model_key]
            if token_count >= 0:
                ratio = len(text) / token_count if token_count > 0 else 0
                details = token_details.get(model_key, {})
                response_data['results'].append({
                    'model': model_key,
                    'model_name': MODELS.get(model_key, model_key),
                    'token_count': token_count,
                    'char_per_token': round(ratio, 2),
                    'token_preview': details.get('preview_tokens', []),
                    'preview_count': details.get('preview_count', 0)
                })
        
        return jsonify(response_data)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'处理请求时出错: {str(e)}'
        }), 500


if __name__ == '__main__':
    # 启动Web服务
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    host = os.environ.get('HOST', '0.0.0.0')  # 0.0.0.0 允许外部访问
    
    print("=" * 60)
    print("Token计算工具 - Web服务")
    print("=" * 60)
    print(f"服务地址: http://{host}:{port}")
    print(f"本地访问: http://localhost:{port}")
    print(f"局域网访问: http://<本机IP>:{port}")
    print("=" * 60)
    print("按 Ctrl+C 停止服务")
    print("=" * 60)
    print()
    
    app.run(host=host, port=port, debug=debug)

