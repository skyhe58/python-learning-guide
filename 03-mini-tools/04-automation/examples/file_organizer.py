#!/usr/bin/env python3
"""
文件整理工具 — 按扩展名自动分类文件到子目录

模块: 03-小工具开发
知识点: 自动化脚本
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python file_organizer.py <目录> [--dry-run] [--rules rules.json] [--undo]

描述:
    扫描指定目录下的文件，按扩展名自动分类到对应子目录。
    支持预览模式、自定义分类规则和撤销操作。
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

# 默认分类规则：类别名 -> 扩展名列表
DEFAULT_RULES: dict[str, list[str]] = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "文档": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md"],
    "代码": [".py", ".java", ".js", ".ts", ".html", ".css", ".c", ".cpp", ".go", ".rs"],
    "压缩包": [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2", ".xz"],
    "音频": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
    "视频": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
    "数据": [".csv", ".json", ".xml", ".yaml", ".yml", ".sql", ".db"],
}

# 操作日志文件名，用于撤销
LOG_FILENAME = ".organize_log.json"


def load_rules(rules_file: str | None) -> dict[str, list[str]]:
    """加载分类规则。"""
    if rules_file:
        path = Path(rules_file)
        if not path.is_file():
            print(f"错误：规则文件 '{rules_file}' 不存在", file=sys.stderr)
            sys.exit(1)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_RULES


def classify_file(filename: str, rules: dict[str, list[str]]) -> str:
    """根据扩展名判断文件所属类别。"""
    ext = Path(filename).suffix.lower()
    for category, extensions in rules.items():
        if ext in extensions:
            return category
    return "其他"


def organize(directory: str, rules: dict[str, list[str]], dry_run: bool = False) -> int:
    """整理目录下的文件。

    Args:
        directory: 目标目录路径
        rules: 分类规则
        dry_run: 预览模式

    Returns:
        移动的文件数量
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        print(f"错误：目录 '{directory}' 不存在", file=sys.stderr)
        sys.exit(1)

    # 收集文件（排除子目录和隐藏文件）
    files = [f for f in dir_path.iterdir()
             if f.is_file() and not f.name.startswith(".")]

    if not files:
        print("目录中没有需要整理的文件。")
        return 0

    print(f"扫描目录: {dir_path.resolve()}")
    print(f"发现 {len(files)} 个文件\n")

    # 按类别分组
    categories: dict[str, list[Path]] = {}
    for f in files:
        cat = classify_file(f.name, rules)
        categories.setdefault(cat, []).append(f)

    # 显示分类计划
    print("分类计划:")
    for cat, cat_files in sorted(categories.items()):
        names = ", ".join(f.name for f in cat_files[:5])
        suffix = f", ... 等 {len(cat_files)} 个" if len(cat_files) > 5 else ""
        print(f"  {cat} ({len(cat_files)} 个): {names}{suffix}")

    if dry_run:
        print("\n预览完成，使用不带 --dry-run 参数执行实际整理。")
        return 0

    # 执行移动并记录日志
    move_log = []
    count = 0
    for cat, cat_files in categories.items():
        target_dir = dir_path / cat
        target_dir.mkdir(exist_ok=True)
        for f in cat_files:
            dest = target_dir / f.name
            if dest.exists():
                print(f"  [跳过] {f.name}（目标已存在）")
                continue
            shutil.move(str(f), str(dest))
            move_log.append({"from": str(f), "to": str(dest)})
            count += 1

    # 保存操作日志
    log_path = dir_path / LOG_FILENAME
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(move_log, f, ensure_ascii=False, indent=2)

    print(f"\n完成！共移动 {count} 个文件。")
    print(f"操作日志已保存到: {log_path}")
    return count


def undo(directory: str) -> int:
    """撤销上次整理操作。"""
    dir_path = Path(directory)
    log_path = dir_path / LOG_FILENAME

    if not log_path.is_file():
        print("没有找到操作日志，无法撤销。")
        return 0

    with open(log_path, "r", encoding="utf-8") as f:
        move_log = json.load(f)

    count = 0
    for entry in reversed(move_log):
        src = Path(entry["to"])
        dest = Path(entry["from"])
        if src.is_file():
            shutil.move(str(src), str(dest))
            count += 1
            print(f"  [还原] {src.name} -> {dest.parent.name}/")

    # 清理空目录
    for item in dir_path.iterdir():
        if item.is_dir() and not any(item.iterdir()):
            item.rmdir()
            print(f"  [删除空目录] {item.name}/")

    log_path.unlink()
    print(f"\n撤销完成！共还原 {count} 个文件。")
    return count


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(
        description="文件整理工具 — 按扩展名自动分类文件到子目录"
    )
    parser.add_argument("directory", help="要整理的目录路径")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际移动文件")
    parser.add_argument("--rules", help="自定义分类规则 JSON 文件路径")
    parser.add_argument("--undo", action="store_true", help="撤销上次整理操作")
    return parser


def main():
    """主函数：解析参数并执行文件整理或撤销。"""
    parser = build_parser()
    args = parser.parse_args()

    if args.undo:
        undo(args.directory)
    else:
        rules = load_rules(args.rules)
        organize(args.directory, rules, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
