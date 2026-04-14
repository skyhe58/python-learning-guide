# YOLO 实际应用案例

> **模块：** 07-yolo-cv（计算机视觉）
> **难度：** 进阶
> **前置知识：** YOLO 检测与训练
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

YOLO 目标检测在众多实际场景中有广泛应用。本节介绍几个典型的应用案例，帮助理解如何将 YOLO 技术落地到实际项目中。

## 应用案例

### 1. 人脸检测与识别

| 项目 | 说明 |
|------|------|
| 场景 | 门禁系统、考勤打卡、人脸支付 |
| 模型 | YOLOv8-face（专用人脸检测模型） |
| 关键点 | 人脸定位 + 关键点检测 + 特征提取 + 比对 |
| 挑战 | 光照变化、遮挡、角度变化 |

```python
# 人脸检测示例
from ultralytics import YOLO
model = YOLO("yolov8n-face.pt")
results = model("group_photo.jpg")
# 后续可接入 face_recognition 库进行人脸识别
```

### 2. 车辆检测与交通监控

| 项目 | 说明 |
|------|------|
| 场景 | 交通流量统计、违章检测、停车场管理 |
| 模型 | YOLOv8 + COCO 预训练（含 car/truck/bus 类别） |
| 关键点 | 车辆检测 + 跟踪 + 计数 + 车牌识别 |
| 挑战 | 遮挡、小目标、夜间检测 |

```python
# 车辆检测 + 跟踪
from ultralytics import YOLO
model = YOLO("yolov8n.pt")
# 使用 track 模式进行目标跟踪
results = model.track("traffic_video.mp4", persist=True, tracker="bytetrack.yaml")
```

### 3. 工业缺陷检测

| 项目 | 说明 |
|------|------|
| 场景 | 产品质检、PCB 板检测、表面缺陷检测 |
| 模型 | YOLOv8 + 自定义数据集训练 |
| 关键点 | 高精度检测 + 小缺陷识别 + 实时性 |
| 挑战 | 缺陷样本少、缺陷种类多、精度要求高 |

```python
# 自定义缺陷检测模型训练
model = YOLO("yolov8m.pt")  # 使用 medium 模型提高精度
model.train(
    data="defect_dataset/data.yaml",
    epochs=200,
    imgsz=1280,  # 更大的输入尺寸检测小缺陷
)
```

### 4. 安防监控

| 项目 | 说明 |
|------|------|
| 场景 | 入侵检测、异常行为识别、人群密度估计 |
| 模型 | YOLOv8 + 行为分析算法 |
| 关键点 | 实时检测 + 区域入侵判断 + 告警 |
| 挑战 | 7x24 小时运行、误报率控制 |

### 5. 医学影像分析

| 项目 | 说明 |
|------|------|
| 场景 | X 光片异常检测、细胞计数、病灶定位 |
| 模型 | YOLOv8 + 医学数据集训练 |
| 关键点 | 高精度 + 可解释性 + 辅助诊断 |
| 挑战 | 数据标注成本高、精度要求极高 |

### 6. 农业智能化

| 项目 | 说明 |
|------|------|
| 场景 | 果实成熟度检测、病虫害识别、杂草检测 |
| 模型 | YOLOv8 + 农业数据集 |
| 关键点 | 户外环境适应 + 实时性 |
| 挑战 | 光照变化大、目标形态多样 |

## 部署方案

| 部署方式 | 适用场景 | 工具 |
|----------|----------|------|
| Python 脚本 | 开发测试 | ultralytics |
| ONNX Runtime | 跨平台部署 | onnxruntime |
| TensorRT | NVIDIA GPU 加速 | tensorrt |
| OpenVINO | Intel 硬件加速 | openvino |
| TFLite | 移动端/嵌入式 | tensorflow-lite |
| CoreML | iOS/macOS | coreml-tools |

```python
# 模型导出
from ultralytics import YOLO
model = YOLO("best.pt")

model.export(format="onnx")        # 通用格式
model.export(format="engine")      # TensorRT（NVIDIA GPU）
model.export(format="openvino")    # Intel 加速
model.export(format="tflite")      # 移动端
```

## 性能优化建议

1. **模型选择**：根据场景选择合适的模型规格（n/s/m/l/x）
2. **输入尺寸**：小目标用大尺寸（1280），一般场景用 640
3. **批处理**：多张图像同时推理提高吞吐量
4. **模型量化**：INT8 量化可提速 2-4 倍，精度损失小
5. **硬件加速**：使用 TensorRT/OpenVINO 充分利用硬件

## 参考资料

- [Ultralytics 应用案例](https://docs.ultralytics.com/guides/)
- [YOLO 部署指南](https://docs.ultralytics.com/modes/export/)
- [目标跟踪文档](https://docs.ultralytics.com/modes/track/)
