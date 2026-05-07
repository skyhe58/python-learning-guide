#!/usr/bin/env python3
"""
Pandas 基础演示

模块: 06-ai-apps（AI 应用）
知识点: Pandas 基础（入门铺垫）
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    pip install pandas
    python pandas_demo.py

描述:
    演示 Pandas DataFrame 创建、查询、过滤、聚合（控制在 30 行以内）。
"""

import pandas as pd


def main():
    """Pandas 核心操作演示。"""
    # 创建 DataFrame
    df = pd.DataFrame({
        "姓名": ["张三", "李四", "王五", "赵六", "孙七"],
        "年龄": [25, 30, 28, 35, 22],
        "城市": ["北京", "上海", "北京", "深圳", "上海"],
        "薪资": [15000, 25000, 18000, 30000, 12000],
    })
    print("原始数据:")
    print(df)

    # 基本信息
    print(f"\n形状: {df.shape}, 列: {list(df.columns)}")
    print(f"统计摘要:\n{df.describe()}")

    # 过滤（类似 Java Stream.filter）
    high_salary = df[df["薪资"] > 15000]
    print(f"\n薪资 > 15000:\n{high_salary}")

    # 分组聚合（类似 Java Collectors.groupingBy）
    city_avg = df.groupby("城市")["薪资"].mean()
    print(f"\n各城市平均薪资:\n{city_avg}")

    # 排序
    sorted_df = df.sort_values("薪资", ascending=False)
    print(f"\n按薪资降序:\n{sorted_df[['姓名', '薪资']]}")

    # 新增列
    df["税后薪资"] = df["薪资"] * 0.85
    print(f"\n新增税后薪资列:\n{df[['姓名', '薪资', '税后薪资']]}")


if __name__ == "__main__":
    main()
