#!/usr/bin/env python3
"""
argparse 完整示例

模块: 03-小工具开发
知识点: 命令行工具开发
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python argparse_demo.py greet --name Alice --count 3
    python argparse_demo.py calc add 10 20
    python argparse_demo.py calc mul 5 6
    python argparse_demo.py search "hello" --ignore-case --max-results 5

描述:
    演示 argparse 的完整功能，包括子命令、互斥参数组、
    类型验证、自定义格式化和多级子命令。
"""

import argparse
import sys


# ============================================================
# 子命令 1: greet — 打招呼（演示基本参数和互斥参数）
# ============================================================

def cmd_greet(args):
    """打招呼子命令。"""
    greeting = args.greeting or "Hello"
    for i in range(args.count):
        if args.uppercase:
            print(f"{greeting}, {args.name}!".upper())
        elif args.lowercase:
            print(f"{greeting}, {args.name}!".lower())
        else:
            print(f"{greeting}, {args.name}!")


# ============================================================
# 子命令 2: calc — 计算器（演示二级子命令和类型验证）
# ============================================================

def cmd_calc_add(args):
    """加法运算。"""
    result = args.a + args.b
    print(f"{args.a} + {args.b} = {result}")


def cmd_calc_mul(args):
    """乘法运算。"""
    result = args.a * args.b
    print(f"{args.a} × {args.b} = {result}")


def cmd_calc_div(args):
    """除法运算（演示错误处理）。"""
    if args.b == 0:
        print("错误：除数不能为零", file=sys.stderr)
        sys.exit(1)
    result = args.a / args.b
    precision = args.precision
    print(f"{args.a} ÷ {args.b} = {result:.{precision}f}")


# ============================================================
# 子命令 3: search — 搜索（演示多种参数类型）
# ============================================================

def cmd_search(args):
    """搜索子命令（模拟搜索功能）。"""
    print(f"搜索关键词: '{args.pattern}'")
    print(f"忽略大小写: {args.ignore_case}")
    print(f"最大结果数: {args.max_results}")
    if args.file_types:
        print(f"文件类型过滤: {', '.join(args.file_types)}")
    print(f"详细模式: {args.verbose}")


# ============================================================
# 自定义类型验证函数
# ============================================================

def positive_int(value: str) -> int:
    """自定义类型：正整数验证。"""
    try:
        n = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' 不是有效的整数")
    if n <= 0:
        raise argparse.ArgumentTypeError(f"'{value}' 不是正整数（必须 > 0）")
    return n


# ============================================================
# 构建解析器
# ============================================================

def build_parser() -> argparse.ArgumentParser:
    """构建完整的命令行参数解析器。"""
    # 主解析器
    parser = argparse.ArgumentParser(
        prog="argparse_demo",
        description="argparse 完整功能演示",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
               "  %(prog)s greet --name Alice\n"
               "  %(prog)s calc add 10 20\n"
               "  %(prog)s search 'hello' --ignore-case",
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s 1.0.0"
    )

    subparsers = parser.add_subparsers(dest="command", help="可用子命令")

    # --- greet 子命令 ---
    p_greet = subparsers.add_parser("greet", help="打招呼")
    p_greet.add_argument("--name", "-n", required=True, help="姓名")
    p_greet.add_argument("--count", "-c", type=positive_int, default=1,
                         help="重复次数（正整数，默认 1）")
    p_greet.add_argument("--greeting", "-g", help="自定义问候语（默认 Hello）")

    # 互斥参数组：--uppercase 和 --lowercase 不能同时使用
    case_group = p_greet.add_mutually_exclusive_group()
    case_group.add_argument("--uppercase", "-U", action="store_true",
                            help="全部大写输出")
    case_group.add_argument("--lowercase", "-L", action="store_true",
                            help="全部小写输出")

    # --- calc 子命令（含二级子命令） ---
    p_calc = subparsers.add_parser("calc", help="计算器")
    calc_sub = p_calc.add_subparsers(dest="operation", help="运算类型")

    for name, func, desc in [
        ("add", cmd_calc_add, "加法"),
        ("mul", cmd_calc_mul, "乘法"),
    ]:
        p = calc_sub.add_parser(name, help=desc)
        p.add_argument("a", type=float, help="第一个数")
        p.add_argument("b", type=float, help="第二个数")

    p_div = calc_sub.add_parser("div", help="除法")
    p_div.add_argument("a", type=float, help="被除数")
    p_div.add_argument("b", type=float, help="除数")
    p_div.add_argument("--precision", "-p", type=int, default=2,
                       help="小数位数（默认 2）")

    # --- search 子命令 ---
    p_search = subparsers.add_parser("search", help="搜索")
    p_search.add_argument("pattern", help="搜索关键词")
    p_search.add_argument("--ignore-case", "-i", action="store_true",
                          help="忽略大小写")
    p_search.add_argument("--max-results", "-m", type=positive_int, default=10,
                          help="最大结果数（默认 10）")
    p_search.add_argument("--file-types", "-t", nargs="+",
                          help="文件类型过滤（如 .py .txt）")
    p_search.add_argument("--verbose", "-v", action="count", default=0,
                          help="详细模式（可叠加 -vv）")

    return parser


def main():
    """主函数：解析参数并分发到对应子命令。"""
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "greet":
        cmd_greet(args)
    elif args.command == "calc":
        if not args.operation:
            parser.parse_args(["calc", "--help"])
            return
        ops = {"add": cmd_calc_add, "mul": cmd_calc_mul, "div": cmd_calc_div}
        ops[args.operation](args)
    elif args.command == "search":
        cmd_search(args)


if __name__ == "__main__":
    main()
