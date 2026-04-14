#!/usr/bin/env python3
"""
Matplotlib 绘图演示

模块: 06-ai-apps（AI 应用）
知识点: Matplotlib 绘图（入门铺垫）
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    pip install matplotlib
    python matplotlib_demo.py

描述:
    演示折线图、柱状图、散点图的绘制（每种控制在 30 行以内）。
    使用 Agg 后端保存为文件，无需 GUI 环境。
"""

import matplotlib
matplotlib.use("Agg")  # 非 GUI 后端，适合服务器环境
import matplotlib.pyplot as plt
import numpy as np


def main():
    """绘制三种基础图表。"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # 1. 折线图 — 模拟训练 loss 曲线
    epochs = range(1, 11)
    loss = [0.9, 0.7, 0.5, 0.35, 0.25, 0.18, 0.13, 0.1, 0.08, 0.06]
    axes[0].plot(epochs, loss, "b-o", label="训练 Loss")
    axes[0].set_title("训练 Loss 曲线")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].legend()
    axes[0].grid(True)

    # 2. 柱状图 — 框架流行度对比
    frameworks = ["Django", "FastAPI", "Flask", "Scrapy"]
    stars = [72000, 65000, 64000, 48000]
    colors = ["#2196F3", "#4CAF50", "#FF9800", "#9C27B0"]
    axes[1].bar(frameworks, stars, color=colors)
    axes[1].set_title("Python 框架 GitHub Stars")
    axes[1].set_ylabel("Stars")

    # 3. 散点图 — 模拟数据分布
    np.random.seed(42)
    x = np.random.randn(50)
    y = 2 * x + np.random.randn(50) * 0.5
    axes[2].scatter(x, y, c=y, cmap="coolwarm", alpha=0.7)
    axes[2].set_title("数据分布散点图")
    axes[2].set_xlabel("X")
    axes[2].set_ylabel("Y")

    plt.tight_layout()
    plt.savefig("charts_demo.png", dpi=100)
    print("✅ 图表已保存为 charts_demo.png")
    print("  包含: 折线图、柱状图、散点图")


if __name__ == "__main__":
    main()
