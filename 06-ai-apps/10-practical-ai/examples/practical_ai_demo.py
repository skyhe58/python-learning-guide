#!/usr/bin/env python3
"""
实用 AI 应用概览演示

模块: 06-ai-apps（AI 应用）
知识点: 实用 AI 应用（应用进阶）
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python practical_ai_demo.py

依赖安装:
    # 基础演示无需额外依赖
    # 使用 Transformers: pip install transformers torch
    # 使用 OpenAI: pip install openai

描述:
    演示常见 AI 应用场景的实现思路，使用 mock 模拟。
    包括文本分类、情感分析、文本摘要、翻译等。
"""

import logging
import re

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def demo_text_classification():
    """演示文本分类（使用简单规则模拟）。"""
    logger.info("--- 1. 文本分类 ---")

    # 简单的关键词分类器（模拟 LLM/Transformers 分类）
    categories = {
        "技术": ["python", "代码", "编程", "框架", "api", "数据库"],
        "商业": ["市场", "销售", "营收", "客户", "产品"],
        "生活": ["美食", "旅游", "健康", "运动", "电影"],
    }

    texts = [
        "Python 3.12 发布了新的性能优化特性",
        "今年第三季度营收同比增长 20%",
        "周末去了一家很棒的日料餐厅",
    ]

    for text in texts:
        text_lower = text.lower()
        scores = {}
        for cat, keywords in categories.items():
            scores[cat] = sum(1 for kw in keywords if kw in text_lower)
        predicted = max(scores, key=scores.get) if max(scores.values()) > 0 else "未知"
        logger.info(f"  '{text[:30]}...' → {predicted}")

    print("  💡 实际应用: 使用 OpenAI API 或 Transformers Pipeline 效果更好")


def demo_sentiment_analysis():
    """演示情感分析（使用简单规则模拟）。"""
    logger.info("\n--- 2. 情感分析 ---")

    positive_words = {"好", "棒", "优秀", "推荐", "满意", "喜欢", "方便", "快"}
    negative_words = {"差", "烂", "失望", "难用", "慢", "贵", "坏", "糟糕"}

    reviews = [
        "这个产品非常好用，强烈推荐！",
        "质量太差了，用了一天就坏了。",
        "价格合理，物流也很快，满意。",
        "界面设计很糟糕，操作很难用。",
    ]

    for review in reviews:
        pos = sum(1 for w in positive_words if w in review)
        neg = sum(1 for w in negative_words if w in review)
        if pos > neg:
            sentiment = "😊 正面"
        elif neg > pos:
            sentiment = "😞 负面"
        else:
            sentiment = "😐 中性"
        logger.info(f"  '{review[:25]}...' → {sentiment}")

    print("  💡 实际应用: transformers pipeline('sentiment-analysis')")


def demo_text_summary():
    """演示文本摘要（使用简单提取式摘要模拟）。"""
    logger.info("\n--- 3. 文本摘要 ---")

    text = (
        "Python 是一种广泛使用的高级编程语言。它由 Guido van Rossum 于 1991 年创建。"
        "Python 的设计哲学强调代码的可读性和简洁性。"
        "Python 支持多种编程范式，包括面向对象、函数式和过程式编程。"
        "Python 拥有丰富的标准库和第三方库生态系统。"
        "Python 在 Web 开发、数据科学、人工智能等领域有广泛应用。"
    )

    # 简单提取式摘要：取前两句
    sentences = re.split(r"[。！？]", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    summary = "。".join(sentences[:2]) + "。"

    logger.info(f"  原文 ({len(text)} 字): {text[:50]}...")
    logger.info(f"  摘要 ({len(summary)} 字): {summary}")

    print("  💡 实际应用: OpenAI API 或 transformers pipeline('summarization')")


def demo_translation():
    """演示翻译（使用简单词典模拟）。"""
    logger.info("\n--- 4. 翻译 ---")

    # 简单词典翻译（模拟）
    simple_dict = {
        "你好": "Hello", "世界": "World", "编程": "Programming",
        "语言": "Language", "学习": "Learning", "人工智能": "AI",
    }

    texts = ["你好世界", "学习编程语言", "人工智能"]
    for text in texts:
        translated = text
        for cn, en in simple_dict.items():
            translated = translated.replace(cn, en)
        logger.info(f"  '{text}' → '{translated}'")

    print("  💡 实际应用: OpenAI API 或 MarianMT / Argos Translate")


def show_real_code_examples():
    """展示真实代码参考。"""
    logger.info("\n--- 5. 真实代码参考 ---")
    print("""
    # === Transformers Pipeline（本地模型）===
    from transformers import pipeline

    # 情感分析
    classifier = pipeline("sentiment-analysis")
    result = classifier("I love Python!")
    # [{'label': 'POSITIVE', 'score': 0.9998}]

    # 文本摘要
    summarizer = pipeline("summarization")
    summary = summarizer(long_text, max_length=100)

    # === OpenAI API ===
    from openai import OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "你是翻译专家"},
            {"role": "user", "content": "翻译: 你好世界"},
        ],
    )

    # === Ollama 免费替代 ===
    # ollama run qwen2.5
    # 然后使用 OpenAI SDK，base_url="http://localhost:11434/v1"
    """)


def main():
    """主函数。"""
    print("=" * 60)
    print("  实用 AI 应用概览演示")
    print("  使用简单规则模拟，展示应用思路")
    print("=" * 60)

    demo_text_classification()
    demo_sentiment_analysis()
    demo_text_summary()
    demo_translation()
    show_real_code_examples()

    print("✅ 实用 AI 应用演示完成！")


if __name__ == "__main__":
    main()
