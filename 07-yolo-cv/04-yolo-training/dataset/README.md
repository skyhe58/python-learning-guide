# 数据集准备说明

## 目录结构

```
dataset/
├── images/
│   ├── train/          # 训练集图像（80%）
│   └── val/            # 验证集图像（20%）
├── labels/
│   ├── train/          # 训练集标注
│   └── val/            # 验证集标注
├── data.yaml           # 数据集配置
└── README.md           # 本文件
```

## YOLO 标注格式

每张图像对应一个同名的 `.txt` 文件，每行一个目标：

```
<class_id> <x_center> <y_center> <width> <height>
```

- `class_id`: 类别编号（从 0 开始）
- `x_center`, `y_center`: 边界框中心坐标（归一化到 0-1）
- `width`, `height`: 边界框宽高（归一化到 0-1）

## data.yaml 示例

```yaml
path: ./dataset
train: images/train
val: images/val

nc: 3
names: ['cat', 'dog', 'bird']
```

## 标注工具推荐

| 工具 | 类型 | 特点 |
|------|------|------|
| [LabelImg](https://github.com/HumanSignal/labelImg) | 桌面端 | 免费，支持 YOLO 格式 |
| [Roboflow](https://roboflow.com/) | 在线 | 免费额度，自动增强 |
| [CVAT](https://cvat.ai/) | 在线/自部署 | 开源，功能强大 |
| [Label Studio](https://labelstud.io/) | 自部署 | 开源，支持多种任务 |

## 数据增强建议

训练时 Ultralytics 会自动进行数据增强，包括：
- 随机翻转、旋转
- 颜色抖动（亮度、对比度、饱和度）
- Mosaic 拼接（将 4 张图拼成 1 张）
- MixUp 混合
