#!/usr/bin/env python3
"""
Prompt Engineering 提示词工程演示

模块: 06-ai-apps（AI 应用）
知识点: Prompt Engineering（应用入门）
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python prompt_demo.py

描述:
    演示提示词工程的核心技巧：角色设定、Few-shot、
    Chain of Thought、输出格式约束等。
    使用模板展示，无需 API 调用。
"""

import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def demo_role_setting():
    """演示角色设定技巧。"""
    logger.info("--- 1. 角色设定（System Prompt）---")

    # 好的 System Prompt 示例
    prompts = {
        "代码审查": {
            "system": (
                "你是一位资深 Python 代码审查专家。"
                "请从代码质量、性能、安全性三个维度审查代码，"
                "给出具体的改进建议和修改后的代码。"
                "回复格式：先总结问题，再逐条给出建议。"
            ),
            "user": "请审查这段代码: def add(a, b): return a + b",
        },
        "技术翻译": {
            "system": (
                "你是一位技术文档翻译专家，精通中英文互译。"
                "翻译时保留技术术语的英文原文（用括号标注），"
                "确保翻译准确且符合中文技术文档的表达习惯。"
            ),
            "user": "翻译: Dependency Injection is a design pattern.",
        },
    }

    for name, prompt in prompts.items():
        print(f"\n  [{name}]")
        print(f"  System: {prompt['system'][:80]}...")
        print(f"  User:   {prompt['user']}")


def demo_few_shot():
    """演示 Few-shot 示例引导。"""
    logger.info("\n--- 2. Few-shot 示例引导 ---")

    prompt = """请将以下文本分类为"正面"或"负面"。

示例:
输入: "这个产品非常好用，推荐购买！"
输出: 正面

输入: "质量太差了，用了一天就坏了。"
输出: 负面

输入: "包装精美，物流很快，非常满意。"
输出: 正面

现在请分类:
输入: "价格虚高，性价比很低。"
输出: """

    print(f"  Few-shot Prompt:\n{prompt}")
    print("  预期输出: 负面")
    print("  技巧: 提供 3-5 个示例，模型会学习输出格式和分类标准")


def demo_chain_of_thought():
    """演示 Chain of Thought 思维链。"""
    logger.info("\n--- 3. Chain of Thought 思维链 ---")

    # 不使用 CoT
    basic_prompt = "小明有 5 个苹果，给了小红 2 个，又买了 3 个，请问还有几个？"

    # 使用 CoT
    cot_prompt = """小明有 5 个苹果，给了小红 2 个，又买了 3 个，请问还有几个？

请一步一步思考：
1. 首先，小明有多少个苹果？
2. 给了小红之后还剩多少？
3. 又买了之后总共多少？
最后给出答案。"""

    print(f"  基础 Prompt: {basic_prompt}")
    print(f"\n  CoT Prompt:\n{cot_prompt}")
    print("\n  技巧: 加上'请一步一步思考'可以显著提升推理准确率")


def demo_output_format():
    """演示输出格式约束。"""
    logger.info("\n--- 4. 输出格式约束 ---")

    prompt = """请分析以下 Python 代码的问题，以 JSON 格式返回结果。

代码:
```python
def divide(a, b):
    return a / b
```

请严格按照以下 JSON 格式返回:
{
    "issues": [
        {
            "severity": "high/medium/low",
            "description": "问题描述",
            "suggestion": "修改建议"
        }
    ],
    "score": 0-100
}"""

    print(f"  格式约束 Prompt:\n{prompt}")

    # 模拟预期输出
    expected = {
        "issues": [
            {
                "severity": "high",
                "description": "未处理除零错误",
                "suggestion": "添加 b == 0 的检查",
            }
        ],
        "score": 60,
    }
    print(f"\n  预期输出:\n{json.dumps(expected, ensure_ascii=False, indent=2)}")


def demo_prompt_template():
    """演示可复用的 Prompt 模板。"""
    logger.info("\n--- 5. Prompt 模板化 ---")

    # 使用 Python f-string 构建可复用模板
    def build_review_prompt(code: str, language: str = "Python") -> list[dict]:
        return [
            {
                "role": "system",
                "content": f"你是一位 {language} 代码审查专家。请从以下维度审查代码：\n"
                           "1. 代码质量\n2. 性能\n3. 安全性\n"
                           "以 Markdown 格式返回审查报告。",
            },
            {
                "role": "user",
                "content": f"请审查以下 {language} 代码:\n```{language.lower()}\n{code}\n```",
            },
        ]

    messages = build_review_prompt("def add(a, b): return a + b")
    print("  模板化 Messages:")
    for msg in messages:
        print(f"    [{msg['role']}] {msg['content'][:60]}...")

    print("\n  技巧: 将 Prompt 模板化，方便复用和维护")


def main():
    """主函数。"""
    print("=" * 60)
    print("  Prompt Engineering 提示词工程演示")
    print("=" * 60)

    demo_role_setting()
    demo_few_shot()
    demo_chain_of_thought()
    demo_output_format()
    demo_prompt_template()

    print("\n✅ Prompt Engineering 演示完成！")


if __name__ == "__main__":
    main()
