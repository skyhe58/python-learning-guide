#!/usr/bin/env python3
"""
YOLO 模型自动下载脚本

模块: 07-yolo-cv（计算机视觉）
知识点: YOLO 目标检测
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    pip install ultralytics
    python download_model.py

描述:
    自动下载 YOLO 预训练模型文件。
    支持选择不同规格的模型。
"""

import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

MODELS = {
    "yolov8n": {"size": "~6MB", "desc": "Nano - 速度最快，适合边缘设备"},
    "yolov8s": {"size": "~22MB", "desc": "Small - 平衡速度和精度"},
    "yolov8m": {"size": "~52MB", "desc": "Medium - 较高精度"},
    "yolov8l": {"size": "~87MB", "desc": "Large - 高精度"},
    "yolov8x": {"size": "~131MB", "desc": "Extra Large - 最高精度"},
}


def download_model(model_name: str = "yolov8n"):
    """下载指定的 YOLO 模型。"""
    try:
        from ultralytics import YOLO
    except ImportError:
        logger.error("ultralytics 未安装！")
        logger.info("请先安装: pip install ultralytics")
        sys.exit(1)

    model_file = f"{model_name}.pt"
    info = MODELS.get(model_name, {})
    logger.info(f"下载模型: {model_file}")
    logger.info(f"  大小: {info.get('size', '未知')}")
    logger.info(f"  说明: {info.get('desc', '未知')}")

    try:
        model = YOLO(model_file)
        logger.info(f"✅ 模型 {model_file} 下载/加载成功！")
        return model
    except Exception as e:
        logger.error(f"下载失败: {e}")
        return None


def main():
    """主函数。"""
    print("=" * 60)
    print("  YOLO 模型下载工具")
    print("=" * 60)

    print("\n可用模型:")
    for name, info in MODELS.items():
        print(f"  {name:10s} {info['size']:>8s}  {info['desc']}")

    # 默认下载 nano 模型
    model_name = sys.argv[1] if len(sys.argv) > 1 else "yolov8n"
    print(f"\n下载模型: {model_name}")
    print("(可通过命令行参数指定: python download_model.py yolov8s)\n")

    download_model(model_name)


if __name__ == "__main__":
    main()
