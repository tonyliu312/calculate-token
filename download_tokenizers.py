#!/usr/bin/env python3
"""
下载所有tokenizer到本地
"""

import sys
from pathlib import Path
from calculate_tokens import MODELS

try:
    from transformers import AutoTokenizer
    from huggingface_hub import snapshot_download
except ImportError:
    print("错误: 请先安装必要的库")
    print("运行: pip install transformers huggingface_hub")
    sys.exit(1)


def download_tokenizer(model_key: str, model_name: str, output_dir: Path):
    """下载单个tokenizer"""
    print(f"\n正在下载 {model_key} ({model_name})...")
    
    try:
        # 创建输出目录
        model_dir = output_dir / model_key
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # 方法1: 使用snapshot_download下载tokenizer相关文件
        try:
            print(f"  使用snapshot_download下载...")
            snapshot_download(
                repo_id=model_name,
                allow_patterns=[
                    "tokenizer_config.json",
                    "vocab.json",
                    "merges.txt",
                    "vocab.txt",
                    "special_tokens_map.json",
                    "added_tokens.json",
                    "tokenizer.json",
                    "*.model",
                    "*.bpe",
                    "*.vocab",
                    "spiece.model",
                    "sentencepiece.bpe.model",
                    "*.tiktoken",
                ],
                local_dir=str(model_dir),
                local_dir_use_symlinks=False,
                ignore_patterns=["*.bin", "*.safetensors", "*.pt", "*.pth", "*.h5", "*.onnx", "*.pb"],
            )
            print(f"  ✓ 下载完成: {model_dir}")
        except Exception as e1:
            print(f"  snapshot_download失败: {e1}")
            # 方法2: 使用AutoTokenizer下载
            try:
                print(f"  使用AutoTokenizer下载...")
                tokenizer = AutoTokenizer.from_pretrained(
                    model_name,
                    trust_remote_code=True
                )
                tokenizer.save_pretrained(str(model_dir))
                print(f"  ✓ 下载完成: {model_dir}")
            except Exception as e2:
                print(f"  AutoTokenizer下载也失败: {e2}")
                raise e2
        
        return True
    
    except Exception as e:
        print(f"  ✗ 下载失败: {e}")
        return False


def main():
    """主函数"""
    # 输出目录
    output_dir = Path(__file__).parent / "tokenizers"
    output_dir.mkdir(exist_ok=True)
    
    print("=" * 80)
    print("Tokenizer下载工具")
    print("=" * 80)
    print(f"输出目录: {output_dir}")
    print(f"将下载 {len(MODELS)} 个模型的tokenizer")
    print("=" * 80)
    
    # 统计
    success_count = 0
    fail_count = 0
    failed_models = []
    
    # 下载所有模型
    for model_key, model_name in MODELS.items():
        success = download_tokenizer(model_key, model_name, output_dir)
        if success:
            success_count += 1
        else:
            fail_count += 1
            failed_models.append(model_key)
    
    # 创建模型索引文件
    index_file = output_dir / "models_index.json"
    import json
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(MODELS, f, indent=2, ensure_ascii=False)
    print(f"\n模型索引已保存到: {index_file}")
    
    # 输出结果
    print("\n" + "=" * 80)
    print("下载完成")
    print("=" * 80)
    print(f"成功: {success_count}/{len(MODELS)}")
    print(f"失败: {fail_count}/{len(MODELS)}")
    
    if failed_models:
        print(f"\n失败的模型:")
        for model in failed_models:
            print(f"  - {model}")
    
    print("=" * 80)
    
    if fail_count > 0:
        print("\n警告: 部分模型下载失败，请检查网络连接或稍后重试")
        sys.exit(1)
    else:
        print("\n所有tokenizer下载成功！")


if __name__ == "__main__":
    main()

