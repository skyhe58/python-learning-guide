#!/usr/bin/env python3
"""
思维导图生成工具 — 自动扫描目录结构生成 Mermaid 格式思维导图

模块: tools
Python 版本: >= 3.9
最后验证: 2025-07-14

运行方式:
    python tools/generate_mindmap.py
    python tools/generate_mindmap.py --dir ./01-python-basics
    python tools/generate_mindmap.py --dir . --depth 2 --output mindmap.md

描述:
    扫描指定目录的文件结构，生成 Mermaid mindmap 格式的思维导图。
    默认扫描项目根目录（tools/ 的父目录），输出到 stdout。
    可通过 --output 参数将结果写入文件。
    本工具为通用型，可复用于任意 Markdown 项目的目录结构可视化。
"""

import argparse
import os
import sys
from pathlib import Path


# 默认忽略的目录和文件
DEFAULT_IGNORE = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "node_modules",
    ".idea",
    ".vscode",
    ".kiro",
    ".DS_Store",
    "*.pyc",
}


def should_ignore(name: str) -> bool:
    """判断文件或目录是否应被忽略"""
    if name in DEFAULT_IGNORE:
        return True
    if name.startswith("."):
        return True
    for pattern in DEFAULT_IGNORE:
        if pattern.startswith("*") and name.endswith(pattern[1:]):
            return True
    return False


def scan_directory(dir_path: Path, current_depth: int, max_depth: int) -> dict:
    """
    递归扫描目录结构，返回嵌套字典表示的树形结构。

    参数:
        dir_path: 要扫描的目录路径
        current_depth: 当前递归深度
        max_depth: 最大扫描深度（-1 表示无限制）

    返回:
        包含目录名和子节点的字典
    """
    result = {
        "name": dir_path.name,
        "children": [],
    }

    if max_depth != -1 and current_depth >= max_depth:
        return result

    try:
        entries = sorted(dir_path.iterdir(), key=lambda e: (not e.is_dir(), e.name))
    except PermissionError:
        return result

    for entry in entries:
        if should_ignore(entry.name):
            continue

        if entry.is_dir():
            child = scan_directory(entry, current_depth + 1, max_depth)
            result["children"].append(child)
        else:
            result["children"].append({"name": entry.name, "children": []})

    return result


def generate_mermaid(tree: dict, indent: int = 0) -> list[str]:
    """
    将树形结构转换为 Mermaid mindmap 格式的文本行。

    参数:
        tree: scan_directory 返回的树形结构字典
        indent: 当前缩进层级

    返回:
        Mermaid mindmap 格式的文本行列表
    """
    lines = []
    prefix = "  " * indent

    if indent == 0:
        # 根节点
        lines.append("mindmap")
        lines.append(f"  root(({tree['name']}))")
        for child in tree["children"]:
            lines.extend(generate_mermaid(child, indent=2))
    else:
        # 子节点：目录用圆角矩形，文件用普通文本
        name = tree["name"]
        if tree["children"]:
            # 有子节点的目录
            lines.append(f"{prefix}{name}")
            for child in tree["children"]:
                lines.extend(generate_mermaid(child, indent + 1))
        else:
            lines.append(f"{prefix}{name}")

    return lines


def get_default_dir() -> Path:
    """获取默认扫描目录（tools/ 的父目录，即项目根目录）"""
    return Path(__file__).resolve().parent.parent


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="自动扫描目录结构生成 Mermaid 格式思维导图。"
        "本工具为通用型，可复用于任意 Markdown 项目。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 扫描项目根目录，输出到 stdout
  python tools/generate_mindmap.py

  # 扫描指定目录
  python tools/generate_mindmap.py --dir ./01-python-basics

  # 限制扫描深度为 2 层
  python tools/generate_mindmap.py --depth 2

  # 输出到文件
  python tools/generate_mindmap.py --output mindmap.md
        """,
    )
    parser.add_argument(
        "--dir",
        type=str,
        default=None,
        help="要扫描的目录路径（默认: 项目根目录，即 tools/ 的父目录）",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="输出文件路径（默认: 输出到 stdout）",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=-1,
        help="最大扫描深度，-1 表示无限制（默认: -1）",
    )
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()

    # 确定扫描目录
    if args.dir:
        scan_dir = Path(args.dir).resolve()
    else:
        scan_dir = get_default_dir()

    if not scan_dir.is_dir():
        print(f"错误: 目录不存在 — {scan_dir}", file=sys.stderr)
        sys.exit(1)

    # 扫描目录结构
    tree = scan_directory(scan_dir, current_depth=0, max_depth=args.depth)

    # 生成 Mermaid 思维导图
    mermaid_lines = generate_mermaid(tree)
    mermaid_text = "\n".join(mermaid_lines) + "\n"

    # 输出结果
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(mermaid_text, encoding="utf-8")
        print(f"思维导图已写入: {output_path}")
    else:
        print(mermaid_text)


if __name__ == "__main__":
    main()
