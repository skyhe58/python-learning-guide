# OpenCV 图像基础

> **模块：** 07-yolo-cv（计算机视觉）
> **难度：** 入门
> **前置知识：** Python 基础、NumPy 基础
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

OpenCV（Open Source Computer Vision Library）是最流行的计算机视觉库。在 Python 中，OpenCV 的图像本质上就是 NumPy 数组，因此掌握 NumPy 是学习 OpenCV 的前提。

## 核心概念

| 概念 | 说明 |
|------|------|
| 图像表示 | NumPy 数组，形状为 (高, 宽, 通道) |
| 颜色空间 | BGR（OpenCV 默认）、RGB、灰度、HSV |
| 像素操作 | 直接通过数组索引访问和修改像素 |
| 图像变换 | 缩放、旋转、裁剪、翻转 |
| 滤波 | 模糊、锐化、边缘检测 |

## Java 对比

| 特性 | Java | Python (OpenCV) |
|------|------|-----------------|
| 图像读取 | `ImageIO.read()` | `cv2.imread()` |
| 图像显示 | `JFrame + JLabel` | `cv2.imshow()` |
| 像素操作 | `BufferedImage.getRGB()` | `img[y, x]` |
| 图像缩放 | `Graphics2D.drawImage()` | `cv2.resize()` |

## 实战代码

**文件：** `examples/opencv_demo.py`

```bash
pip install opencv-python numpy
python examples/opencv_demo.py
```

演示内容：
- 使用 NumPy 生成测试图像（不依赖外部图片文件）
- 颜色空间转换
- 基础图像操作（缩放、裁剪、绘制）
- 图像滤波

## 常见陷阱

- ⚠️ OpenCV 默认颜色空间是 BGR，不是 RGB
- ⚠️ `cv2.imshow()` 在无 GUI 环境（服务器）会报错，用 `cv2.imwrite()` 保存
- ⚠️ 图像坐标是 (y, x)，不是 (x, y)
- ⚠️ `cv2.resize()` 参数是 (宽, 高)，与数组 shape (高, 宽) 相反

> 💻 **完整可运行代码：** [opencv_demo.py](examples/opencv_demo.py)

## 参考资料

- [OpenCV Python 教程](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [OpenCV 官方文档](https://docs.opencv.org/)
