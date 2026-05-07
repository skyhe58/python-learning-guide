#!/usr/bin/env python3
"""
检索模块

模块: 06-ai-apps（AI 应用）
知识点: RAG 问答系统 - 向量检索
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    由 qa_chain.py 调用

描述:
    根据用户问题检索最相关的文本块。
    使用余弦相似度计算向量距离。
"""

import logging
import math

logger = logging.getLogger(__name__)


def cosine_similarity(v1: dict, v2: dict) -> float:
    """计算两个稀疏向量的余弦相似度。"""
    common = set(v1.keys()) & set(v2.keys())
    if not common:
        return 0.0
    dot = sum(v1[w] * v2[w] for w in common)
    norm1 = math.sqrt(sum(v ** 2 for v in v1.values()))
    norm2 = math.sqrt(sum(v ** 2 for v in v2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def retrieve(query: str, embedded_chunks: list, embedder, top_k: int = 3) -> list:
    """
    检索与查询最相关的文本块。

    Args:
        query: 用户问题
        embedded_chunks: 向量化后的文本块列表
        embedder: 向量化器（用于将查询向量化）
        top_k: 返回最相关的 k 个结果
    """
    # 将查询向量化
    query_vector = embedder.embed(query)

    # 计算相似度
    results = []
    for chunk in embedded_chunks:
        sim = cosine_similarity(query_vector, chunk.vector)
        results.append((chunk, sim))

    # 按相似度降序排序
    results.sort(key=lambda x: x[1], reverse=True)

    # 返回 Top K
    top_results = results[:top_k]
    logger.info(f"检索 '{query[:20]}...': 返回 {len(top_results)} 个结果")
    for chunk, sim in top_results:
        logger.info(f"  [{sim:.3f}] {chunk.content[:50]}...")

    return top_results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from loader import load_documents
    from splitter import split_documents
    from embedder import embed_chunks

    docs = load_documents()
    chunks = split_documents(docs)
    embedded, embedder = embed_chunks(chunks)

    results = retrieve("什么是 FastAPI？", embedded, embedder, top_k=2)
    for chunk, sim in results:
        print(f"[{sim:.3f}] {chunk.content}")
