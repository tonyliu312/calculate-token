#!/usr/bin/env python3
"""
Token计算工具 - 支持Qwen3系列和DeepSeek系列模型
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional

# 延迟导入transformers，以便在显示帮助信息时不需要安装
try:
    from transformers import AutoTokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False


# 支持的模型列表
MODELS = {
    # Qwen3系列（实际可用的模型）
    "qwen3-0.6b": "Qwen/Qwen3-0.6B",
    "qwen3-1.7b": "Qwen/Qwen3-1.7B",
    "qwen3-4b": "Qwen/Qwen3-4B",
    "qwen3-8b": "Qwen/Qwen3-8B",
    "qwen3-14b": "Qwen/Qwen3-14B",
    "qwen3-32b": "Qwen/Qwen3-32B",
    "qwen3-30b-a3b": "Qwen/Qwen3-30B-A3B",
    # DeepSeek系列 - V3, V3.1
    "deepseek-v3": "deepseek-ai/DeepSeek-V3",
    "deepseek-v3-base": "deepseek-ai/DeepSeek-V3-Base",
    "deepseek-v3.1": "deepseek-ai/DeepSeek-V3.1",
    "deepseek-v3.1-base": "deepseek-ai/DeepSeek-V3.1-Base",
    # 注意：DeepSeek-671B在HuggingFace上不存在，已移除
}


class TokenCalculator:
    """Token计算器"""
    
    def __init__(self, models: Optional[List[str]] = None, local_mode: bool = False, tokenizers_dir: Optional[str] = None):
        """
        初始化Token计算器
        
        Args:
            models: 要使用的模型列表，如果为None则使用所有模型
            local_mode: 是否使用本地模式（从本地文件系统加载）
            tokenizers_dir: 本地tokenizer目录路径（local_mode=True时使用）
        """
        self.local_mode = local_mode
        self.tokenizers_dir = Path(tokenizers_dir) if tokenizers_dir else Path(__file__).parent / "tokenizers"
        
        # 如果是本地模式，自动扫描tokenizers目录
        if local_mode:
            self.available_models = self._scan_tokenizers_dir()
        else:
            # 在线模式，使用MODELS字典
            self.available_models = list(MODELS.keys())
        
        # 如果指定了models，只使用指定的模型
        if models:
            self.models = [m for m in models if m in self.available_models]
        else:
            self.models = self.available_models
        
        self.tokenizers: Dict[str, any] = {}
        self._load_tokenizers()
    
    def _scan_tokenizers_dir(self) -> List[str]:
        """
        扫描tokenizers目录，自动发现所有可用的模型
        
        Returns:
            模型键名列表
        """
        models = []
        
        if not self.tokenizers_dir.exists():
            print(f"警告: tokenizers目录不存在: {self.tokenizers_dir}")
            return models
        
        # 扫描目录，查找所有子目录（每个子目录代表一个模型）
        print(f"扫描tokenizers目录: {self.tokenizers_dir}")
        scanned_models = []
        for item in self.tokenizers_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                # 检查是否是有效的tokenizer目录（包含tokenizer.json或tokenizer_config.json）
                tokenizer_json = item / "tokenizer.json"
                tokenizer_config = item / "tokenizer_config.json"
                if tokenizer_json.exists() or tokenizer_config.exists():
                    scanned_models.append(item.name)
        
        if scanned_models:
            print(f"从目录扫描发现 {len(scanned_models)} 个模型")
            models = sorted(scanned_models)
        else:
            print(f"警告: 在 {self.tokenizers_dir} 中未发现任何模型")
            # 如果目录扫描失败，尝试读取models_index.json作为备选
            index_file = self.tokenizers_dir / "models_index.json"
            if index_file.exists():
                try:
                    import json
                    with open(index_file, 'r', encoding='utf-8') as f:
                        index_data = json.load(f)
                        models = list(index_data.keys())
                        print(f"从 models_index.json 读取到 {len(models)} 个模型（备选方案）")
                except Exception as e:
                    print(f"警告: 读取 models_index.json 也失败: {e}")
        
        return models
    
    def _load_tokenizers(self):
        """加载所有需要的tokenizer"""
        if not TRANSFORMERS_AVAILABLE:
            print("错误: 请先安装transformers库")
            print("运行: pip install transformers")
            sys.exit(1)
        
        print(f"正在加载 {len(self.models)} 个tokenizers...")
        for model_key in self.models:
            try:
                if self.local_mode:
                    # 从本地加载
                    local_path = self.tokenizers_dir / model_key
                    if not local_path.exists():
                        print(f"  警告: 本地tokenizer不存在: {local_path}，跳过")
                        continue
                    print(f"  加载 {model_key} (本地: {local_path})...")
                    self.tokenizers[model_key] = AutoTokenizer.from_pretrained(
                        str(local_path),
                        trust_remote_code=True,
                        local_files_only=True
                    )
                else:
                    # 从HuggingFace Hub加载（需要MODELS字典）
                    if model_key not in MODELS:
                        print(f"  警告: 未知的模型 '{model_key}'，跳过")
                        continue
                    model_name = MODELS[model_key]
                    print(f"  加载 {model_key} ({model_name})...")
                    self.tokenizers[model_key] = AutoTokenizer.from_pretrained(
                        model_name,
                        trust_remote_code=True
                    )
            except Exception as e:
                print(f"  错误: 无法加载 {model_key}: {e}")
        
        if not self.tokenizers:
            print("错误: 没有成功加载任何tokenizer")
            sys.exit(1)
        
        print(f"成功加载 {len(self.tokenizers)} 个tokenizer\n")
    
    def calculate_tokens(self, text: str) -> Dict[str, int]:
        """
        计算文本的token数量
        
        Args:
            text: 输入文本
            
        Returns:
            字典，键为模型名，值为token数量
        """
        results = {}
        for model_key, tokenizer in self.tokenizers.items():
            try:
                tokens = tokenizer.encode(text, add_special_tokens=False)
                results[model_key] = len(tokens)
            except Exception as e:
                print(f"警告: 计算 {model_key} 的tokens时出错: {e}")
                results[model_key] = -1
        
        return results
    
    def get_token_ids(self, text: str, model_key: str) -> List[int]:
        """
        获取指定模型的分词结果（token IDs）
        
        Args:
            text: 输入文本
            model_key: 模型键名
            
        Returns:
            token ID列表
        """
        if model_key not in self.tokenizers:
            return []
        try:
            return self.tokenizers[model_key].encode(text, add_special_tokens=False)
        except Exception as e:
            print(f"警告: 获取 {model_key} 的token IDs时出错: {e}")
            return []
    
    def decode_tokens(self, token_ids: List[int], model_key: str) -> List[str]:
        """
        将token IDs解码为token字符串列表
        
        Args:
            token_ids: token ID列表
            model_key: 模型键名
            
        Returns:
            token字符串列表
        """
        if model_key not in self.tokenizers:
            return []
        try:
            tokenizer = self.tokenizers[model_key]
            tokens = []
            for token_id in token_ids:
                token_str = tokenizer.decode([token_id], skip_special_tokens=False)
                tokens.append(token_str)
            return tokens
        except Exception as e:
            print(f"警告: 解码 {model_key} 的tokens时出错: {e}")
            return []
    
    def print_results(self, text: str, results: Dict[str, int]):
        """
        打印结果
        
        Args:
            text: 原始文本
            results: token计算结果
        """
        print("=" * 80)
        print("Token计算结果")
        print("=" * 80)
        print(f"\n输入文本长度: {len(text)} 字符")
        print(f"输入文本预览: {text[:100]}{'...' if len(text) > 100 else ''}\n")
        print("-" * 80)
        print(f"{'模型':<30} {'Token数量':<15} {'字符/Token':<15}")
        print("-" * 80)
        
        for model_key in sorted(results.keys()):
            token_count = results[model_key]
            if token_count >= 0:
                ratio = len(text) / token_count if token_count > 0 else 0
                print(f"{model_key:<30} {token_count:<15} {ratio:.2f}")
            else:
                print(f"{model_key:<30} {'错误':<15}")
        
        print("-" * 80)
        print(f"\n平均Token数量: {sum(v for v in results.values() if v >= 0) / len([v for v in results.values() if v >= 0]):.1f}")
        print("=" * 80)


def read_text_from_file(file_path: str) -> str:
    """
    从文件读取文本
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件内容
    """
    path = Path(file_path)
    if not path.exists():
        print(f"错误: 文件不存在: {file_path}")
        sys.exit(1)
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"错误: 无法读取文件 {file_path}: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="计算文本在不同大模型tokenizer下的token数量",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从文件读取
  python calculate_tokens.py -f input.txt
  
  # 直接输入文本
  python calculate_tokens.py -t "Hello, world!"
  
  # 指定特定模型
  python calculate_tokens.py -t "Hello" --models qwen2.5-7b deepseek-chat-7b
  
  # 从标准输入读取
  echo "Hello" | python calculate_tokens.py
        """
    )
    
    parser.add_argument(
        '-f', '--file',
        type=str,
        help='输入文件路径'
    )
    
    parser.add_argument(
        '-t', '--text',
        type=str,
        help='直接输入文本'
    )
    
    parser.add_argument(
        '--models',
        nargs='+',
        choices=list(MODELS.keys()),
        help='指定要使用的模型（可选，默认使用所有模型）'
    )
    
    parser.add_argument(
        '--list-models',
        action='store_true',
        help='列出所有支持的模型'
    )
    
    args = parser.parse_args()
    
    # 列出所有模型
    if args.list_models:
        print("支持的模型列表:")
        print("-" * 80)
        for key, value in sorted(MODELS.items()):
            print(f"  {key:<30} {value}")
        return
    
    # 获取输入文本
    text = None
    if args.file:
        text = read_text_from_file(args.file)
    elif args.text:
        text = args.text
    elif not sys.stdin.isatty():
        # 从标准输入读取
        text = sys.stdin.read()
    else:
        parser.print_help()
        print("\n错误: 请提供输入文本（使用 -f, -t 或通过管道输入）")
        sys.exit(1)
    
    if not text:
        print("错误: 输入文本为空")
        sys.exit(1)
    
    # 创建计算器并计算
    calculator = TokenCalculator(models=args.models, local_mode=False)
    results = calculator.calculate_tokens(text)
    calculator.print_results(text, results)


if __name__ == "__main__":
    main()

