#!/usr/bin/env python3
"""
PDF 信息查看工具

模块: 03-小工具开发
知识点: PDF 操作
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python pdf_info.py <子命令> <PDF文件>

描述:
    使用 PyPDF2 读取 PDF 文件信息，包括页数统计和元数据读取。
    运行前会检查 PyPDF2 是否已安装，未安装时给出提示。
"""

import argparse
import sys
from pathlib import Path


def check_dependency():
    """检查 PyPDF2 是否已安装。"""
    try:
        import PyPDF2  # noqa: F401
        return True
    except ImportError:
        print("错误：需要安装 PyPDF2 库。请运行：", file=sys.stderr)
        print("  pip install PyPDF2", file=sys.stderr)
        return False


def get_pdf_reader(filepath: str):
    """打开 PDF 文件并返回 reader 对象。"""
    from PyPDF2 import PdfReader

    path = Path(filepath)
    if not path.is_file():
        print(f"错误：文件 '{filepath}' 不存在", file=sys.stderr)
        sys.exit(1)
    if path.suffix.lower() != ".pdf":
        print(f"警告：文件 '{filepath}' 可能不是 PDF 文件", file=sys.stderr)

    try:
        reader = PdfReader(str(path))
        return reader, path
    except Exception as e:
        print(f"错误：无法读取 PDF 文件: {e}", file=sys.stderr)
        sys.exit(1)


def format_size(size_bytes: int) -> str:
    """将字节数格式化为可读的文件大小。"""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def cmd_info(args):
    """查看 PDF 完整信息。"""
    reader, path = get_pdf_reader(args.file)

    print(f"文件: {path.name}")
    print(f"路径: {path.resolve()}")
    print(f"大小: {format_size(path.stat().st_size)}")
    print(f"页数: {len(reader.pages)}")

    # 元数据
    meta = reader.metadata
    if meta:
        print("元数据:")
        fields = [
            ("标题", meta.title),
            ("作者", meta.author),
            ("主题", meta.subject),
            ("创建工具", meta.creator),
            ("生成器", meta.producer),
        ]
        for label, value in fields:
            if value:
                print(f"  {label}: {value}")
    else:
        print("元数据: 无")


def cmd_pages(args):
    """统计 PDF 页数。"""
    reader, path = get_pdf_reader(args.file)
    print(f"{path.name}: {len(reader.pages)} 页")


def cmd_meta(args):
    """读取 PDF 元数据。"""
    reader, path = get_pdf_reader(args.file)
    meta = reader.metadata

    print(f"文件: {path.name}")
    if not meta:
        print("该 PDF 文件没有元数据。")
        return

    # 打印所有可用的元数据字段
    print("元数据:")
    fields = {
        "/Title": "标题",
        "/Author": "作者",
        "/Subject": "主题",
        "/Creator": "创建工具",
        "/Producer": "生成器",
        "/CreationDate": "创建日期",
        "/ModDate": "修改日期",
    }
    found = False
    for key, label in fields.items():
        value = meta.get(key)
        if value:
            print(f"  {label}: {value}")
            found = True

    if not found:
        print("  （元数据字段均为空）")


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(description="PDF 信息查看工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    p_info = subparsers.add_parser("info", help="查看 PDF 完整信息")
    p_info.add_argument("file", help="PDF 文件路径")

    p_pages = subparsers.add_parser("pages", help="统计页数")
    p_pages.add_argument("file", help="PDF 文件路径")

    p_meta = subparsers.add_parser("meta", help="查看元数据")
    p_meta.add_argument("file", help="PDF 文件路径")

    return parser


def main():
    """主函数：检查依赖，解析参数并执行子命令。"""
    if not check_dependency():
        sys.exit(1)

    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    commands = {"info": cmd_info, "pages": cmd_pages, "meta": cmd_meta}
    commands[args.command](args)


if __name__ == "__main__":
    main()
