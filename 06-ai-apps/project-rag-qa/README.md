# RAG 问答系统项目

> **模块：** 06-ai-apps（AI 应用）
> **难度：** 应用进阶
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 项目说明

本项目实现一个完整的 RAG（检索增强生成）问答系统，演示从文档加载到生成回答的完整流程。

**核心特点：** 使用简单的 TF-IDF 模拟向量检索，不依赖 OpenAI API 或 ChromaDB，可直接运行。

## 项目结构

```
project-rag-qa/
├── README.md          # 项目说明
├── loader.py          # 文档加载模块
├── splitter.py        # 文本分块模块
├── embedder.py        # 向量化模块（TF-IDF 模拟）
├── retriever.py       # 检索模块
└── qa_chain.py        # 问答链（入口）
```

## 数据流程

```
文档文件 → loader.py（加载）→ splitter.py（分块）→ embedder.py（向量化）
                                                          ↓
用户提问 → retriever.py（检索相关片段）→ qa_chain.py（生成回答）
```

## 运行方式

```bash
# 无需额外依赖，使用 Python 标准库
cd project-rag-qa
python qa_chain.py
```

## 预期输出

```
=== RAG 问答系统 ===
加载了 6 个文档片段
分块后共 12 个文本块
向量化完成

问题: 什么是 FastAPI？
检索到 2 个相关片段
回答: FastAPI 是一个现代的 Python Web 框架...

问题: YOLO 有什么用？
检索到 2 个相关片段
回答: YOLO 是实时目标检测算法...
```

## 扩展为真实系统

将本项目扩展为使用真实 Embedding 和 LLM 的系统：

```python
# 替换 embedder.py → 使用 OpenAI Embedding
from openai import OpenAI
client = OpenAI()
response = client.embeddings.create(model="text-embedding-3-small", input=text)

# 替换向量存储 → 使用 ChromaDB
import chromadb
client = chromadb.Client()
collection = client.create_collection("docs")

# 替换 qa_chain.py → 使用 LLM 生成回答
response = client.chat.completions.create(model="gpt-4", messages=[...])
```

> 💻 **完整可运行代码：** [loader.py](loader.py) | [splitter.py](splitter.py) | [embedder.py](embedder.py) | [retriever.py](retriever.py) | [qa_chain.py](qa_chain.py)
