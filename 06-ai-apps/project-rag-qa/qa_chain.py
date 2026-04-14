#!/usr/bin/env python3
"""
RAG 问答链（项目入口）

模块: 06-ai-apps（AI 应用）
知识点: RAG 问答系统
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python qa_chain.py

描述:
    RAG 问答系统的入口，串联所有模块：
    文档加载 → 文本分块 → 向量化 → 检索 → 生成回答。
    使用 TF-IDF + 模板回答模拟完整流程。
"""

import logging

from loader import load_documents
from splitter import split_documents
from embedder import embed_chunks
from retriever import retrieve

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def generate_answer(question: str, context_chunks: list) -> str:
    """
    根据检索到的上下文生成回答。

    在真实系统中，这里会调用 LLM API：
        prompt = f"基于以下资料回答问题:\\n{context}\\n问题: {question}"
        response = client.chat.completions.create(model="gpt-4", messages=[...])

    这里使用简单的模板拼接模拟。
    """
    if not context_chunks:
        return "抱歉，未找到相关信息。"

    # 拼接上下文
    context_texts = []
    sources = set()
    for chunk, similarity in context_chunks:
        context_texts.append(chunk.content)
        sources.add(chunk.metadata.get("source", "未知"))

    context = "\n".join(context_texts)

    # 模拟 LLM 生成回答（实际应调用 API）
    answer = f"根据知识库中的信息：\n\n{context_texts[0]}"
    if len(context_texts) > 1:
        answer += f"\n\n补充信息：{context_texts[1][:100]}..."

    answer += f"\n\n📚 参考来源: {', '.join(sources)}"
    return answer


class RAGSystem:
    """RAG 问答系统。"""

    def __init__(self):
        self.embedded_chunks = None
        self.embedder = None

    def build_index(self):
        """构建知识库索引。"""
        logger.info("=== 构建知识库索引 ===")

        # 1. 加载文档
        documents = load_documents()

        # 2. 文本分块
        chunks = split_documents(documents, chunk_size=150, overlap=30)

        # 3. 向量化
        self.embedded_chunks, self.embedder = embed_chunks(chunks)

        logger.info("知识库索引构建完成\n")

    def ask(self, question: str) -> str:
        """回答问题。"""
        if not self.embedded_chunks:
            return "请先构建知识库索引"

        logger.info(f"问题: {question}")

        # 4. 检索相关文档
        results = retrieve(question, self.embedded_chunks, self.embedder, top_k=2)

        # 5. 生成回答
        answer = generate_answer(question, results)
        return answer


def main():
    """主函数：运行 RAG 问答系统。"""
    print("=" * 60)
    print("  RAG 问答系统")
    print("  使用 TF-IDF 模拟向量检索，无需外部 API")
    print("=" * 60)

    # 初始化系统
    rag = RAGSystem()
    rag.build_index()

    # 测试问答
    questions = [
        "什么是 FastAPI？",
        "YOLO 有什么特点？",
        "RAG 是什么技术？",
        "Python 有哪些应用领域？",
    ]

    for question in questions:
        print(f"\n{'─' * 50}")
        print(f"❓ {question}")
        answer = rag.ask(question)
        print(f"\n💬 {answer}")

    print(f"\n{'─' * 50}")
    print("✅ RAG 问答系统演示完成！")


if __name__ == "__main__":
    main()
