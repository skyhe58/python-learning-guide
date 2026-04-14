# AI Agent 智能体

> **模块：** 06-ai-apps（AI 应用）
> **难度：** 应用进阶
> **前置知识：** LLM API、LangChain、Prompt Engineering
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

AI Agent（智能体）是能够自主决策、调用外部工具完成复杂任务的 AI 系统。与简单的 LLM 对话不同，Agent 可以根据任务需求选择合适的工具（搜索、计算、代码执行等），并通过多步推理完成目标。

## Agent 工作流程

```
用户任务 → Agent 分析 → 选择工具 → 执行工具 → 观察结果
                ↑                                    ↓
                └──── 判断是否完成 ←── 需要更多步骤 ──┘
                         ↓
                    完成 → 返回最终结果
```

## 核心概念

| 概念 | 说明 |
|------|------|
| Tool | Agent 可调用的外部功能（搜索、计算、API 等） |
| Function Calling | LLM 决定调用哪个工具及参数 |
| ReAct | Reasoning + Acting，推理与行动交替的模式 |
| Planning | Agent 将复杂任务分解为子任务 |

## 实战代码

**文件：** `examples/agent_demo.py`

```bash
python examples/agent_demo.py
```

> 💻 **完整可运行代码：** [agent_demo.py](examples/agent_demo.py)

## 参考资料

- [LangChain Agent 文档](https://python.langchain.com/docs/how_to/#agents)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
