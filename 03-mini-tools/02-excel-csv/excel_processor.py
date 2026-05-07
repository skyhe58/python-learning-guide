#!/usr/bin/env python3
"""
Excel/CSV 数据处理工具

模块: 03-小工具开发
知识点: Excel/CSV 数据处理
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python excel_processor.py <子命令> <文件> [选项]

描述:
    基于 csv 标准库的 CSV 数据处理工具，支持查看信息、
    条件筛选、统计汇总和格式转换。无需安装第三方依赖。
"""

import argparse
import csv
import sys
from pathlib import Path


def read_csv(filepath: str, encoding: str = "utf-8") -> tuple[list[str], list[dict]]:
    """读取 CSV 文件，返回 (列名列表, 数据行字典列表)。"""
    path = Path(filepath)
    if not path.is_file():
        print(f"错误：文件 '{filepath}' 不存在", file=sys.stderr)
        sys.exit(1)

    with open(path, "r", encoding=encoding, newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)
    return headers, rows


def cmd_info(args):
    """查看 CSV 文件基本信息。"""
    headers, rows = read_csv(args.file, args.encoding)

    print(f"文件: {args.file}")
    print(f"行数: {len(rows)}（不含表头）")
    print(f"列数: {len(headers)}")
    print(f"列名: {', '.join(headers)}")

    # 预览前 5 行
    preview_count = min(5, len(rows))
    if preview_count > 0:
        print(f"\n前 {preview_count} 行预览:")
        # 计算列宽
        col_widths = {h: max(len(h), 6) for h in headers}
        for row in rows[:preview_count]:
            for h in headers:
                col_widths[h] = max(col_widths[h], len(str(row.get(h, ""))))

        # 打印表头
        header_line = "  ".join(h.ljust(col_widths[h]) for h in headers)
        print(f"  {header_line}")

        # 打印数据行
        for row in rows[:preview_count]:
            line = "  ".join(
                str(row.get(h, "")).ljust(col_widths[h]) for h in headers
            )
            print(f"  {line}")


def _try_float(value: str) -> float | None:
    """尝试将字符串转为浮点数，失败返回 None。"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _compare(row_value: str, op: str, target: str) -> bool:
    """根据运算符比较值。"""
    if op == "contains":
        return target in row_value
    if op == "==":
        return row_value == target
    if op == "!=":
        return row_value != target

    # 数值比较
    row_num = _try_float(row_value)
    target_num = _try_float(target)
    if row_num is None or target_num is None:
        return False

    ops = {">": row_num > target_num, "<": row_num < target_num,
           ">=": row_num >= target_num, "<=": row_num <= target_num}
    return ops.get(op, False)


def cmd_filter(args):
    """按条件筛选数据行。"""
    headers, rows = read_csv(args.file, args.encoding)

    if args.column not in headers:
        print(f"错误：列 '{args.column}' 不存在。可用列: {', '.join(headers)}",
              file=sys.stderr)
        sys.exit(1)

    matched = [r for r in rows if _compare(r.get(args.column, ""), args.op, args.value)]
    print(f"筛选条件: {args.column} {args.op} {args.value}")
    print(f"匹配 {len(matched)} 行（共 {len(rows)} 行）")

    if args.output and matched:
        with open(args.output, "w", encoding=args.encoding, newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(matched)
        print(f"结果已保存到: {args.output}")
    elif matched:
        # 打印匹配结果
        for row in matched[:10]:
            print("  " + " | ".join(f"{h}={row.get(h, '')}" for h in headers))
        if len(matched) > 10:
            print(f"  ... 还有 {len(matched) - 10} 行")


def cmd_stats(args):
    """对数值列进行统计汇总。"""
    headers, rows = read_csv(args.file, args.encoding)

    if args.column not in headers:
        print(f"错误：列 '{args.column}' 不存在。可用列: {', '.join(headers)}",
              file=sys.stderr)
        sys.exit(1)

    values = []
    for row in rows:
        num = _try_float(row.get(args.column, ""))
        if num is not None:
            values.append(num)

    if not values:
        print(f"列 '{args.column}' 中没有有效的数值数据。")
        return

    total = sum(values)
    avg = total / len(values)
    print(f"列: {args.column}")
    print(f"  总数: {len(values)}")
    print(f"  求和: {total:.2f}")
    print(f"  平均值: {avg:.2f}")
    print(f"  最大值: {max(values):.2f}")
    print(f"  最小值: {min(values):.2f}")


def cmd_convert(args):
    """CSV 格式转换（分隔符、编码）。"""
    headers, rows = read_csv(args.file, args.encoding)

    # 处理转义字符
    delimiter = args.delimiter.encode().decode("unicode_escape")
    out_encoding = args.out_encoding or args.encoding

    with open(args.output, "w", encoding=out_encoding, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(rows)

    print(f"转换完成: {args.file} -> {args.output}")
    print(f"  分隔符: '{delimiter}' | 编码: {out_encoding}")
    print(f"  共 {len(rows)} 行数据")


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(
        description="CSV 数据处理工具（基于标准库，无需第三方依赖）"
    )
    parser.add_argument("--encoding", default="utf-8", help="文件编码（默认 utf-8）")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # info 子命令
    p_info = subparsers.add_parser("info", help="查看 CSV 文件信息")
    p_info.add_argument("file", help="CSV 文件路径")

    # filter 子命令
    p_filter = subparsers.add_parser("filter", help="按条件筛选数据")
    p_filter.add_argument("file", help="CSV 文件路径")
    p_filter.add_argument("--column", required=True, help="筛选列名")
    p_filter.add_argument(
        "--op", required=True,
        choices=["==", "!=", ">", "<", ">=", "<=", "contains"],
        help="比较运算符",
    )
    p_filter.add_argument("--value", required=True, help="比较值")
    p_filter.add_argument("--output", help="输出文件路径")

    # stats 子命令
    p_stats = subparsers.add_parser("stats", help="统计汇总")
    p_stats.add_argument("file", help="CSV 文件路径")
    p_stats.add_argument("--column", required=True, help="统计列名")

    # convert 子命令
    p_convert = subparsers.add_parser("convert", help="格式转换")
    p_convert.add_argument("file", help="CSV 文件路径")
    p_convert.add_argument("--output", required=True, help="输出文件路径")
    p_convert.add_argument("--delimiter", default=",", help="输出分隔符（默认逗号）")
    p_convert.add_argument("--out-encoding", help="输出编码（默认与输入相同）")

    return parser


def main():
    """主函数：解析参数并执行对应子命令。"""
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    commands = {
        "info": cmd_info,
        "filter": cmd_filter,
        "stats": cmd_stats,
        "convert": cmd_convert,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
