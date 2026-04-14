#!/usr/bin/env python3
"""
YOLO 模型训练流程说明

模块: 07-yolo-cv（计算机视觉）
知识点: YOLO 模型训练与微调
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python training_intro.py

描述:
    展示 YOLO 模型训练的完整流程和关键参数说明。
    由于训练需要 GPU 和数据集，本脚本以说明为主。
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def show_training_workflow():
    """展示训练工作流程。"""
    logger.info("--- YOLO 训练工作流程 ---")

    steps = [
        ("1. 数据收集", "收集目标场景图像，建议每类 100+ 张"),
        ("2. 数据标注", "使用 LabelImg/Roboflow 标注边界框"),
        ("3. 数据集划分", "训练集:验证集 = 8:2"),
        ("4. 配置 data.yaml", "指定路径、类别数、类别名"),
        ("5. 选择基础模型", "yolov8n(快) / yolov8m(平衡) / yolov8x(精)"),
        ("6. 开始训练", "model.train(data='data.yaml', epochs=100)"),
        ("7. 评估验证", "model.val() 查看 mAP 等指标"),
        ("8. 导出部署", "model.export(format='onnx') 导出模型"),
    ]

    for step, desc in steps:
        logger.info(f"  {step}: {desc}")


def show_training_params():
    """展示关键训练参数。"""
    logger.info("\n--- 关键训练参数 ---")

    params = {
        "epochs": ("100", "训练轮数，小数据集 50-100，大数据集 200+"),
        "imgsz": ("640", "输入图像大小，越大精度越高但越慢"),
        "batch": ("16", "批次大小，根据 GPU 显存调整"),
        "lr0": ("0.01", "初始学习率，过大不稳定，过小收敛慢"),
        "device": ("0", "GPU 编号，'cpu' 用 CPU 训练"),
        "patience": ("50", "早停耐心值，验证集指标不提升时停止"),
        "augment": ("True", "数据增强，提升泛化能力"),
        "pretrained": ("True", "使用预训练权重，加速收敛"),
    }

    for param, (default, desc) in params.items():
        logger.info(f"  {param:12s} = {default:6s}  # {desc}")


def show_training_code():
    """展示完整训练代码。"""
    logger.info("\n--- 完整训练代码 ---")
    print("""
    from ultralytics import YOLO

    # ===== 训练 =====
    model = YOLO("yolov8n.pt")  # 加载预训练模型
    results = model.train(
        data="dataset/data.yaml",
        epochs=100,
        imgsz=640,
        batch=16,
        device="0",
    )

    # ===== 验证 =====
    metrics = model.val()
    print(f"mAP50: {metrics.box.map50:.3f}")
    print(f"mAP50-95: {metrics.box.map:.3f}")

    # ===== 预测 =====
    results = model("test_image.jpg")
    results[0].save("result.jpg")

    # ===== 导出 =====
    model.export(format="onnx")    # ONNX 格式
    model.export(format="torchscript")  # TorchScript
    # 支持格式: onnx, torchscript, tflite, coreml, openvino 等
    """)


def show_evaluation_metrics():
    """展示评估指标说明。"""
    logger.info("\n--- 评估指标说明 ---")

    metrics = [
        ("mAP50", "IoU=0.5 时的平均精度，最常用指标"),
        ("mAP50-95", "IoU=0.5:0.95 的平均精度，更严格"),
        ("Precision", "精确率，检测结果中正确的比例"),
        ("Recall", "召回率，实际目标被检测到的比例"),
        ("F1-Score", "精确率和召回率的调和平均"),
        ("IoU", "交并比，预测框与真实框的重叠程度"),
    ]

    for name, desc in metrics:
        logger.info(f"  {name:12s}: {desc}")


def main():
    """主函数。"""
    print("=" * 60)
    print("  YOLO 模型训练流程说明")
    print("  实际训练需要 GPU 和标注数据集")
    print("=" * 60)

    show_training_workflow()
    show_training_params()
    show_evaluation_metrics()
    show_training_code()

    print("\n✅ 训练流程说明完成！")


if __name__ == "__main__":
    main()
