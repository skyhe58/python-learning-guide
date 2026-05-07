#!/usr/bin/env python3
"""
图像预处理与后处理演示

模块: 07-yolo-cv（计算机视觉）
知识点: 图像预处理与后处理
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    pip install numpy
    python image_processing_demo.py

描述:
    演示目标检测中的图像预处理（缩放、归一化、Letterbox）
    和后处理（NMS 非极大值抑制）。使用 NumPy 实现，不依赖外部图片。
"""

import logging
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def demo_preprocessing():
    """演示图像预处理。"""
    logger.info("--- 1. 图像预处理 ---")

    # 模拟一张 480x640 的彩色图像
    img = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
    logger.info(f"原始图像: shape={img.shape}, dtype={img.dtype}")

    # 1. 缩放到模型输入尺寸
    target_size = (640, 640)
    # 简单缩放（实际用 cv2.resize）
    h_ratio = target_size[0] / img.shape[0]
    w_ratio = target_size[1] / img.shape[1]
    h_idx = (np.arange(target_size[0]) / h_ratio).astype(int).clip(0, img.shape[0] - 1)
    w_idx = (np.arange(target_size[1]) / w_ratio).astype(int).clip(0, img.shape[1] - 1)
    resized = img[np.ix_(h_idx, w_idx)]
    logger.info(f"缩放后: shape={resized.shape}")

    # 2. 归一化 [0, 255] → [0, 1]
    normalized = resized.astype(np.float32) / 255.0
    logger.info(f"归一化: min={normalized.min():.2f}, max={normalized.max():.2f}")

    # 3. 通道转换 HWC → CHW（PyTorch 格式）
    chw = np.transpose(normalized, (2, 0, 1))
    logger.info(f"通道转换 HWC→CHW: {normalized.shape} → {chw.shape}")

    # 4. 添加 batch 维度
    batch = np.expand_dims(chw, axis=0)
    logger.info(f"添加 batch 维度: {batch.shape}  (NCHW 格式)")


def demo_letterbox():
    """演示 Letterbox 等比缩放。"""
    logger.info("\n--- 2. Letterbox 等比缩放 ---")

    # 模拟一张 1080x1920 的图像（竖屏）
    img_h, img_w = 1080, 1920
    target = 640

    # 计算缩放比例（保持宽高比）
    scale = min(target / img_h, target / img_w)
    new_h = int(img_h * scale)
    new_w = int(img_w * scale)

    # 计算填充
    pad_h = (target - new_h) // 2
    pad_w = (target - new_w) // 2

    logger.info(f"原始尺寸: {img_h}x{img_w}")
    logger.info(f"缩放比例: {scale:.3f}")
    logger.info(f"缩放后: {new_h}x{new_w}")
    logger.info(f"填充: 上下各 {pad_h}px, 左右各 {pad_w}px")
    logger.info(f"最终尺寸: {target}x{target}")


def compute_iou(box1: list, box2: list) -> float:
    """计算两个框的 IoU（交并比）。"""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union = area1 + area2 - intersection

    return intersection / union if union > 0 else 0


def nms(boxes: list[list], scores: list[float], iou_threshold: float = 0.5) -> list[int]:
    """
    非极大值抑制（NMS）。

    Args:
        boxes: 边界框列表 [[x1,y1,x2,y2], ...]
        scores: 置信度列表
        iou_threshold: IoU 阈值
    Returns:
        保留的框的索引列表
    """
    if not boxes:
        return []

    # 按置信度降序排序
    indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    keep = []

    while indices:
        current = indices.pop(0)
        keep.append(current)

        # 移除与当前框 IoU 过高的框
        remaining = []
        for idx in indices:
            iou = compute_iou(boxes[current], boxes[idx])
            if iou < iou_threshold:
                remaining.append(idx)
        indices = remaining

    return keep


def demo_nms():
    """演示 NMS 非极大值抑制。"""
    logger.info("\n--- 3. NMS 非极大值抑制 ---")

    # 模拟检测结果（多个重叠的框）
    boxes = [
        [100, 100, 300, 300],  # 框 A
        [110, 110, 310, 310],  # 框 B（与 A 高度重叠）
        [105, 105, 305, 305],  # 框 C（与 A 高度重叠）
        [400, 400, 550, 550],  # 框 D（独立区域）
        [410, 410, 560, 560],  # 框 E（与 D 重叠）
    ]
    scores = [0.9, 0.75, 0.85, 0.95, 0.7]

    logger.info(f"NMS 前: {len(boxes)} 个检测框")
    for i, (box, score) in enumerate(zip(boxes, scores)):
        logger.info(f"  框 {i}: {box}, 置信度={score:.2f}")

    # 执行 NMS
    keep = nms(boxes, scores, iou_threshold=0.5)

    logger.info(f"\nNMS 后: 保留 {len(keep)} 个框 (IoU 阈值=0.5)")
    for idx in keep:
        logger.info(f"  框 {idx}: {boxes[idx]}, 置信度={scores[idx]:.2f}")

    # 展示 IoU 计算
    logger.info(f"\nIoU 示例:")
    logger.info(f"  框 0 vs 框 1: IoU={compute_iou(boxes[0], boxes[1]):.3f} (高重叠)")
    logger.info(f"  框 0 vs 框 3: IoU={compute_iou(boxes[0], boxes[3]):.3f} (无重叠)")


def main():
    """主函数。"""
    print("=" * 60)
    print("  图像预处理与后处理演示")
    print("  使用 NumPy 实现，不依赖外部图片")
    print("=" * 60)

    demo_preprocessing()
    demo_letterbox()
    demo_nms()

    print("\n✅ 图像处理演示完成！")


if __name__ == "__main__":
    main()
