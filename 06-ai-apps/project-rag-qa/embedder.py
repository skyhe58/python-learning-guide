#!/usr/bin/env python3
"""
向量化模块

模块: 06-ai-apps（AI 应用）
知识点: RAG 问答系统 - 向量嵌入
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    由 qa_chain.py 调用

描述:
    将文本块转换为向量表示。使用 TF-IDF 模拟真实的 Embedding，
    无需 OpenAI API 或 sentence-transformers。
"""

import logging
import math
import re
from collections import Counter
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class EmbeddedChunk:
    """带向量的文本块。"""
    content: str
    metadata: dict
    chunk_id: int
    vector: dict = field(default_factory=dict)


def _tokenize(text: str) -> list[str]:
    """简单中英文分词。"""
    return re.findall(r"[a-zA-Z]+|[\u4e00-\u9fff]", text.lower())


class TFIDFEmbedder:
    """TF-IDF 向量化器（模拟 Embedding 模型）。"""

    def __init__(self):
        self.idf: dict[str, float] = {}
        self.vocab: set[str] = set()

    def fit(self, texts: list[str]):
        """计算 IDF。"""
        n_docs = len(texts)
        doc_tokens = [set(_tokenize(t)) for t in texts]
        all_words = set()
        for tokens in doc_tokens:
            all_words.update(tokens)
        self.vocab = all_words
        for word in all_words:
            df = sum(1 for tokens in doc_tokens if word in tokens)
            self.idf[word] = math.log(n_docs / (df + 1)) + 1

    def embed(self, text: str) -> dict[str, float]:
        """将文本转换为 TF-IDF 向量。"""
        tokens = _tokenize(text)
        tf = Counter(tokens)
        total = len(tokens) if tokens else 1
        return {w: (tf[w] / total) * self.idf.get(w, 0) for w in tf if w in self.idf}


def embed_chunks(chunks: list) -> tuple[list[EmbeddedChunk], TFIDFEmbedder]:
    """将文本块向量化。"""
    texts = [c.content for c in chunks]
    embedder = TFIDFEmbedder()
    embedder.fit(texts)

    embedded = []
    for chunk in chunks:
        vector = embedder.embed(chunk.content)
        embedded.append(EmbeddedChunk(
            content=chunk.content,
            metadata=chunk.metadata,
            chunk_id=chunk.chunk_id,
            vector=vector,
        ))

    logger.info(f"向量化完成: {len(embedded)} 个文本块, 词汇表大小: {len(embedder.vocab)}")
    return embedded, embedder


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from loader import load_documents
    from splitter import split_documents
    docs = load_documents()
    chunks = split_documents(docs)
    embedded, embedder = embed_chunks(chunks)
    for ec in embedded[:3]:
        print(f"[{ec.chunk_id}] 向量维度: {len(ec.vector)}, 内容: {ec.content[:40]}...")
