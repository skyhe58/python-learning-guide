# 小工具开发 速查卡片

## 核心概念

| 概念 | 说明 | 示例 |
|------|------|------|
| argparse | Python 标准库命令行解析 | `parser = argparse.ArgumentParser()` |
| click | 第三方装饰器风格 CLI 框架 | `@click.command()` |
| pathlib | 面向对象的路径操作 | `Path("file.txt").stem` |
| csv 模块 | 标准库 CSV 读写 | `csv.DictReader(f)` |
| shutil | 高级文件操作 | `shutil.move(src, dst)` |
| --dry-run | 预览模式设计模式 | 先展示计划，再执行操作 |

## argparse 常用语法

### 基本用法

```python
import argparse

parser = argparse.ArgumentParser(description="工具描述")
parser.add_argument("input", help="位置参数")           # 必填位置参数
parser.add_argument("--output", "-o", help="可选参数")   # 可选命名参数
parser.add_argument("--count", type=int, default=1)      # 指定类型和默认值
parser.add_argument("--verbose", action="store_true")    # 布尔标志
parser.add_argument("--mode", choices=["a", "b", "c"])   # 限定选项
args = parser.parse_args()
```

### 子命令

```python
subparsers = parser.add_subparsers(dest="command")
p_sub = subparsers.add_parser("sub", help="子命令")
p_sub.add_argument("--option", help="子命令选项")
```

### 互斥参数

```python
group = parser.add_mutually_exclusive_group()
group.add_argument("--json", action="store_true")
group.add_argument("--csv", action="store_true")
```

## click 常用语法

### 基本用法

```python
import click

@click.command()
@click.option("--name", "-n", required=True, help="姓名")
@click.option("--count", "-c", type=int, default=1)
@click.option("--verbose", is_flag=True)
@click.argument("filename")
def main(name, count, verbose, filename):
    """工具描述（自动生成帮助文本）"""
    click.echo(f"Hello, {name}!")
```

### 子命令组

```python
@click.group()
def cli():
    """主命令组"""
    pass

@cli.command()
@click.argument("x", type=float)
def sub(x):
    """子命令"""
    click.echo(x)
```

## 文件操作速查

```python
from pathlib import Path

# 路径操作
p = Path("dir/file.txt")
p.stem          # "file"
p.suffix        # ".txt"
p.parent        # Path("dir")
p.name          # "file.txt"

# 目录遍历
list(p.parent.iterdir())       # 列出目录内容
list(p.parent.glob("*.txt"))   # 按模式匹配

# 文件操作
p.rename("new_name.txt")       # 重命名
p.exists()                     # 是否存在
p.is_file()                    # 是否为文件
p.stat().st_size               # 文件大小（字节）
```

## CSV 操作速查

```python
import csv

# 读取 CSV（字典模式）
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["列名"])

# 写入 CSV
with open("out.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["名称", "值"])
    writer.writeheader()
    writer.writerow({"名称": "A", "值": "1"})
```

## 系统信息速查

```python
import platform, os, shutil

platform.system()          # "Linux" / "Darwin" / "Windows"
platform.python_version()  # "3.12.0"
os.cpu_count()             # CPU 核心数
shutil.disk_usage("/")     # 磁盘使用情况 (total, used, free)
```

## 常见陷阱

- ⚠️ argparse 不指定 `type` 时，参数值默认为字符串，`"3" + 1` 会报错
- ⚠️ click 装饰器顺序：`@click.command()` 必须在最外层（最上面）
- ⚠️ `Path.rename()` 不能跨文件系统移动，跨盘用 `shutil.move()`
- ⚠️ CSV 写入时必须加 `newline=""`，否则 Windows 下会多出空行
- ⚠️ 文件编码：中文环境建议显式指定 `encoding="utf-8"`
- ⚠️ `--dry-run` 模式应该在所有修改操作前检查，避免部分执行

## 面试高频考点

- argparse 和 click 的区别与选型依据
- `pathlib.Path` vs `os.path` 的优劣对比
- Python 中如何实现命令行工具的子命令
- `csv.DictReader` vs `csv.reader` 的区别
- 如何设计可撤销的文件操作（日志 + 逆操作）
- `shutil.move()` vs `os.rename()` vs `Path.rename()` 的区别
