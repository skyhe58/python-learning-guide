# AI 应用

> **阶段：** 第四阶段
> **前置条件：** [01-Python 基础](../01-python-basics/)，建议完成第二、三阶段后学习

## 模块简介

本模块面向 Java 开发者，从 AI 基础入门（NumPy/Pandas/Matplotlib）到实际 AI 应用开发（LLM API、RAG、AI Agent），循序渐进地掌握 Python AI 生态。每个知识点都标注了难度等级，帮助你按照合适的节奏学习。

## 知识点列表

| 序号 | 知识点 | 描述 | 难度 |
|------|--------|------|------|
| 01 | [NumPy 基础](./01-numpy-basics/) | 数组创建与基础运算，对标 Java 数组操作 | 入门铺垫 |
| 02 | [Pandas 基础](./02-pandas-basics/) | DataFrame 数据读取与基础操作，对标 Java Stream | 入门铺垫 |
| 03 | [Matplotlib 绘图](./03-matplotlib/) | 折线图/柱状图/散点图基础绑制 | 入门铺垫 |
| 04 | [Jupyter Notebook](./04-jupyter/) | Jupyter 安装、使用和快捷键 | 入门铺垫 |
| 05 | [LLM API 调用](./05-llm-api/) | OpenAI Chat Completions API、流式响应 | 应用入门 |
| 06 | [Prompt Engineering](./06-prompt-engineering/) | 提示词工程基础技巧 | 应用入门 |
| 07 | [LangChain 对话链](./07-langchain/) | 使用 LangChain 构建对话链 | 应用入门 |
| 08 | [RAG 检索增强生成](./08-rag/) | 文档加载、文本分块、向量嵌入、知识库问答 | 应用进阶 |
| 09 | [AI Agent 智能体](./09-ai-agent/) | LangChain Agent、Function Calling、多步推理 | 应用进阶 |
| 10 | [实用 AI 应用](./10-practical-ai/) | 文本分类、图像生成、语音识别、文本摘要 | 应用进阶 |

## 推荐学习路径

```
入门铺垫：NumPy → Pandas → Matplotlib → Jupyter
    ↓
应用入门：LLM API 调用 → Prompt Engineering → LangChain
    ↓
应用进阶：RAG → AI Agent → 实用 AI 应用
    ↓
综合实战：RAG 问答系统项目
```

## 模块依赖安装

```bash
pip install -r requirements.txt
```

## 综合项目

完成所有知识点学习后，请挑战 [RAG 问答系统项目](./project-rag-qa/)，涵盖文档加载、文本分块、向量化存储、检索和 LLM 生成回答的完整流程。
