#!/usr/bin/env python3
"""
Flask Web应用 - Token计算工具
"""

import os
import sys
import threading
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
_calculator_lock = threading.Lock()  # 添加锁防止并发问题


def get_calculator():
    """获取或创建TokenCalculator实例（单例模式，线程安全）"""
    global _calculator
    with _calculator_lock:
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
        
        # 验证tokenizers字典完整性
        if _calculator:
            tokenizer_count = len(_calculator.tokenizers)
            if tokenizer_count == 0:
                print("错误: tokenizers字典为空！")
            elif tokenizer_count < len(MODELS):
                print(f"警告: 只加载了 {tokenizer_count}/{len(MODELS)} 个tokenizer")
        
        return _calculator


@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')


@app.route('/api/models', methods=['GET'])
def get_models():
    """获取可用模型列表"""
    try:
        calculator = get_calculator()
        
        if calculator is None:
            return jsonify({
                'success': False,
                'error': 'TokenCalculator未初始化'
            }), 500
        
        # 验证tokenizers字典完整性
        if not calculator.tokenizers:
            return jsonify({
                'success': False,
                'error': '没有可用的tokenizer，请检查tokenizers目录或重启服务'
            }), 500
        
        available_models = list(calculator.tokenizers.keys())
        
        # 记录当前加载的模型数量（用于调试）
        print(f"[API] /api/models - 当前加载的模型数量: {len(available_models)}")
        if len(available_models) < len(MODELS):
            print(f"[API] 警告: 期望 {len(MODELS)} 个模型，实际加载 {len(available_models)} 个")
            print(f"[API] 已加载的模型: {sorted(available_models)}")
        
        models_info = []
        for model_key in available_models:
            # 获取模型显示名称（优先从MODELS字典，否则使用key）
            model_name = MODELS.get(model_key, model_key)
            models_info.append({
                'key': model_key,
                'name': model_name,
                'available': True
            })
        
        # 如果使用本地模式，只显示已加载的模型
        # 如果使用在线模式，显示所有MODELS中的模型（包括未加载的）
        if not calculator.local_mode:
            for model_key in MODELS.keys():
                if model_key not in available_models:
                    models_info.append({
                        'key': model_key,
                        'name': MODELS[model_key],
                        'available': False
                    })
        
        # 计算总模型数（本地模式使用实际加载数，在线模式使用MODELS字典）
        total_count = len(available_models) if calculator.local_mode else len(MODELS)
        
        return jsonify({
            'success': True,
            'models': sorted(models_info, key=lambda x: x['key']),
            'loaded_count': len(available_models),
            'total_count': total_count,
            'local_mode': calculator.local_mode
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'获取模型列表时出错: {str(e)}'
        }), 500


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
        
        # 获取计算器（使用锁保护）
        calculator = get_calculator()
        if calculator is None:
            return jsonify({
                'success': False,
                'error': 'TokenCalculator未初始化'
            }), 500
        
        # 验证tokenizers字典完整性
        if not calculator.tokenizers:
            return jsonify({
                'success': False,
                'error': '没有可用的tokenizer，请重启服务'
            }), 500
        
        # 如果指定了模型，只使用选中的模型（不修改全局tokenizers字典）
        models_to_use = None
        if selected_models:
            # 过滤出可用的模型
            available_models = [m for m in selected_models if m in calculator.tokenizers]
            if not available_models:
                return jsonify({
                    'success': False,
                    'error': '所选模型都不可用'
                }), 400
            models_to_use = available_models
            print(f"[API] /api/calculate - 使用选中的模型: {models_to_use}")
        
        # 计算tokens（如果指定了模型，只计算选中的模型，但不修改全局字典）
        if models_to_use:
            # 使用临时字典进行计算，不修改全局tokenizers
            temp_tokenizers = {k: v for k, v in calculator.tokenizers.items() if k in models_to_use}
            results = {}
            for model_key, tokenizer in temp_tokenizers.items():
                try:
                    tokens = tokenizer.encode(text, add_special_tokens=False)
                    results[model_key] = len(tokens)
                except Exception as e:
                    print(f"警告: 计算 {model_key} 的tokens时出错: {e}")
                    results[model_key] = -1
        else:
            # 使用所有模型
            results = calculator.calculate_tokens(text)
        
        # 获取分词结果（前100个token作为预览）
        token_details = {}
        for model_key in results.keys():
            if results[model_key] >= 0:
                try:
                    token_ids = calculator.get_token_ids(text, model_key)
                    # 只取前100个token作为预览
                    preview_ids = token_ids[:100]
                    tokens = calculator.decode_tokens(preview_ids, model_key)
                    token_details[model_key] = {
                        'total_tokens': len(token_ids),
                        'preview_tokens': tokens,
                        'preview_count': len(preview_ids)
                    }
                except Exception as e:
                    print(f"警告: 获取 {model_key} 的分词详情时出错: {e}")
                    token_details[model_key] = {
                        'total_tokens': results[model_key],
                        'preview_tokens': [],
                        'preview_count': 0
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
                # 获取模型显示名称（优先从MODELS字典，否则使用key）
                model_name = MODELS.get(model_key, model_key)
                response_data['results'].append({
                    'model': model_key,
                    'model_name': model_name,
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


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    try:
        calculator = get_calculator()
        if calculator is None:
            return jsonify({
                'status': 'error',
                'message': 'TokenCalculator未初始化'
            }), 500
        
        tokenizer_count = len(calculator.tokenizers)
        
        # 本地模式：期望数量等于实际发现的模型数
        # 在线模式：期望数量等于MODELS字典中的数量
        if calculator.local_mode:
            expected_count = len(calculator.available_models)
            missing_models = sorted([m for m in calculator.available_models if m not in calculator.tokenizers])
        else:
            expected_count = len(MODELS)
            missing_models = sorted([m for m in MODELS.keys() if m not in calculator.tokenizers])
        
        status = 'healthy' if tokenizer_count == expected_count else 'degraded'
        
        return jsonify({
            'status': status,
            'tokenizer_count': tokenizer_count,
            'expected_count': expected_count,
            'loaded_models': sorted(list(calculator.tokenizers.keys())),
            'missing_models': missing_models,
            'local_mode': calculator.local_mode
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
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
