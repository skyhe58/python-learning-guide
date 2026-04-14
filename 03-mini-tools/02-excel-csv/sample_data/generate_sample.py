#!/usr/bin/env python3
"""
生成示例 CSV 数据

模块: 03-小工具开发
知识点: Excel/CSV 数据处理
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python generate_sample.py

描述:
    生成一个包含销售数据的示例 CSV 文件，用于测试 excel_processor.py。
"""

import csv
import random
from pathlib import Path


# 示例产品数据
PRODUCTS = [
    ("笔记本电脑", "电子产品", 5999.00),
    ("机械键盘", "电子产品", 399.00),
    ("无线鼠标", "电子产品", 129.00),
    ("显示器", "电子产品", 2499.00),
    ("Python 编程书", "图书", 79.90),
    ("算法导论", "图书", 128.00),
    ("办公椅", "办公用品", 899.00),
    ("笔记本", "办公用品", 29.90),
    ("签字笔套装", "办公用品", 45.00),
    ("台灯", "办公用品", 199.00),
]


def main():
    """生成示例 CSV 文件。"""
    script_dir = Path(__file__).parent
    output_file = script_dir / "sales.csv"

    random.seed(42)  # 固定种子，确保可重复

    rows = []
    for i in range(20):
        product, category, base_price = random.choice(PRODUCTS)
        # 价格小幅波动
        price = round(base_price * random.uniform(0.9, 1.1), 2)
        quantity = random.randint(1, 10)
        # 生成日期
        month = random.randint(1, 6)
        day = random.randint(1, 28)
        date = f"2025-{month:02d}-{day:02d}"
        rows.append({
            "日期": date,
            "产品": product,
            "类别": category,
            "金额": f"{price:.2f}",
            "数量": str(quantity),
        })

    # 按日期排序
    rows.sort(key=lambda r: r["日期"])

    headers = ["日期", "产品", "类别", "金额", "数量"]
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"已生成示例数据: {output_file}")
    print(f"共 {len(rows)} 行数据，包含 {len(headers)} 列: {', '.join(headers)}")


if __name__ == "__main__":
    main()
