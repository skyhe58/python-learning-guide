# Jupyter Notebook 入门

> **模块：** 06-ai-apps（AI 应用）
> **难度：** 入门铺垫
> **前置知识：** Python 基础
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

Jupyter Notebook 是数据科学和 AI 开发的标准工具，支持在浏览器中交互式编写和运行 Python 代码。它的核心优势是"代码 + 文档 + 可视化"一体化，非常适合数据探索和实验。

**在后续 AI 应用中的用途：**
- 数据探索和可视化分析
- 模型训练实验和调参
- 结果展示和报告生成

## 安装与启动

```bash
# 安装
pip install jupyter

# 启动 Notebook
jupyter notebook

# 或使用 JupyterLab（更现代的界面）
pip install jupyterlab
jupyter lab
```

## 常用快捷键

| 快捷键 | 模式 | 功能 |
|--------|------|------|
| `Shift+Enter` | 通用 | 运行当前单元格并跳到下一个 |
| `Ctrl+Enter` | 通用 | 运行当前单元格 |
| `A` | 命令模式 | 在上方插入单元格 |
| `B` | 命令模式 | 在下方插入单元格 |
| `DD` | 命令模式 | 删除当前单元格 |
| `M` | 命令模式 | 切换为 Markdown 单元格 |
| `Y` | 命令模式 | 切换为代码单元格 |
| `Esc` | 编辑模式 | 进入命令模式 |
| `Enter` | 命令模式 | 进入编辑模式 |
| `Tab` | 编辑模式 | 代码补全 |

## VS Code 替代方案

如果你更习惯 VS Code，可以安装 **Jupyter 扩展**，直接在 VS Code 中使用 Notebook：

1. 安装扩展：`ms-toolsai.jupyter`
2. 创建 `.ipynb` 文件
3. 在 VS Code 中直接编辑和运行

## 实战代码

**文件：** `examples/jupyter_intro.py`

```bash
python examples/jupyter_intro.py
```

> 💻 **完整可运行代码：** [jupyter_intro.py](examples/jupyter_intro.py)

## 参考资料

- [Jupyter 官方文档](https://jupyter.org/documentation)
- [JupyterLab 文档](https://jupyterlab.readthedocs.io/)
