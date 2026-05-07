#!/usr/bin/env python3
"""
NumPy 基础演示

模块: 06-ai-apps（AI 应用）
知识点: NumPy 基础（入门铺垫）
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    pip install numpy
    python numpy_demo.py

描述:
    演示 NumPy 数组创建、基础运算和常用操作（控制在 30 行以内）。
"""

import numpy as np


def main():
    """NumPy 核心操作演示。"""
    # 数组创建
    a = np.array([1, 2, 3, 4, 5])
    zeros = np.zeros((2, 3))          # 2x3 全零矩阵
    ones = np.ones((3, 3))            # 3x3 全一矩阵
    rng = np.arange(0, 10, 2)         # [0, 2, 4, 6, 8]
    print(f"数组: {a}, 形状: {a.shape}, 类型: {a.dtype}")
    print(f"全零矩阵:\n{zeros}")
    print(f"等差数列: {rng}")

    # 向量化运算（无需循环，比 Java 简洁得多）
    b = np.array([10, 20, 30, 40, 50])
    print(f"加法: {a + b}")
    print(f"乘法: {a * b}")
    print(f"均值: {a.mean()}, 最大值: {a.max()}, 求和: {a.sum()}")

    # 矩阵运算
    m1 = np.array([[1, 2], [3, 4]])
    m2 = np.array([[5, 6], [7, 8]])
    print(f"矩阵乘法:\n{m1 @ m2}")

    # 索引和切片
    arr = np.arange(12).reshape(3, 4)
    print(f"3x4 矩阵:\n{arr}")
    print(f"第 1 行: {arr[0]}, 第 2 列: {arr[:, 1]}")


if __name__ == "__main__":
    main()
