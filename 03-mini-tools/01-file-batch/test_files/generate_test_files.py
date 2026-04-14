#!/usr/bin/env python3
"""
生成测试用示例文件

模块: 03-小工具开发
知识点: 文件批量处理
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python generate_test_files.py

描述:
    在当前目录下生成一组用于测试 batch_rename.py 的示例文件。
    包含不同扩展名和命名风格的文件，方便测试各种重命名模式。
"""

from pathlib import Path


# 要生成的测试文件列表
TEST_FILES = [
    "report_q1.txt",
    "report_q2.txt",
    "report_q3.txt",
    "data_2024.csv",
    "data_2025.csv",
    "photo_001.jpg",
    "photo_002.jpg",
    "photo_003.jpg",
    "notes_old.md",
    "summary_old.md",
]


def main():
    """在脚本所在目录下生成测试文件。"""
    script_dir = Path(__file__).parent
    created = 0

    for filename in TEST_FILES:
        filepath = script_dir / filename
        filepath.write_text(
            f"这是测试文件: {filename}\n用于测试 batch_rename.py 的各种重命名模式。\n",
            encoding="utf-8",
        )
        created += 1
        print(f"[创建] {filename}")

    print(f"\n完成！共创建 {created} 个测试文件，位于: {script_dir}")


if __name__ == "__main__":
    main()
