# 实用 AI 应用

> **模块：** 06-ai-apps（AI 应用）
> **难度：** 应用进阶
> **前置知识：** LLM API、Prompt Engineering
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

本节介绍几种常见的实用 AI 应用场景，包括文本分类、情感分析、文本摘要和翻译。这些应用可以通过 LLM API 或专用模型（Transformers）实现。

## 应用场景概览

| 应用 | 技术方案 | 免费替代 |
|------|----------|----------|
| 文本分类 | OpenAI API / Transformers Pipeline | Ollama + 开源模型 |
| 情感分析 | OpenAI API / Transformers sentiment | Ollama / HuggingFace |
| 文本摘要 | OpenAI API / Transformers summarization | Ollama |
| 翻译 | OpenAI API / MarianMT | Ollama / Argos Translate |
| 图像生成 | DALL-E API / Stable Diffusion | Stable Diffusion 本地 |
| 语音识别 | OpenAI Whisper API | Whisper 本地模型 |

## 免费替代方案

对于不想使用付费 API 的用户：
1. **Ollama** — 本地运行 Llama/Qwen 等开源模型
2. **HuggingFace Transformers** — 本地运行专用模型
3. **Stable Diffusion** — 本地图像生成

## 实战代码

**文件：** `examples/practical_ai_demo.py`

```bash
python examples/practical_ai_demo.py
```

> 💻 **完整可运行代码：** [practical_ai_demo.py](examples/practical_ai_demo.py)

## 参考资料

- [HuggingFace Transformers](https://huggingface.co/docs/transformers/)
- [Ollama 模型库](https://ollama.ai/library)
