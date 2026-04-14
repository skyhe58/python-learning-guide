# 计算机视觉 速查卡片

## 核心概念

| 概念 | 说明 | 示例 |
|------|------|------|
| OpenCV | 计算机视觉库 | `cv2.imread("img.jpg")` |
| NumPy 图像 | 图像 = NumPy 数组 | `img.shape → (H, W, C)` |
| BGR | OpenCV 默认颜色空间 | `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` |
| YOLO | 实时目标检测 | `model("image.jpg")` |
| NMS | 非极大值抑制 | 去除重叠检测框 |
| IoU | 交并比 | 衡量框重叠程度 |
| mAP | 平均精度 | 模型评估指标 |

## OpenCV 速查

```python
import cv2
import numpy as np

# 读取/保存图像
img = cv2.imread("image.jpg")          # 读取（BGR 格式）
cv2.imwrite("output.jpg", img)         # 保存

# 颜色空间转换
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 图像变换
resized = cv2.resize(img, (640, 640))  # 缩放（宽, 高）
flipped = cv2.flip(img, 1)            # 水平翻转
cropped = img[y1:y2, x1:x2]           # 裁剪

# 绘制
cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)  # 矩形
cv2.circle(img, (cx,cy), r, (0,0,255), 2)             # 圆
cv2.putText(img, "text", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

# 滤波
blurred = cv2.GaussianBlur(img, (5,5), 0)
edges = cv2.Canny(img, 100, 200)
```

## YOLO 速查

```python
from ultralytics import YOLO

# 加载模型
model = YOLO("yolov8n.pt")    # nano（最快）
model = YOLO("yolov8m.pt")    # medium（平衡）
model = YOLO("best.pt")       # 自定义训练的模型

# 检测
results = model("image.jpg", conf=0.25)
for result in results:
    for box in result.boxes:
        cls = result.names[int(box.cls[0])]
        conf = float(box.conf[0])
        x1, y1, x2, y2 = box.xyxy[0].tolist()

# 训练
model.train(data="data.yaml", epochs=100, imgsz=640)

# 验证
metrics = model.val()

# 导出
model.export(format="onnx")

# 跟踪
results = model.track("video.mp4", persist=True)
```

## YOLO 数据集格式

```yaml
# data.yaml
path: ./dataset
train: images/train
val: images/val
nc: 3
names: ['cat', 'dog', 'bird']
```

```
# 标注文件 (每行一个目标)
# class_id x_center y_center width height (归一化 0-1)
0 0.5 0.5 0.3 0.4
1 0.2 0.8 0.1 0.15
```

## 常见陷阱

- ⚠️ OpenCV 颜色空间是 BGR，不是 RGB
- ⚠️ `cv2.resize()` 参数是 (宽, 高)，数组 shape 是 (高, 宽)
- ⚠️ 图像坐标是 (y, x)，不是 (x, y)
- ⚠️ YOLO 首次运行会自动下载模型文件
- ⚠️ 训练数据太少容易过拟合
- ⚠️ `cv2.imshow()` 在无 GUI 环境会报错
- ⚠️ 图像路径含中文可能导致读取失败

## 面试高频考点

- YOLO 的单阶段检测原理
- NMS 非极大值抑制算法
- IoU 计算方法
- mAP 评估指标的含义
- Anchor-based vs Anchor-free 的区别
- 图像预处理流程（归一化、Letterbox）
- 模型量化和部署优化
- YOLOv5 vs YOLOv8 的改进点
