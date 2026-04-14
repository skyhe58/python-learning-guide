# Prompt Engineering（提示词工程）

> **模块：** 06-ai-apps（AI 应用）
> **难度：** 应用入门
> **前置知识：** LLM API 调用
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

Prompt Engineering 是通过精心设计输入提示词来引导 LLM 产生更好输出的技术。好的提示词可以显著提升模型的回答质量、准确性和一致性。

## 核心技巧

| 技巧 | 说明 | 适用场景 |
|------|------|----------|
| 角色设定 | 给模型指定身份和行为规范 | 所有场景 |
| Few-shot | 提供几个示例引导输出格式 | 格式化输出 |
| Chain of Thought | 要求模型逐步推理 | 复杂推理 |
| 输出格式约束 | 指定 JSON/Markdown 等格式 | 结构化输出 |
| 分步指令 | 将复杂任务拆分为步骤 | 多步骤任务 |

## 实战代码

**文件：** `examples/prompt_demo.py`

```bash
python examples/prompt_demo.py
```

**预期输出：**
```
=== Prompt Engineering 演示 ===
[角色设定] 系统提示词设计
[Few-shot] 示例引导输出
[CoT] 思维链推理
[格式约束] JSON 输出
```

> 💻 **完整可运行代码：** [prompt_demo.py](examples/prompt_demo.py)

## 参考资料

- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Prompt Engineering Guide](https://www.promptingguide.ai/zh)
