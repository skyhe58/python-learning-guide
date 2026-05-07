#!/usr/bin/env python3
"""
OpenCV 图像基础演示

模块: 07-yolo-cv（计算机视觉）
知识点: OpenCV 图像基础
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    pip install opencv-python numpy
    python opencv_demo.py

描述:
    使用 NumPy 生成测试图像，演示 OpenCV 的基础操作。
    不依赖外部图片文件。
"""

import logging
import os

import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def check_opencv():
    """检查 OpenCV 是否安装。"""
    try:
        import cv2
        logger.info(f"OpenCV 版本: {cv2.__version__}")
        return True
    except ImportError:
        logger.warning("OpenCV 未安装，请运行: pip install opencv-python")
        logger.info("以下使用纯 NumPy 演示图像基础概念")
        return False


def demo_create_image():
    """使用 NumPy 创建测试图像。"""
    logger.info("--- 1. 创建测试图像 ---")

    # 创建纯色图像 (高, 宽, 通道)
    # OpenCV 使用 BGR 颜色空间
    height, width = 300, 400
    img = np.zeros((height, width, 3), dtype=np.uint8)
    logger.info(f"空白图像: shape={img.shape}, dtype={img.dtype}")

    # 填充颜色区域
    img[0:100, :] = [255, 0, 0]      # 上部蓝色 (BGR)
    img[100:200, :] = [0, 255, 0]    # 中部绿色
    img[200:300, :] = [0, 0, 255]    # 下部红色

    logger.info(f"像素值 [0,0]: {img[0, 0]} (蓝色 BGR)")
    logger.info(f"像素值 [150,0]: {img[150, 0]} (绿色 BGR)")
    return img


def demo_image_operations(img: np.ndarray):
    """演示基础图像操作。"""
    logger.info("\n--- 2. 基础图像操作 ---")

    has_cv2 = check_opencv()

    if has_cv2:
        import cv2

        # 缩放
        resized = cv2.resize(img, (200, 150))  # (宽, 高)
        logger.info(f"缩放: {img.shape} → {resized.shape}")

        # 裁剪（直接用 NumPy 切片）
        cropped = img[50:250, 100:300]
        logger.info(f"裁剪: {cropped.shape}")

        # 翻转
        flipped_h = cv2.flip(img, 1)  # 水平翻转
        flipped_v = cv2.flip(img, 0)  # 垂直翻转
        logger.info("翻转: 水平/垂直翻转完成")

        # 颜色空间转换
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        logger.info(f"灰度图: shape={gray.shape}")

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        logger.info(f"BGR → RGB 转换完成")
    else:
        # 纯 NumPy 演示
        resized_h, resized_w = 150, 200
        # 简单最近邻缩放
        row_idx = (np.arange(resized_h) * img.shape[0] / resized_h).astype(int)
        col_idx = (np.arange(resized_w) * img.shape[1] / resized_w).astype(int)
        resized = img[np.ix_(row_idx, col_idx)]
        logger.info(f"缩放 (NumPy): {img.shape} → {resized.shape}")

        cropped = img[50:250, 100:300]
        logger.info(f"裁剪 (NumPy): {cropped.shape}")

        # BGR → 灰度（加权平均）
        gray = np.dot(img[..., :3], [0.114, 0.587, 0.299]).astype(np.uint8)
        logger.info(f"灰度图 (NumPy): shape={gray.shape}")


def demo_drawing(img: np.ndarray):
    """演示在图像上绘制图形。"""
    logger.info("\n--- 3. 绘制图形 ---")

    has_cv2 = check_opencv()
    canvas = img.copy()

    if has_cv2:
        import cv2

        # 绘制矩形
        cv2.rectangle(canvas, (50, 50), (350, 250), (255, 255, 255), 2)
        logger.info("绘制矩形: (50,50) → (350,250)")

        # 绘制圆形
        cv2.circle(canvas, (200, 150), 80, (0, 255, 255), 2)
        logger.info("绘制圆形: 中心(200,150), 半径80")

        # 绘制文字
        cv2.putText(canvas, "OpenCV Demo", (80, 280), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        logger.info("绘制文字: 'OpenCV Demo'")

        # 保存图像
        output_path = "opencv_demo_output.png"
        cv2.imwrite(output_path, canvas)
        logger.info(f"图像已保存: {output_path}")
    else:
        # 纯 NumPy 绘制矩形
        canvas[50, 50:350] = [255, 255, 255]    # 上边
        canvas[250, 50:350] = [255, 255, 255]   # 下边
        canvas[50:250, 50] = [255, 255, 255]    # 左边
        canvas[50:250, 350] = [255, 255, 255]   # 右边
        logger.info("绘制矩形 (NumPy): 使用数组索引")


def demo_image_info():
    """演示图像信息查看。"""
    logger.info("\n--- 4. 图像信息 ---")

    # 创建不同类型的图像
    color_img = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
    gray_img = np.random.randint(0, 256, (480, 640), dtype=np.uint8)

    for name, img in [("彩色图", color_img), ("灰度图", gray_img)]:
        logger.info(f"  {name}: shape={img.shape}, dtype={img.dtype}, "
                     f"size={img.size}, 内存={img.nbytes / 1024:.1f} KB")


def main():
    """主函数。"""
    print("=" * 60)
    print("  OpenCV 图像基础演示")
    print("  使用 NumPy 生成测试图像，不依赖外部文件")
    print("=" * 60)

    check_opencv()
    img = demo_create_image()
    demo_image_operations(img)
    demo_drawing(img)
    demo_image_info()

    print("\n✅ OpenCV 基础演示完成！")


if __name__ == "__main__":
    main()
