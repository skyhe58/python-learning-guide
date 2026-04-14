#!/usr/bin/env python3
"""
click 完整示例

模块: 03-小工具开发
知识点: 命令行工具开发
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python click_demo.py greet --name Alice --count 3
    python click_demo.py calc add 10 20
    python click_demo.py file-info README.md
    python click_demo.py --help

描述:
    演示 click 的装饰器风格 CLI 开发，包括子命令组、
    选项/参数、类型验证、颜色输出和确认提示。
    运行前需安装 click: pip install click
"""

import sys
from pathlib import Path

# 依赖检查
try:
    import click
except ImportError:
    print("错误：需要安装 click 库。请运行：", file=sys.stderr)
    print("  pip install click", file=sys.stderr)
    sys.exit(1)


# ============================================================
# 主命令组
# ============================================================

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """click 完整功能演示 — 装饰器风格的 CLI 工具。"""
    pass


# ============================================================
# 子命令 1: greet — 打招呼
# ============================================================

@cli.command()
@click.option("--name", "-n", required=True, help="姓名")
@click.option("--count", "-c", type=click.IntRange(min=1), default=1,
              help="重复次数（默认 1）")
@click.option("--greeting", "-g", default="Hello", help="自定义问候语")
@click.option("--color", type=click.Choice(["red", "green", "blue", "yellow"]),
              default=None, help="输出颜色")
def greet(name: str, count: int, greeting: str, color: str | None):
    """打招呼 — 演示基本选项和颜色输出。"""
    for _ in range(count):
        message = f"{greeting}, {name}!"
        if color:
            click.secho(message, fg=color, bold=True)
        else:
            click.echo(message)


# ============================================================
# 子命令组 2: calc — 计算器（嵌套子命令）
# ============================================================

@cli.group()
def calc():
    """计算器 — 演示嵌套子命令组。"""
    pass


@calc.command()
@click.argument("a", type=float)
@click.argument("b", type=float)
def add(a: float, b: float):
    """加法运算。"""
    result = a + b
    click.echo(f"{a} + {b} = {click.style(str(result), fg='green', bold=True)}")


@calc.command()
@click.argument("a", type=float)
@click.argument("b", type=float)
def mul(a: float, b: float):
    """乘法运算。"""
    result = a * b
    click.echo(f"{a} × {b} = {click.style(str(result), fg='green', bold=True)}")


@calc.command()
@click.argument("a", type=float)
@click.argument("b", type=float)
@click.option("--precision", "-p", type=int, default=2, help="小数位数")
def div(a: float, b: float, precision: int):
    """除法运算。"""
    if b == 0:
        click.secho("错误：除数不能为零", fg="red", err=True)
        sys.exit(1)
    result = a / b
    click.echo(f"{a} ÷ {b} = {click.style(f'{result:.{precision}f}', fg='green', bold=True)}")


# ============================================================
# 子命令 3: file-info — 文件信息（演示 Path 类型和确认提示）
# ============================================================

@cli.command("file-info")
@click.argument("filepath", type=click.Path(exists=True))
@click.option("--delete", is_flag=True, help="查看后删除文件（会要求确认）")
def file_info(filepath: str, delete: bool):
    """查看文件信息 — 演示 Path 类型验证和确认提示。"""
    path = Path(filepath)

    click.echo(f"文件名: {click.style(path.name, bold=True)}")
    click.echo(f"路径: {path.resolve()}")
    click.echo(f"大小: {path.stat().st_size} 字节")
    click.echo(f"类型: {'目录' if path.is_dir() else '文件'}")

    if path.is_file():
        click.echo(f"扩展名: {path.suffix or '无'}")

        # 尝试读取前几行
        try:
            text = path.read_text(encoding="utf-8")
            lines = text.splitlines()
            click.echo(f"行数: {len(lines)}")
            if lines:
                click.echo("\n前 3 行预览:")
                for line in lines[:3]:
                    click.echo(f"  {line}")
        except (UnicodeDecodeError, PermissionError):
            click.echo("（二进制文件，无法预览）")

    # 确认删除
    if delete:
        if click.confirm(click.style(f"\n确定要删除 '{path.name}' 吗？", fg="red")):
            path.unlink()
            click.secho(f"已删除: {path.name}", fg="yellow")
        else:
            click.echo("已取消删除。")


# ============================================================
# 子命令 4: demo — 交互式演示
# ============================================================

@cli.command()
def demo():
    """交互式功能演示 — 展示 click 的交互能力。"""
    click.secho("=== click 交互式演示 ===", fg="cyan", bold=True)

    # 文本输入
    name = click.prompt("请输入你的名字", default="World")
    click.echo(f"你好, {name}!")

    # 选择
    lang = click.prompt(
        "你最喜欢的编程语言",
        type=click.Choice(["Python", "Java", "Go", "Rust"]),
        default="Python",
    )
    click.secho(f"好选择！{lang} 是一门很棒的语言。", fg="green")

    # 确认
    if click.confirm("要查看更多演示吗？"):
        # 颜色展示
        click.echo("\n颜色输出演示:")
        for color in ["red", "green", "yellow", "blue", "magenta", "cyan"]:
            click.secho(f"  这是 {color} 颜色", fg=color)
    else:
        click.echo("再见！")


def main():
    """主函数入口。"""
    cli()


if __name__ == "__main__":
    main()
