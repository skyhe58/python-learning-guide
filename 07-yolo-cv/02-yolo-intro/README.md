# YOLO 模型介绍与版本对比

> **模块：** 07-yolo-cv（计算机视觉）
> **难度：** 入门
> **前置知识：** Python 基础
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

YOLO（You Only Look Once）是一种实时目标检测算法，将目标检测问题转化为单次回归问题。与传统的两阶段检测器（如 Faster R-CNN）不同，YOLO 只需要一次前向传播就能同时预测所有目标的位置和类别。

## YOLO 发展历程

```
YOLOv1 (2016) → YOLOv2 (2017) → YOLOv3 (2018) → YOLOv4 (2020)
    → YOLOv5 (2020, Ultralytics) → YOLOv7 (2022)
    → YOLOv8 (2023, Ultralytics) → YOLOv11 (2024, Ultralytics)
```

## 版本对比

| 特性 | YOLOv5 | YOLOv8 | YOLOv11 |
|------|--------|--------|---------|
| 开发者 | Ultralytics | Ultralytics | Ultralytics |
| 发布年份 | 2020 | 2023 | 2024 |
| 框架 | PyTorch | PyTorch | PyTorch |
| 架构 | CSPDarknet + PANet | CSPDarknet + C2f | 改进 C2f + SPPF |
| Anchor | Anchor-based | Anchor-free | Anchor-free |
| 任务支持 | 检测 | 检测/分割/分类/姿态 | 检测/分割/分类/姿态/OBB |
| API 风格 | 脚本式 | 统一 Python API | 统一 Python API |
| 速度 | 快 | 更快 | 最快 |
| 精度 (mAP) | 高 | 更高 | 最高 |
| 社区成熟度 | 非常成熟 | 成熟 | 快速增长 |

## 模型规格对比（YOLOv8 系列）

| 模型 | 参数量 | mAP50-95 | 速度 (ms) | 适用场景 |
|------|--------|----------|-----------|----------|
| YOLOv8n | 3.2M | 37.3 | 1.2 | 边缘设备/移动端 |
| YOLOv8s | 11.2M | 44.9 | 1.9 | 轻量级应用 |
| YOLOv8m | 25.9M | 50.2 | 4.0 | 平衡精度和速度 |
| YOLOv8l | 43.7M | 52.9 | 6.1 | 高精度需求 |
| YOLOv8x | 68.2M | 53.9 | 9.8 | 最高精度 |

## 支持的任务类型

| 任务 | 说明 | 输出 |
|------|------|------|
| Detection | 目标检测 | 边界框 + 类别 + 置信度 |
| Segmentation | 实例分割 | 像素级掩码 |
| Classification | 图像分类 | 类别 + 置信度 |
| Pose | 姿态估计 | 关键点坐标 |
| OBB | 旋转目标检测 | 旋转边界框 |

## 选型建议

```
需要实时检测（>30 FPS）？
├── 是 → 边缘设备？
│   ├── 是 → YOLOv8n / YOLOv11n
│   └── 否 → YOLOv8s / YOLOv11s
└── 否 → 追求最高精度？
    ├── 是 → YOLOv8x / YOLOv11x
    └── 否 → YOLOv8m / YOLOv11m（推荐）
```

## YOLO vs 其他检测器

| 特性 | YOLO | Faster R-CNN | SSD |
|------|------|-------------|-----|
| 检测方式 | 单阶段 | 两阶段 | 单阶段 |
| 速度 | 非常快 | 较慢 | 快 |
| 精度 | 高 | 最高 | 中等 |
| 小目标 | 一般 | 好 | 一般 |
| 部署难度 | 简单 | 复杂 | 中等 |
| 推荐场景 | 实时应用 | 高精度需求 | 嵌入式设备 |

## 参考资料

- [Ultralytics 官方文档](https://docs.ultralytics.com/)
- [YOLOv8 GitHub](https://github.com/ultralytics/ultralytics)
- [YOLO 论文原文](https://arxiv.org/abs/1506.02640)
