# LangChain 对话链

> **模块：** 06-ai-apps（AI 应用）
> **难度：** 应用入门
> **前置知识：** LLM API 调用、Prompt Engineering
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

LangChain 是构建 LLM 应用的主流框架，提供了 Chain（链）、Agent（智能体）、Memory（记忆）等抽象，帮助开发者快速构建复杂的 AI 应用。

## 核心概念

| 概念 | 说明 | 类比 |
|------|------|------|
| LLM | 大语言模型封装 | 数据库连接 |
| Prompt Template | 提示词模板 | SQL 模板 |
| Chain | 将多个组件串联 | Pipeline |
| Memory | 对话历史管理 | Session |
| Agent | 自主决策和工具调用 | 微服务编排 |
| Tool | Agent 可调用的外部工具 | API 接口 |

## 实战代码

**文件：** `examples/langchain_intro.py`

```bash
pip install langchain  # 可选，演示使用概念模拟
python examples/langchain_intro.py
```

> 💻 **完整可运行代码：** [langchain_intro.py](examples/langchain_intro.py)

## 参考资料

- [LangChain 官方文档](https://python.langchain.com/)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
