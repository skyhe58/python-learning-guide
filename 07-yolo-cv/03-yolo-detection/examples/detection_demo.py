#!/usr/bin/env python3
"""
YOLO 目标检测演示

模块: 07-yolo-cv（计算机视觉）
知识点: YOLO 目标检测实战
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    pip install ultralytics opencv-python
    python detection_demo.py

描述:
    演示使用 Ultralytics YOLO 进行目标检测。
    检查依赖是否安装，未安装时给出说明并使用模拟演示。
"""

import logging
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def check_ultralytics() -> bool:
    """检查 ultralytics 是否安装。"""
    try:
        import ultralytics
        logger.info(f"Ultralytics 版本: {ultralytics.__version__}")
        return True
    except ImportError:
        logger.warning("ultralytics 未安装")
        logger.info("安装命令: pip install ultralytics")
        return False


def demo_with_ultralytics():
    """使用真实 Ultralytics 库进行检测。"""
    from ultralytics import YOLO

    logger.info("--- YOLO 目标检测（真实模型）---")

    # 加载预训练模型（首次运行会自动下载）
    model = YOLO("yolov8n.pt")
    logger.info(f"模型加载完成: {model.model_name}")

    # 创建测试图像（使用 NumPy 生成）
    test_img = np.random.randint(0, 256, (640, 640, 3), dtype=np.uint8)

    # 执行检测
    results = model(test_img, conf=0.25, verbose=False)

    # 解析结果
    for result in results:
        boxes = result.boxes
        logger.info(f"检测到 {len(boxes)} 个目标")
        for box in boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].tolist()
            cls_name = result.names[cls_id]
            logger.info(f"  {cls_name}: 置信度={conf:.2f}, 位置={xyxy}")


def demo_simulated():
    """模拟 YOLO 检测流程（无需安装 ultralytics）。"""
    logger.info("--- YOLO 目标检测（模拟演示）---")
    logger.info("由于 ultralytics 未安装，使用模拟数据演示检测流程\n")

    # 模拟检测结果
    mock_detections = [
        {"class": "person", "confidence": 0.92, "bbox": [100, 50, 300, 400]},
        {"class": "car", "confidence": 0.87, "bbox": [350, 200, 600, 450]},
        {"class": "dog", "confidence": 0.78, "bbox": [50, 300, 200, 500]},
    ]

    # 模拟检测流程
    logger.info("Step 1: 加载模型")
    logger.info("  model = YOLO('yolov8n.pt')  # 自动下载 ~6MB")

    logger.info("\nStep 2: 执行检测")
    logger.info("  results = model('image.jpg', conf=0.25)")

    logger.info("\nStep 3: 解析结果")
    logger.info(f"  检测到 {len(mock_detections)} 个目标:")
    for det in mock_detections:
        logger.info(f"    {det['class']}: 置信度={det['confidence']:.2f}, "
                     f"位置={det['bbox']}")

    logger.info("\nStep 4: 可视化")
    logger.info("  result.plot()  # 在图像上绘制检测框")
    logger.info("  result.save()  # 保存结果图像")

    # 展示完整代码
    print("\n--- 完整检测代码 ---")
    print("""
    from ultralytics import YOLO

    # 加载模型
    model = YOLO("yolov8n.pt")  # nano 模型，速度最快
    # model = YOLO("yolov8s.pt")  # small 模型，精度更高

    # 检测图像
    results = model("image.jpg", conf=0.25)

    # 遍历结果
    for result in results:
        for box in result.boxes:
            cls_name = result.names[int(box.cls[0])]
            confidence = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            print(f"{cls_name}: {confidence:.2f} at [{x1:.0f},{y1:.0f},{x2:.0f},{y2:.0f}]")

    # 保存可视化结果
    results[0].save("result.jpg")

    # 检测视频
    # results = model("video.mp4", stream=True)
    # for result in results:
    #     frame = result.plot()
    """)


def main():
    """主函数。"""
    print("=" * 60)
    print("  YOLO 目标检测演示")
    print("=" * 60)

    if check_ultralytics():
        demo_with_ultralytics()
    else:
        demo_simulated()

    print("\n✅ YOLO 检测演示完成！")


if __name__ == "__main__":
    main()
