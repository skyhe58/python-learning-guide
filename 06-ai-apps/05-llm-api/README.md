# LLM API 调用

> **模块：** 06-ai-apps（AI 应用）
> **难度：** 应用入门
> **前置知识：** Python 基础、HTTP 请求
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

大语言模型（LLM）通过 API 提供文本生成、对话、翻译等能力。OpenAI 的 Chat Completions API 是最常用的接口，其他厂商（如 Anthropic Claude、Google Gemini）也提供类似的 API。

本节演示 API 调用的完整流程，使用 **mock 模拟**替代真实 API 调用，无需 API Key 即可学习。

## 核心概念

| 概念 | 说明 |
|------|------|
| Chat Completions | 对话补全接口，输入消息列表，返回模型回复 |
| Messages | 消息列表，包含 system/user/assistant 三种角色 |
| Temperature | 控制输出随机性（0=确定性，1=创造性） |
| Tokens | 文本的最小单位，影响计费和上下文长度 |
| Streaming | 流式响应，逐字返回结果 |

## API 调用流程

```
用户输入 → 构造 Messages → 调用 API → 解析响应 → 返回结果
                ↓
    [{"role": "system", "content": "你是助手"},
     {"role": "user", "content": "你好"}]
```

## 免费替代方案：Ollama

如果不想使用付费 API，可以用 **Ollama** 在本地运行开源模型：

```bash
# 安装 Ollama（https://ollama.ai）
# macOS
brew install ollama

# 下载并运行模型
ollama run llama3.2    # Meta Llama 3.2
ollama run qwen2.5     # 通义千问 2.5

# Ollama 提供兼容 OpenAI 的 API
# 只需将 base_url 改为 http://localhost:11434/v1
```

## 实战代码

**文件：** `examples/llm_api_demo.py`

```bash
pip install openai  # 可选，演示使用 mock 模拟
python examples/llm_api_demo.py
```

**预期输出：**
```
=== LLM API 调用演示（Mock 模拟）===
[基础调用] 模型回复: Python 是一种简洁优雅的编程语言...
[流式响应] 逐字输出: P y t h o n ...
[多轮对话] 对话历史管理演示完成
```

## 常见陷阱

- ⚠️ API Key 不要硬编码在代码中，使用环境变量
- ⚠️ 注意 Token 限制，过长的输入会被截断
- ⚠️ 网络请求需要异常处理（超时、限流等）
- ⚠️ Temperature 设置影响输出一致性，生产环境建议设低

> 💻 **完整可运行代码：** [llm_api_demo.py](examples/llm_api_demo.py)

## 参考资料

- [OpenAI API 文档](https://platform.openai.com/docs/api-reference)
- [Ollama 官网](https://ollama.ai/)
