#!/usr/bin/env python3
"""
AI Agent 智能体概念演示

模块: 06-ai-apps（AI 应用）
知识点: AI Agent（应用进阶）
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python agent_demo.py

描述:
    用纯 Python 模拟 AI Agent 的工作流程：
    任务分析 → 工具选择 → 执行 → 观察 → 决策。
    演示 ReAct 模式和 Function Calling 概念。
"""

import logging
import math
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# 工具定义（Agent 可调用的外部功能）
# ---------------------------------------------------------------------------
class CalculatorTool:
    """计算器工具。"""
    name = "calculator"
    description = "执行数学计算，支持加减乘除和常用函数"

    @staticmethod
    def run(expression: str) -> str:
        try:
            allowed = {"sqrt": math.sqrt, "pow": pow, "abs": abs}
            result = eval(expression, {"__builtins__": {}}, allowed)
            return f"计算结果: {result}"
        except Exception as e:
            return f"计算错误: {e}"


class DateTimeTool:
    """日期时间工具。"""
    name = "datetime"
    description = "获取当前日期时间信息"

    @staticmethod
    def run(query: str) -> str:
        now = datetime.now()
        if "日期" in query or "date" in query.lower():
            return f"当前日期: {now.strftime('%Y-%m-%d')}"
        if "时间" in query or "time" in query.lower():
            return f"当前时间: {now.strftime('%H:%M:%S')}"
        return f"当前日期时间: {now.strftime('%Y-%m-%d %H:%M:%S')}"


class SearchTool:
    """模拟搜索工具。"""
    name = "search"
    description = "搜索知识库获取信息"

    KNOWLEDGE = {
        "python": "Python 是一种高级编程语言，由 Guido van Rossum 创建。",
        "fastapi": "FastAPI 是高性能 Python Web 框架，支持异步。",
        "yolo": "YOLO 是实时目标检测算法，YOLOv8 最新。",
    }

    @staticmethod
    def run(query: str) -> str:
        query_lower = query.lower()
        for key, value in SearchTool.KNOWLEDGE.items():
            if key in query_lower:
                return f"搜索结果: {value}"
        return "未找到相关信息"


# ---------------------------------------------------------------------------
# 简单 Agent 实现
# ---------------------------------------------------------------------------
class SimpleAgent:
    """
    简单的 ReAct Agent 实现。

    ReAct 模式: Thought → Action → Observation → ... → Final Answer
    """

    def __init__(self, tools: list):
        self.tools = {tool.name: tool for tool in tools}
        self.max_steps = 5

    def _select_tool(self, task: str) -> tuple[str, str]:
        """根据任务选择工具（模拟 LLM 的 Function Calling）。"""
        task_lower = task.lower()
        if any(w in task_lower for w in ["计算", "加", "减", "乘", "除", "sqrt"]):
            expr = task.split("计算")[-1].strip() if "计算" in task else task
            return "calculator", expr
        if any(w in task_lower for w in ["日期", "时间", "几号", "几点"]):
            return "datetime", task
        if any(w in task_lower for w in ["什么是", "搜索", "查找", "介绍"]):
            return "search", task
        return "", task

    def run(self, task: str) -> str:
        """执行任务（ReAct 循环）。"""
        logger.info(f"任务: {task}")
        steps = []

        for step in range(1, self.max_steps + 1):
            # Thought: 分析当前状态
            logger.info(f"  [Step {step}] Thought: 分析任务...")

            # Action: 选择工具
            tool_name, tool_input = self._select_tool(task)

            if not tool_name:
                # 无需工具，直接回答
                answer = f"关于'{task}'，这是一个通用问题，建议查阅相关文档。"
                logger.info(f"  [Step {step}] Final Answer: {answer}")
                return answer

            logger.info(f"  [Step {step}] Action: 使用工具 [{tool_name}]({tool_input})")

            # Execute: 执行工具
            tool = self.tools.get(tool_name)
            if tool:
                observation = tool.run(tool_input)
            else:
                observation = f"工具 {tool_name} 不可用"

            logger.info(f"  [Step {step}] Observation: {observation}")
            steps.append({"thought": "分析任务", "action": tool_name, "observation": observation})

            # 判断是否完成
            if observation and "错误" not in observation:
                final = f"根据工具执行结果: {observation}"
                logger.info(f"  [Step {step}] Final Answer: {final}")
                return final

        return "达到最大步数，任务未完成"


def main():
    """主函数。"""
    print("=" * 60)
    print("  AI Agent 智能体演示")
    print("  模拟 ReAct 模式: Thought → Action → Observation")
    print("=" * 60)

    # 初始化 Agent
    tools = [CalculatorTool(), DateTimeTool(), SearchTool()]
    agent = SimpleAgent(tools)

    # 测试不同类型的任务
    tasks = [
        "计算 sqrt(144) + 10",
        "现在是什么日期？",
        "什么是 FastAPI？",
        "搜索 YOLO 相关信息",
    ]

    for task in tasks:
        print(f"\n{'─' * 40}")
        result = agent.run(task)
        print(f"  结果: {result}")

    print(f"\n{'─' * 40}")
    print("✅ AI Agent 演示完成！")


if __name__ == "__main__":
    main()
