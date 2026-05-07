#!/usr/bin/env python3
"""
LLM API 调用演示（Mock 模拟）

模块: 06-ai-apps（AI 应用）
知识点: LLM API 调用（应用入门）
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python llm_api_demo.py

依赖安装:
    pip install openai  # 可选，本演示使用 mock 模拟

描述:
    演示 OpenAI Chat Completions API 的调用流程，
    使用 mock 模拟响应，无需真实 API Key。
    同时说明如何切换到 Ollama 本地模型。
"""

import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Mock LLM 客户端（模拟 OpenAI API 响应）
# ---------------------------------------------------------------------------
class MockChatCompletion:
    """模拟 OpenAI ChatCompletion 响应。"""

    def __init__(self, content: str):
        self.choices = [type("Choice", (), {"message": type("Msg", (), {"content": content, "role": "assistant"})()})]
        self.usage = {"prompt_tokens": 50, "completion_tokens": len(content), "total_tokens": 50 + len(content)}


class MockLLMClient:
    """
    模拟 LLM API 客户端。

    真实使用时替换为:
        from openai import OpenAI
        client = OpenAI(api_key="your-key")

    使用 Ollama 本地模型时:
        client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    """

    MOCK_RESPONSES = {
        "default": "Python 是一种简洁优雅的编程语言，以其可读性和丰富的生态系统著称。",
        "code": "```python\ndef hello():\n    print('Hello, World!')\n```",
        "translate": "Hello, World! 的中文翻译是：你好，世界！",
    }

    def create(self, model="gpt-4", messages=None, temperature=0.7, stream=False):
        """模拟 chat.completions.create() 方法。"""
        user_msg = messages[-1]["content"] if messages else ""

        # 根据输入选择模拟响应
        if "代码" in user_msg or "code" in user_msg.lower():
            response_text = self.MOCK_RESPONSES["code"]
        elif "翻译" in user_msg or "translate" in user_msg.lower():
            response_text = self.MOCK_RESPONSES["translate"]
        else:
            response_text = self.MOCK_RESPONSES["default"]

        if stream:
            return self._stream_response(response_text)
        return MockChatCompletion(response_text)

    def _stream_response(self, text):
        """模拟流式响应。"""
        for char in text:
            yield type("Chunk", (), {
                "choices": [type("C", (), {"delta": type("D", (), {"content": char})()})]
            })()
            time.sleep(0.02)


# ---------------------------------------------------------------------------
# 演示函数
# ---------------------------------------------------------------------------
def demo_basic_call():
    """演示基础 API 调用。"""
    logger.info("--- 1. 基础 API 调用 ---")

    client = MockLLMClient()

    # 构造消息（OpenAI 格式）
    messages = [
        {"role": "system", "content": "你是一个 Python 编程助手。"},
        {"role": "user", "content": "请简单介绍一下 Python。"},
    ]

    # 调用 API
    response = client.create(model="gpt-4", messages=messages, temperature=0.7)

    # 解析响应
    reply = response.choices[0].message.content
    tokens = response.usage
    logger.info(f"模型回复: {reply}")
    logger.info(f"Token 用量: {tokens}")

    # --- 真实 OpenAI 调用代码 ---
    # from openai import OpenAI
    # client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    # response = client.chat.completions.create(
    #     model="gpt-4",
    #     messages=messages,
    #     temperature=0.7,
    # )
    # print(response.choices[0].message.content)


def demo_streaming():
    """演示流式响应。"""
    logger.info("\n--- 2. 流式响应 ---")

    client = MockLLMClient()
    messages = [{"role": "user", "content": "什么是 Python？"}]

    print("  流式输出: ", end="", flush=True)
    for chunk in client.create(model="gpt-4", messages=messages, stream=True):
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
    print()  # 换行


def demo_multi_turn():
    """演示多轮对话（维护对话历史）。"""
    logger.info("\n--- 3. 多轮对话 ---")

    client = MockLLMClient()

    # 对话历史
    conversation = [
        {"role": "system", "content": "你是一个 Python 编程助手。"},
    ]

    # 模拟多轮对话
    user_inputs = ["请介绍 Python", "写一段代码示例", "翻译 Hello World"]

    for user_input in user_inputs:
        conversation.append({"role": "user", "content": user_input})
        response = client.create(model="gpt-4", messages=conversation)
        reply = response.choices[0].message.content
        conversation.append({"role": "assistant", "content": reply})
        logger.info(f"  用户: {user_input}")
        logger.info(f"  助手: {reply[:60]}...")

    logger.info(f"对话历史共 {len(conversation)} 条消息")


def show_ollama_guide():
    """展示 Ollama 免费替代方案。"""
    logger.info("\n--- 4. Ollama 免费替代方案 ---")
    print("""
    Ollama 允许在本地运行开源 LLM，完全免费：

    # 安装 Ollama
    # macOS: brew install ollama
    # Linux: curl -fsSL https://ollama.ai/install.sh | sh

    # 下载模型
    ollama pull llama3.2      # Meta Llama 3.2 (3B)
    ollama pull qwen2.5       # 通义千问 2.5

    # Python 代码（兼容 OpenAI SDK）
    from openai import OpenAI
    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # Ollama 不需要真实 key
    )
    response = client.chat.completions.create(
        model="llama3.2",
        messages=[{"role": "user", "content": "你好"}],
    )
    print(response.choices[0].message.content)
    """)


def main():
    """主函数。"""
    print("=" * 60)
    print("  LLM API 调用演示（Mock 模拟，无需 API Key）")
    print("=" * 60)

    demo_basic_call()
    demo_streaming()
    demo_multi_turn()
    show_ollama_guide()

    print("✅ LLM API 演示完成！")


if __name__ == "__main__":
    main()
