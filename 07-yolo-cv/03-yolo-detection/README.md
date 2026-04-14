# YOLO 目标检测实战

> **模块：** 07-yolo-cv（计算机视觉）
> **难度：** 进阶
> **前置知识：** OpenCV 基础、YOLO 概念
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

使用 Ultralytics 库可以非常简单地进行 YOLO 目标检测。只需几行代码就能加载预训练模型、执行检测并可视化结果。

## 快速开始

```python
from ultralytics import YOLO

# 加载预训练模型
model = YOLO("yolov8n.pt")

# 执行检测
results = model("image.jpg")

# 查看结果
for result in results:
    boxes = result.boxes      # 检测框
    for box in boxes:
        cls = box.cls          # 类别
        conf = box.conf        # 置信度
        xyxy = box.xyxy        # 坐标 [x1, y1, x2, y2]
```

## 实战代码

**文件：**
- `examples/detection_demo.py` — 检测示例（检查依赖，未安装时给出说明）
- `download_model.py` — 模型自动下载脚本

```bash
pip install ultralytics
python examples/detection_demo.py
```

## 常见陷阱

- ⚠️ 首次运行会自动下载模型文件（约 6MB~130MB）
- ⚠️ GPU 加速需要安装 CUDA 版本的 PyTorch
- ⚠️ 图像路径包含中文可能导致读取失败
- ⚠️ 置信度阈值（conf）影响检测结果数量

> 💻 **完整可运行代码：** [detection_demo.py](examples/detection_demo.py)

## 参考资料

- [Ultralytics 检测文档](https://docs.ultralytics.com/tasks/detect/)
- [COCO 数据集类别](https://docs.ultralytics.com/datasets/detect/coco/)
