#!/usr/bin/env python3
"""
文本分块模块

模块: 06-ai-apps（AI 应用）
知识点: RAG 问答系统 - 文本分块
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    由 qa_chain.py 调用

描述:
    将长文档分割为较小的文本块，便于向量化和检索。
    模拟 LangChain 的 RecursiveCharacterTextSplitter。
"""

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TextChunk:
    """文本块。"""
    content: str
    metadata: dict
    chunk_id: int


def split_documents(documents: list, chunk_size: int = 150, overlap: int = 30) -> list[TextChunk]:
    """
    将文档分割为文本块。

    Args:
        documents: 文档列表
        chunk_size: 每个块的最大字符数
        overlap: 相邻块的重叠字符数
    """
    chunks = []
    chunk_id = 0

    for doc in documents:
        text = doc.content
        # 按句子分割
        sentences = []
        current = ""
        for char in text:
            current += char
            if char in "。！？\n":
                sentences.append(current.strip())
                current = ""
        if current.strip():
            sentences.append(current.strip())

        # 合并句子为块
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
                chunks.append(TextChunk(
                    content=current_chunk.strip(),
                    metadata={**doc.metadata, "chunk_id": chunk_id},
                    chunk_id=chunk_id,
                ))
                chunk_id += 1
                # 保留重叠部分
                current_chunk = current_chunk[-overlap:] + sentence if overlap > 0 else sentence
            else:
                current_chunk += sentence

        if current_chunk.strip():
            chunks.append(TextChunk(
                content=current_chunk.strip(),
                metadata={**doc.metadata, "chunk_id": chunk_id},
                chunk_id=chunk_id,
            ))
            chunk_id += 1

    logger.info(f"分块完成: {len(documents)} 个文档 → {len(chunks)} 个文本块")
    return chunks


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from loader import load_documents
    docs = load_documents()
    chunks = split_documents(docs)
    for chunk in chunks:
        print(f"[{chunk.chunk_id}] ({len(chunk.content)} 字) {chunk.content[:60]}...")
