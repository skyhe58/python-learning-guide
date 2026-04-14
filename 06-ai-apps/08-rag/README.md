# RAG 检索增强生成

> **模块：** 06-ai-apps（AI 应用）
> **难度：** 应用进阶
> **前置知识：** LLM API 调用、LangChain 基础
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

RAG（Retrieval-Augmented Generation）是将文档检索与 LLM 生成相结合的技术。它解决了 LLM 的两个核心问题：知识过时和幻觉（编造事实）。

## RAG 工作流程

```
文档 → 分块 → 向量化 → 存入向量数据库
                                ↓
用户提问 → 向量化 → 相似度检索 → 获取相关文档片段
                                ↓
            相关文档 + 用户问题 → LLM 生成回答
```

## 核心组件

| 组件 | 职责 | 常用工具 |
|------|------|----------|
| Document Loader | 加载文档 | LangChain Loaders |
| Text Splitter | 文本分块 | RecursiveCharacterTextSplitter |
| Embedding | 文本向量化 | OpenAI Embedding / sentence-transformers |
| Vector Store | 向量存储和检索 | ChromaDB / FAISS / Pinecone |
| LLM | 生成回答 | GPT-4 / Llama / Qwen |

## 实战代码

**文件：** `examples/rag_demo.py`

```bash
python examples/rag_demo.py
```

> 💻 **完整可运行代码：** [rag_demo.py](examples/rag_demo.py)

## 参考资料

- [LangChain RAG 教程](https://python.langchain.com/docs/tutorials/rag/)
- [ChromaDB 文档](https://docs.trychroma.com/)
