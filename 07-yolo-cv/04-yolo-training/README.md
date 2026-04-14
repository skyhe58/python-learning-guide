# YOLO 模型训练与微调

> **模块：** 07-yolo-cv（计算机视觉）
> **难度：** 进阶
> **前置知识：** YOLO 检测基础
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

当预训练模型无法满足特定场景需求时（如检测特定产品缺陷、识别自定义物体），需要使用自定义数据集对 YOLO 模型进行训练或微调。

## 训练流程

```
1. 数据准备 → 2. 数据标注 → 3. 数据集配置 → 4. 模型训练 → 5. 评估验证
```

### 1. 数据准备
- 收集目标场景的图像（建议每类 100+ 张）
- 图像格式：JPG/PNG
- 建议分辨率：640x640 或更高

### 2. 数据标注
- 工具推荐：[LabelImg](https://github.com/HumanSignal/labelImg)、[Roboflow](https://roboflow.com/)
- 输出 YOLO 格式标注文件

### 3. YOLO 标注格式

每张图像对应一个 `.txt` 标注文件：
```
<class_id> <x_center> <y_center> <width> <height>
```
- 所有值归一化到 [0, 1]
- 坐标相对于图像宽高

示例：
```
0 0.5 0.5 0.3 0.4
1 0.2 0.8 0.1 0.15
```

### 4. 数据集目录结构

```
dataset/
├── images/
│   ├── train/          # 训练集图像
│   │   ├── img001.jpg
│   │   └── ...
│   └── val/            # 验证集图像
│       ├── img101.jpg
│       └── ...
├── labels/
│   ├── train/          # 训练集标注
│   │   ├── img001.txt
│   │   └── ...
│   └── val/            # 验证集标注
│       ├── img101.txt
│       └── ...
└── data.yaml           # 数据集配置文件
```

### 5. data.yaml 配置

```yaml
path: ./dataset
train: images/train
val: images/val

nc: 2                    # 类别数量
names: ['cat', 'dog']    # 类别名称
```

## 训练代码

```python
from ultralytics import YOLO

# 加载预训练模型作为基础
model = YOLO("yolov8n.pt")

# 开始训练
results = model.train(
    data="dataset/data.yaml",
    epochs=100,           # 训练轮数
    imgsz=640,            # 图像大小
    batch=16,             # 批次大小
    lr0=0.01,             # 初始学习率
    device="0",           # GPU 设备（"cpu" 用 CPU）
    project="runs/train", # 输出目录
    name="my_model",      # 实验名称
)
```

## 实战代码

**文件：** `examples/training_intro.py`

```bash
pip install ultralytics
python examples/training_intro.py
```

## 常见陷阱

- ⚠️ 数据集太小容易过拟合，建议每类至少 100 张
- ⚠️ 标注质量直接影响模型效果
- ⚠️ 训练时间取决于数据量和 GPU 性能
- ⚠️ 学习率过大会导致训练不稳定

> 💻 **完整可运行代码：** [training_intro.py](examples/training_intro.py)

## 参考资料

- [Ultralytics 训练文档](https://docs.ultralytics.com/modes/train/)
- [数据集格式说明](https://docs.ultralytics.com/datasets/)
