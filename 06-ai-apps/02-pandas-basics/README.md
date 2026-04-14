# Pandas 基础

> **模块：** 06-ai-apps（AI 应用）
> **难度：** 入门铺垫
> **前置知识：** Python 基础、NumPy 基础
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

Pandas 是 Python 数据分析的核心库，提供 `DataFrame`（二维表格）和 `Series`（一维序列）两种数据结构。它类似于 Java 中的 Stream API + 数据库查询的结合体。

**在后续 AI 应用中的用途：**
- 数据预处理和清洗（训练数据准备）
- 特征工程（从原始数据提取特征）
- 结果分析和可视化

## Java 对比

| 特性 | Java (Stream API) | Python (Pandas) |
|------|-------------------|-----------------|
| 数据过滤 | `.filter(x -> x > 5)` | `df[df['col'] > 5]` |
| 数据转换 | `.map(x -> x * 2)` | `df['col'] * 2` |
| 分组聚合 | `Collectors.groupingBy()` | `df.groupby('col').mean()` |
| 排序 | `.sorted()` | `df.sort_values('col')` |

## 实战代码

**文件：** `examples/pandas_demo.py`

```bash
pip install pandas
python examples/pandas_demo.py
```

> 💻 **完整可运行代码：** [pandas_demo.py](examples/pandas_demo.py)

## 参考资料

- [Pandas 官方文档](https://pandas.pydata.org/docs/)
- [10 分钟入门 Pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
