# NumPy 基础

> **模块：** 06-ai-apps（AI 应用）
> **难度：** 入门铺垫
> **前置知识：** Python 基础（列表、循环）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

NumPy 是 Python 科学计算的基础库，提供高性能的多维数组对象 `ndarray`。在 AI 领域，几乎所有数据（图像、文本向量、模型参数）最终都以 NumPy 数组的形式存在。

**在后续 AI 应用中的用途：**
- 图像数据表示（OpenCV 图像就是 NumPy 数组）
- 向量嵌入（Embedding）的存储和计算
- 模型输入/输出的数据格式

## Java 对比

| 特性 | Java | Python (NumPy) |
|------|------|----------------|
| 数组创建 | `int[] arr = new int[10]` | `np.zeros(10)` |
| 多维数组 | `int[][] matrix` | `np.array([[1,2],[3,4]])` |
| 数组运算 | 手动循环 | 向量化运算 `a + b` |
| 矩阵乘法 | 手动实现 | `a @ b` 或 `np.dot(a, b)` |

## 实战代码

**文件：** `examples/numpy_demo.py`

```bash
pip install numpy
python examples/numpy_demo.py
```

> 💻 **完整可运行代码：** [numpy_demo.py](examples/numpy_demo.py)

## 参考资料

- [NumPy 官方文档](https://numpy.org/doc/)
- [NumPy 快速入门](https://numpy.org/doc/stable/user/quickstart.html)
