#!/usr/bin/env python3
"""
LangChain 概念演示

模块: 06-ai-apps（AI 应用）
知识点: LangChain 对话链（应用入门）
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python langchain_intro.py

依赖安装:
    pip install langchain langchain-openai  # 可选

描述:
    用纯 Python 模拟 LangChain 的核心概念：
    PromptTemplate、Chain、Memory，帮助理解框架思想。
"""

import logging
from string import Template

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# 模拟 LangChain 核心组件
# ---------------------------------------------------------------------------
class MockLLM:
    """模拟 LLM（替代 ChatOpenAI）。"""

    def invoke(self, prompt: str) -> str:
        if "翻译" in prompt:
            return "Translation: Hello, World!"
        if "总结" in prompt or "摘要" in prompt:
            return "这是一段关于 Python 编程的文本摘要。"
        return f"[Mock LLM 回复] 收到输入: {prompt[:50]}..."


class PromptTemplate:
    """
    模拟 LangChain 的 PromptTemplate。

    真实 LangChain 代码:
        from langchain.prompts import ChatPromptTemplate
        prompt = ChatPromptTemplate.from_template(
            "请将以下文本翻译为{language}: {text}"
        )
    """

    def __init__(self, template: str):
        self.template = Template(template)

    def format(self, **kwargs) -> str:
        return self.template.safe_substitute(**kwargs)


class SimpleChain:
    """
    模拟 LangChain 的 Chain（LCEL 管道）。

    真实 LangChain 代码:
        chain = prompt | llm | output_parser
        result = chain.invoke({"language": "英文", "text": "你好"})
    """

    def __init__(self, prompt: PromptTemplate, llm: MockLLM):
        self.prompt = prompt
        self.llm = llm

    def invoke(self, inputs: dict) -> str:
        formatted = self.prompt.format(**inputs)
        logger.info(f"  Prompt: {formatted[:80]}...")
        result = self.llm.invoke(formatted)
        return result


class ConversationMemory:
    """
    模拟 LangChain 的 Memory。

    真实 LangChain 代码:
        from langchain.memory import ConversationBufferMemory
        memory = ConversationBufferMemory()
    """

    def __init__(self):
        self.history: list[dict] = []

    def add(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def get_context(self) -> str:
        return "\n".join(f"{m['role']}: {m['content']}" for m in self.history)


# ---------------------------------------------------------------------------
# 演示函数
# ---------------------------------------------------------------------------
def demo_prompt_template():
    """演示 PromptTemplate。"""
    logger.info("--- 1. PromptTemplate 提示词模板 ---")

    template = PromptTemplate("请将以下文本翻译为$language: $text")
    result = template.format(language="英文", text="你好世界")
    print(f"  模板输出: {result}")

    # 多个模板组合
    review_template = PromptTemplate(
        "你是$role。请审查以下$language代码:\n$code\n请给出改进建议。"
    )
    result = review_template.format(
        role="资深开发者", language="Python", code="def add(a,b): return a+b"
    )
    print(f"  审查模板: {result[:60]}...")


def demo_simple_chain():
    """演示 Chain 链式调用。"""
    logger.info("\n--- 2. Chain 链式调用 ---")

    llm = MockLLM()

    # 翻译链
    translate_chain = SimpleChain(
        prompt=PromptTemplate("请将以下文本翻译为$language: $text"),
        llm=llm,
    )
    result = translate_chain.invoke({"language": "英文", "text": "你好世界"})
    print(f"  翻译结果: {result}")

    # 摘要链
    summary_chain = SimpleChain(
        prompt=PromptTemplate("请总结以下文本（不超过50字）:\n$text"),
        llm=llm,
    )
    result = summary_chain.invoke({"text": "Python 是一种广泛使用的编程语言..."})
    print(f"  摘要结果: {result}")


def demo_memory():
    """演示 Memory 对话记忆。"""
    logger.info("\n--- 3. Memory 对话记忆 ---")

    memory = ConversationMemory()
    llm = MockLLM()

    # 模拟多轮对话
    conversations = [
        ("user", "什么是 Python？"),
        ("assistant", "Python 是一种高级编程语言。"),
        ("user", "它有什么优点？"),
        ("assistant", "简洁、易读、生态丰富。"),
    ]

    for role, content in conversations:
        memory.add(role, content)

    print(f"  对话历史 ({len(memory.history)} 条):")
    print(f"  {memory.get_context()}")

    # 带记忆的新请求
    context = memory.get_context()
    new_prompt = f"基于以下对话历史:\n{context}\n\n用户新问题: 推荐学习资源"
    response = llm.invoke(new_prompt)
    print(f"\n  带记忆的回复: {response}")


def show_real_langchain_code():
    """展示真实 LangChain 代码。"""
    logger.info("\n--- 4. 真实 LangChain 代码参考 ---")
    print("""
    # 安装: pip install langchain langchain-openai

    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema.output_parser import StrOutputParser

    # 初始化 LLM
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)

    # 创建 Prompt 模板
    prompt = ChatPromptTemplate.from_template(
        "请将以下文本翻译为{language}: {text}"
    )

    # 构建 Chain（LCEL 语法）
    chain = prompt | llm | StrOutputParser()

    # 调用
    result = chain.invoke({"language": "英文", "text": "你好世界"})
    print(result)
    """)


def main():
    """主函数。"""
    print("=" * 60)
    print("  LangChain 概念演示")
    print("  模拟 PromptTemplate → Chain → Memory")
    print("=" * 60)

    demo_prompt_template()
    demo_simple_chain()
    demo_memory()
    show_real_langchain_code()

    print("✅ LangChain 概念演示完成！")


if __name__ == "__main__":
    main()
