#!/usr/bin/env python3
"""
Jupyter Notebook 使用说明

模块: 06-ai-apps（AI 应用）
知识点: Jupyter Notebook 入门（入门铺垫）
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python jupyter_intro.py

描述:
    展示 Jupyter Notebook 的核心概念和使用方式（控制在 30 行以内）。
    本脚本模拟 Notebook 的单元格执行流程。
"""


def main():
    """模拟 Jupyter Notebook 的使用流程。"""
    print("=== Jupyter Notebook 使用指南 ===\n")

    # Cell 1: 安装和启动
    print("[Cell 1] 安装和启动:")
    print("  pip install jupyter")
    print("  jupyter notebook  # 浏览器打开 http://localhost:8888\n")

    # Cell 2: 魔法命令（Jupyter 特有功能）
    print("[Cell 2] 常用魔法命令:")
    magic_commands = {
        "%timeit": "测量代码执行时间",
        "%matplotlib inline": "在 Notebook 中内嵌显示图表",
        "!pip install xxx": "在 Notebook 中安装包",
        "%who": "列出当前命名空间中的变量",
        "%%writefile file.py": "将单元格内容写入文件",
    }
    for cmd, desc in magic_commands.items():
        print(f"  {cmd:30s} # {desc}")

    # Cell 3: 典型工作流
    print("\n[Cell 3] 典型 AI 开发工作流:")
    steps = [
        "1. 导入库 (import numpy, pandas, matplotlib)",
        "2. 加载数据 (pd.read_csv / pd.read_excel)",
        "3. 数据探索 (df.head(), df.describe(), df.info())",
        "4. 数据可视化 (plt.plot, plt.scatter)",
        "5. 数据预处理 (清洗、特征工程)",
        "6. 模型训练和评估",
        "7. 结果可视化和导出",
    ]
    for step in steps:
        print(f"  {step}")

    print("\n💡 提示: 在 VS Code 中安装 Jupyter 扩展也可以使用 .ipynb 文件")


if __name__ == "__main__":
    main()
