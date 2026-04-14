#!/usr/bin/env python3
"""
文件批量重命名工具

模块: 03-小工具开发
知识点: 文件批量处理
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python batch_rename.py <目录> --mode <模式> [选项]

描述:
    支持四种重命名模式（前缀/后缀/替换/序号），
    提供 --dry-run 预览功能，使用 argparse 解析命令行参数。
"""

import argparse
import os
import sys
from pathlib import Path


def get_files(directory: str, ext: str | None = None) -> list[Path]:
    """获取目录下的文件列表（排除子目录），可按扩展名过滤。

    Args:
        directory: 目标目录路径
        ext: 可选的扩展名过滤（如 '.txt'）

    Returns:
        排序后的文件路径列表
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        print(f"错误：目录 '{directory}' 不存在或不是目录", file=sys.stderr)
        sys.exit(1)

    files = [f for f in dir_path.iterdir() if f.is_file()]
    if ext:
        ext = ext if ext.startswith(".") else f".{ext}"
        files = [f for f in files if f.suffix.lower() == ext.lower()]
    return sorted(files)


def rename_prefix(files: list[Path], prefix: str) -> list[tuple[Path, Path]]:
    """生成添加前缀的重命名计划。"""
    plan = []
    for f in files:
        new_name = f"{prefix}{f.name}"
        plan.append((f, f.parent / new_name))
    return plan


def rename_suffix(files: list[Path], suffix: str) -> list[tuple[Path, Path]]:
    """生成添加后缀的重命名计划（后缀加在扩展名之前）。"""
    plan = []
    for f in files:
        new_name = f"{f.stem}{suffix}{f.suffix}"
        plan.append((f, f.parent / new_name))
    return plan


def rename_replace(files: list[Path], old: str, new: str) -> list[tuple[Path, Path]]:
    """生成替换字符串的重命名计划。"""
    plan = []
    for f in files:
        if old in f.name:
            new_name = f.name.replace(old, new)
            plan.append((f, f.parent / new_name))
    return plan


def rename_sequence(
    files: list[Path], start: int = 1, digits: int = 3
) -> list[tuple[Path, Path]]:
    """生成按序号重命名的计划。"""
    plan = []
    for i, f in enumerate(files, start=start):
        new_name = f"{str(i).zfill(digits)}{f.suffix}"
        plan.append((f, f.parent / new_name))
    return plan


def execute_plan(plan: list[tuple[Path, Path]], dry_run: bool = False) -> int:
    """执行或预览重命名计划。

    Args:
        plan: (原路径, 新路径) 的列表
        dry_run: 为 True 时只预览不执行

    Returns:
        处理的文件数量
    """
    if not plan:
        print("没有需要重命名的文件。")
        return 0

    tag = "[预览]" if dry_run else "[重命名]"
    count = 0
    for old_path, new_path in plan:
        if old_path == new_path:
            continue
        if not dry_run and new_path.exists():
            print(f"[跳过] {new_path.name} 已存在，跳过 {old_path.name}")
            continue
        print(f"{tag} {old_path.name} -> {new_path.name}")
        if not dry_run:
            old_path.rename(new_path)
        count += 1

    action = "将被重命名" if dry_run else "已重命名"
    print(f"\n{'预览完成！' if dry_run else '完成！'}共 {count} 个文件{action}")
    return count


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(
        description="文件批量重命名工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
使用示例:
  %(prog)s ./photos --mode prefix --prefix "2025_"
  %(prog)s ./docs --mode suffix --suffix "_v2"
  %(prog)s ./files --mode replace --old "旧" --new "新"
  %(prog)s ./files --mode sequence --start 1 --digits 3
  %(prog)s ./files --mode prefix --prefix "new_" --dry-run
        """,
    )
    parser.add_argument("directory", help="目标目录路径")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["prefix", "suffix", "replace", "sequence"],
        help="重命名模式",
    )
    parser.add_argument("--prefix", default="", help="前缀字符串（prefix 模式）")
    parser.add_argument("--suffix", default="", help="后缀字符串（suffix 模式）")
    parser.add_argument("--old", default="", help="要替换的旧字符串（replace 模式）")
    parser.add_argument("--new", default="", help="替换后的新字符串（replace 模式）")
    parser.add_argument("--start", type=int, default=1, help="序号起始值（默认 1）")
    parser.add_argument("--digits", type=int, default=3, help="序号位数（默认 3）")
    parser.add_argument("--ext", default=None, help="只处理指定扩展名（如 .txt）")
    parser.add_argument(
        "--dry-run", action="store_true", help="预览模式，不实际重命名"
    )
    return parser


def main():
    """主函数：解析参数并执行批量重命名。"""
    parser = build_parser()
    args = parser.parse_args()

    files = get_files(args.directory, args.ext)
    if not files:
        print("目标目录中没有匹配的文件。")
        return

    # 根据模式生成重命名计划
    if args.mode == "prefix":
        if not args.prefix:
            parser.error("prefix 模式需要 --prefix 参数")
        plan = rename_prefix(files, args.prefix)
    elif args.mode == "suffix":
        if not args.suffix:
            parser.error("suffix 模式需要 --suffix 参数")
        plan = rename_suffix(files, args.suffix)
    elif args.mode == "replace":
        if not args.old:
            parser.error("replace 模式需要 --old 参数")
        plan = rename_replace(files, args.old, args.new)
    elif args.mode == "sequence":
        plan = rename_sequence(files, args.start, args.digits)
    else:
        parser.error(f"未知模式: {args.mode}")
        return

    execute_plan(plan, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
