#!/usr/bin/env python3
"""
文档加载模块

模块: 06-ai-apps（AI 应用）
知识点: RAG 问答系统 - 文档加载
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    由 qa_chain.py 调用

描述:
    加载文档数据。使用内嵌知识库文本，模拟从文件加载文档。
"""

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Document:
    """文档对象。"""
    content: str
    metadata: dict


# 内嵌知识库（模拟从文件加载）
KNOWLEDGE_BASE = [
    Document(
        content="Python 是一种高级编程语言，由 Guido van Rossum 于 1991 年创建。Python 以简洁和可读性著称，支持面向对象、函数式和过程式编程范式。Python 拥有丰富的标准库和第三方库生态系统，广泛用于 Web 开发、数据分析、人工智能、自动化脚本等领域。",
        metadata={"source": "python_basics.md", "topic": "Python"},
    ),
    Document(
        content="FastAPI 是一个现代的 Python Web 框架，基于 Starlette 和 Pydantic 构建。它支持异步编程（async/await），自动生成 OpenAPI 文档，性能接近 Node.js 和 Go。FastAPI 使用 Python 类型提示进行请求参数验证，开发体验非常好。",
        metadata={"source": "fastapi.md", "topic": "Web 框架"},
    ),
    Document(
        content="Django 是 Python 最流行的全栈 Web 框架，遵循 MTV（Model-Template-View）架构模式。Django 内置 ORM、Admin 后台管理、用户认证系统、表单处理等功能，适合快速开发大型 Web 应用。Django 的理念是'不要重复造轮子'。",
        metadata={"source": "django.md", "topic": "Web 框架"},
    ),
    Document(
        content="NumPy 是 Python 科学计算的基础库，提供高性能的多维数组对象 ndarray。NumPy 的向量化运算比纯 Python 循环快数十倍。NumPy 是 Pandas、Matplotlib、scikit-learn 等库的基础依赖。",
        metadata={"source": "numpy.md", "topic": "数据科学"},
    ),
    Document(
        content="YOLO（You Only Look Once）是一种实时目标检测算法，将检测问题转化为回归问题。YOLOv8 由 Ultralytics 开发，支持目标检测、实例分割、图像分类等多种任务。YOLO 的优势是速度快，适合实时应用场景。",
        metadata={"source": "yolo.md", "topic": "计算机视觉"},
    ),
    Document(
        content="RAG（Retrieval-Augmented Generation）是检索增强生成技术，结合文档检索与大语言模型生成。RAG 的核心流程是：将文档分块并向量化存储，用户提问时检索相关文档片段，将检索结果与问题一起输入 LLM 生成回答。RAG 可以有效减少 LLM 的幻觉问题。",
        metadata={"source": "rag.md", "topic": "AI 应用"},
    ),
]


def load_documents() -> list[Document]:
    """加载文档。"""
    logger.info(f"加载了 {len(KNOWLEDGE_BASE)} 个文档")
    return KNOWLEDGE_BASE


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    docs = load_documents()
    for doc in docs:
        print(f"[{doc.metadata['topic']}] {doc.content[:50]}...")
