# Tokenizer下载状态

## 下载完成情况

### ✅ 成功下载的模型（11个）

#### Qwen3系列（7个）
- ✅ qwen3-0.6b (Qwen/Qwen3-0.6B)
- ✅ qwen3-1.7b (Qwen/Qwen3-1.7B)
- ✅ qwen3-4b (Qwen/Qwen3-4B)
- ✅ qwen3-8b (Qwen/Qwen3-8B)
- ✅ qwen3-14b (Qwen/Qwen3-14B)
- ✅ qwen3-32b (Qwen/Qwen3-32B)
- ✅ qwen3-30b-a3b (Qwen/Qwen3-30B-A3B)

#### DeepSeek系列（4个）
- ✅ deepseek-v3 (deepseek-ai/DeepSeek-V3)
- ✅ deepseek-v3-base (deepseek-ai/DeepSeek-V3-Base)
- ✅ deepseek-v3.1 (deepseek-ai/DeepSeek-V3.1)
- ✅ deepseek-v3.1-base (deepseek-ai/DeepSeek-V3.1-Base)

## 文件大小

- **tokenizers目录总大小**：约50-100MB（取决于具体模型）
- **每个模型**：约2-10MB

## 模型说明

### Qwen3系列
Qwen3是Qwen团队最新发布的模型系列，包含多个不同规模的模型，从0.6B到30B-A3B。

### DeepSeek系列
- **DeepSeek-V3**: DeepSeek V3版本
- **DeepSeek-V3-Base**: DeepSeek V3基础版本
- **DeepSeek-V3.1**: DeepSeek V3.1版本
- **DeepSeek-V3.1-Base**: DeepSeek V3.1基础版本

**注意**：DeepSeek-671B在HuggingFace上不存在，因此未包含在模型列表中。

## 验证下载

检查tokenizers目录：

```bash
ls -la tokenizers/
```

每个模型目录应包含：
- `tokenizer_config.json`
- `tokenizer.json` 或其他tokenizer文件
- 其他相关配置文件

## 使用说明

下载完成后，应用会自动检测并使用本地tokenizer文件，无需网络连接。

所有11个模型都已成功下载，可以完全离线使用。
