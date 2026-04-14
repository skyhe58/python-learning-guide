# 命令行工具开发

> **模块：** 03-小工具开发
> **难度：** 入门
> **前置知识：** Python 基础（01-python-basics）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

Python 提供了多种构建命令行工具的方式。本节重点对比两个最常用的方案：

| 特性 | argparse | click |
|------|----------|-------|
| 来源 | Python 标准库 | 第三方库（`pip install click`） |
| 风格 | 命令式（创建 parser → 添加参数 → 解析） | 声明式（装饰器） |
| 子命令 | `add_subparsers()` | `@click.group()` + `@group.command()` |
| 类型验证 | `type=int` 参数 | `click.INT` / `click.Path()` 等 |
| 互斥参数 | `add_mutually_exclusive_group()` | `cls=MutuallyExclusiveOption`（需自定义） |
| 自动帮助 | 内置 `-h/--help` | 内置 `--help`，格式更美观 |
| 颜色输出 | 需手动实现 | `click.style()` / `click.echo()` |
| 进度条 | 需第三方库 | `click.progressbar()` 内置 |
| 学习曲线 | 中等 | 低（装饰器直观） |
| 适用场景 | 不想引入依赖的项目 | 需要丰富 CLI 交互的项目 |

## 选择建议

```
需要命令行参数？
├── 简单脚本（1-2 个参数）→ sys.argv 手动解析
├── 不想引入依赖 → argparse（标准库）
├── 需要子命令 + 丰富交互 → click
└── 需要自动补全 + 类型提示 → typer（基于 click + type hints）
```

## Java 对比

| 特性 | Java | Python |
|------|------|--------|
| 标准方案 | 无（需第三方库） | `argparse`（标准库） |
| 流行框架 | picocli / Apache Commons CLI | click / typer |
| 注解/装饰器 | picocli `@Command` `@Option` | click `@click.command()` `@click.option()` |
| 子命令 | picocli `@Command(subcommands=...)` | click `@click.group()` |
| 类型安全 | 编译时检查 | 运行时验证 |

**Java (picocli) 写法：**
```java
@Command(name = "greet", description = "打招呼工具")
class Greet implements Runnable {
    @Option(names = {"-n", "--name"}, required = true)
    String name;

    @Option(names = {"-c", "--count"}, defaultValue = "1")
    int count;

    public void run() {
        for (int i = 0; i < count; i++) {
            System.out.println("Hello, " + name + "!");
        }
    }
}
```

**Python (argparse) 写法：**
```python
parser = argparse.ArgumentParser(description="打招呼工具")
parser.add_argument("-n", "--name", required=True)
parser.add_argument("-c", "--count", type=int, default=1)
args = parser.parse_args()
for _ in range(args.count):
    print(f"Hello, {args.name}!")
```

**Python (click) 写法：**
```python
@click.command()
@click.option("-n", "--name", required=True)
@click.option("-c", "--count", type=int, default=1)
def greet(name, count):
    """打招呼工具"""
    for _ in range(count):
        click.echo(f"Hello, {name}!")
```

## 实战代码

### 示例 1：argparse 完整示例

**文件：** `examples/argparse_demo.py`

演示 argparse 的完整功能：子命令、互斥参数、类型验证、自定义 Action。

```bash
python examples/argparse_demo.py greet --name Alice --count 3
python examples/argparse_demo.py calc add 10 20
python examples/argparse_demo.py calc mul 5 6
```

### 示例 2：click 完整示例

**文件：** `examples/click_demo.py`

演示 click 的装饰器风格：子命令组、选项/参数、颜色输出、确认提示。

```bash
python examples/click_demo.py greet --name Alice --count 3
python examples/click_demo.py calc add 10 20
python examples/click_demo.py file-info README.md
```

> **注意：** click 是第三方库，运行前需安装：`pip install click`

## 常见陷阱

### 1. argparse 默认值类型

```python
# ✗ 错误：忘记指定 type，参数值是字符串
parser.add_argument("--count", default=1)
args = parser.parse_args(["--count", "3"])
print(args.count + 1)  # "31"！字符串拼接

# ✓ 正确：指定 type=int
parser.add_argument("--count", type=int, default=1)
```

### 2. click 参数顺序

```python
# ✗ 错误：装饰器顺序反了（click 从下往上应用装饰器）
@click.option("--name")
@click.command()
def greet(name): ...

# ✓ 正确：@click.command() 在最外层
@click.command()
@click.option("--name")
def greet(name): ...
```

### 3. 布尔标志的处理

```python
# argparse：使用 store_true
parser.add_argument("--verbose", action="store_true")

# click：使用 is_flag=True 或 flag_value
@click.option("--verbose", is_flag=True)
```

> 💻 **完整可运行代码：** [argparse_demo.py](examples/argparse_demo.py) | [click_demo.py](examples/click_demo.py)

## 参考资料

- [Python 官方文档 - argparse](https://docs.python.org/zh-cn/3/library/argparse.html)
- [click 官方文档](https://click.palletsprojects.com/)
- [typer 官方文档](https://typer.tiangolo.com/)
- [Real Python - argparse 教程](https://realpython.com/command-line-interfaces-python-argparse/)
