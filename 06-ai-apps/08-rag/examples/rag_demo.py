#!/usr/bin/env python3
"""
RAG 检索增强生成演示

模块: 06-ai-apps（AI 应用）
知识点: RAG（应用进阶）
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python rag_demo.py

描述:
    用纯 Python 模拟 RAG 的完整流程：
    文档加载 → 文本分块 → 向量化 → 检索 → 生成回答。
    使用简单的 TF-IDF 模拟向量检索，无需外部 API。
"""

import logging
import math
import re
from collections import Counter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 模拟知识库文档
# ---------------------------------------------------------------------------
DOCUMENTS = [
    "Python 是一种高级编程语言，由 Guido van Rossum 于 1991 年创建。Python 以简洁和可读性著称，广泛用于 Web 开发、数据分析、人工智能等领域。",
    "FastAPI 是一个现代的 Python Web 框架，基于 Starlette 和 Pydantic 构建。它支持异步编程，自动生成 API 文档，性能接近 Node.js 和 Go。",
    "Django 是 Python 最流行的全栈 Web 框架，内置 ORM、Admin 后台、认证系统。Django 遵循 MTV 架构模式，适合快速开发大型 Web 应用。",
    "NumPy 是 Python 科学计算的基础库，提供高性能的多维数组对象。NumPy 的向量化运算比纯 Python 循环快数十倍，是数据分析和机器学习的基石。",
    "Pandas 是基于 NumPy 的数据分析库，提供 DataFrame 数据结构。Pandas 支持数据读取、清洗、转换、聚合等操作，类似于 SQL 和 Excel 的结合。",
    "YOLO（You Only Look Once）是一种实时目标检测算法。YOLOv8 由 Ultralytics 开发，支持检测、分割、分类等多种任务，是目前最流行的目标检测框架。",
]


# ---------------------------------------------------------------------------
# 简单的 TF-IDF 向量化（模拟 Embedding）
# ---------------------------------------------------------------------------
def tokenize(text: str) -> list[str]:
    """简单中英文分词。"""
    # 英文按空格分词，中文按字分词
    words = re.findall(r"[a-zA-Z]+|[\u4e00-\u9fff]", text.lower())
    return words


def compute_tfidf(documents: list[str]) -> tuple[list[dict], dict]:
    """计算 TF-IDF 向量。"""
    doc_tokens = [tokenize(doc) for doc in documents]
    # 计算 IDF
    all_words = set()
    for tokens in doc_tokens:
        all_words.update(tokens)
    n_docs = len(documents)
    idf = {}
    for word in all_words:
        df = sum(1 for tokens in doc_tokens if word in tokens)
        idf[word] = math.log(n_docs / (df + 1))
    # 计算 TF-IDF
    tfidf_vectors = []
    for tokens in doc_tokens:
        tf = Counter(tokens)
        total = len(tokens)
        vector = {w: (tf[w] / total) * idf.get(w, 0) for w in tf}
        tfidf_vectors.append(vector)
    return tfidf_vectors, idf


def cosine_similarity(v1: dict, v2: dict) -> float:
    """计算余弦相似度。"""
    common = set(v1.keys()) & set(v2.keys())
    dot = sum(v1[w] * v2[w] for w in common)
    norm1 = math.sqrt(sum(v ** 2 for v in v1.values()))
    norm2 = math.sqrt(sum(v ** 2 for v in v2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


# ---------------------------------------------------------------------------
# RAG 流程演示
# ---------------------------------------------------------------------------
def demo_rag_pipeline():
    """演示完整的 RAG 流程。"""
    # Step 1: 文档加载
    logger.info("--- Step 1: 文档加载 ---")
    logger.info(f"加载了 {len(DOCUMENTS)} 个文档片段")

    # Step 2: 向量化（使用 TF-IDF 模拟 Embedding）
    logger.info("\n--- Step 2: 向量化 ---")
    vectors, idf = compute_tfidf(DOCUMENTS)
    logger.info(f"生成了 {len(vectors)} 个文档向量")

    # Step 3: 用户提问 + 检索
    questions = [
        "什么是 FastAPI？",
        "YOLO 是什么？",
        "Python 数据分析用什么库？",
    ]

    for question in questions:
        logger.info(f"\n--- 用户提问: {question} ---")

        # 将问题向量化
        q_tokens = tokenize(question)
        q_tf = Counter(q_tokens)
        q_total = len(q_tokens)
        q_vector = {w: (q_tf[w] / q_total) * idf.get(w, 0) for w in q_tf}

        # 计算相似度并排序
        similarities = []
        for i, vec in enumerate(vectors):
            sim = cosine_similarity(q_vector, vec)
            similarities.append((i, sim))
        similarities.sort(key=lambda x: x[1], reverse=True)

        # 取 Top 2 相关文档
        top_k = 2
        relevant_docs = []
        for idx, sim in similarities[:top_k]:
            relevant_docs.append(DOCUMENTS[idx])
            logger.info(f"  相关文档 (相似度 {sim:.3f}): {DOCUMENTS[idx][:50]}...")

        # Step 4: 构造 Prompt 并"生成"回答
        context = "\n".join(relevant_docs)
        prompt = f"基于以下参考资料回答问题:\n\n{context}\n\n问题: {question}\n回答:"
        # 模拟 LLM 回答（实际应调用 LLM API）
        answer = f"根据知识库，{relevant_docs[0][:60]}..."
        logger.info(f"  回答: {answer}")


def main():
    """主函数。"""
    print("=" * 60)
    print("  RAG 检索增强生成演示")
    print("  使用 TF-IDF 模拟向量检索，无需外部 API")
    print("=" * 60)

    demo_rag_pipeline()

    print("\n✅ RAG 演示完成！")


if __name__ == "__main__":
    main()
