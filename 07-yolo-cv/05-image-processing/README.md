# 图像预处理与后处理

> **模块：** 07-yolo-cv（计算机视觉）
> **难度：** 进阶
> **前置知识：** OpenCV 基础、NumPy
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

在目标检测流程中，图像预处理和后处理是关键环节：
- **预处理**：将原始图像转换为模型可接受的输入格式
- **后处理**：将模型输出转换为有意义的检测结果

## 预处理流程

```
原始图像 → 缩放到固定尺寸 → 归一化 → 通道转换 → 添加 batch 维度
```

## 后处理流程

```
模型输出 → 解码边界框 → 置信度过滤 → NMS 去重 → 坐标还原 → 可视化
```

## 核心概念

| 概念 | 说明 |
|------|------|
| Resize | 将图像缩放到模型输入尺寸（如 640x640） |
| Normalize | 像素值从 [0,255] 归一化到 [0,1] |
| Letterbox | 等比缩放并填充灰边，保持宽高比 |
| NMS | 非极大值抑制，去除重叠的检测框 |
| IoU | 交并比，衡量两个框的重叠程度 |

## 实战代码

**文件：** `examples/image_processing_demo.py`

```bash
pip install numpy opencv-python
python examples/image_processing_demo.py
```

> 💻 **完整可运行代码：** [image_processing_demo.py](examples/image_processing_demo.py)

## 参考资料

- [OpenCV 图像处理教程](https://docs.opencv.org/4.x/d2/d96/tutorial_py_table_of_contents_imgproc.html)
- [NMS 算法详解](https://towardsdatascience.com/non-maximum-suppression-nms-93ce178e177c)
