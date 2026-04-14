# 文件操作

> **模块：** 01-Python 基础
> **难度：** 入门
> **前置知识：** 异常处理（07-exception-handling）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

Python 的文件操作比 Java 简洁得多。Java 需要在 `java.io`（传统 IO）和 `java.nio`（NIO）两套 API 之间选择，还要处理各种流的包装（`FileInputStream` → `InputStreamReader` → `BufferedReader`）；Python 只需要一个 `open()` 函数就能搞定大部分场景，配合 `with` 语句自动管理资源。

Python 3.4 引入的 **pathlib** 模块是路径操作的现代方式，提供面向对象的路径 API，类似 Java 的 `java.nio.file.Path`。相比传统的 `os.path` 模块（纯函数式），`pathlib` 更直观、更 Pythonic——路径可以用 `/` 运算符拼接，方法链式调用，代码可读性大幅提升。

Python 标准库还内置了 `csv` 和 `json` 模块，可以直接读写 CSV 和 JSON 文件，无需第三方库。Java 处理 CSV 通常需要 Apache Commons CSV 或 OpenCSV，处理 JSON 需要 Jackson 或 Gson——Python 在这方面的"开箱即用"体验明显更好。

### 核心概念一览

| 概念 | 说明 |
|------|------|
| `open()` | 打开文件，返回文件对象，支持多种模式（r/w/a/b） |
| `with open(...) as f` | 上下文管理器方式打开文件，自动关闭 |
| `read()` / `readline()` / `readlines()` | 读取文件内容的三种方式 |
| `write()` / `writelines()` | 写入文件内容 |
| `pathlib.Path` | 面向对象的路径操作（Python 3.4+） |
| `os` / `os.path` | 传统的文件系统操作模块 |
| `os.walk()` | 递归遍历目录树 |
| `csv` 模块 | 标准库 CSV 读写 |
| `json` 模块 | 标准库 JSON 读写 |
| 文件模式 | `r`(读) `w`(写) `a`(追加) `b`(二进制) `x`(排他创建) |

## Java 对比

### 文件读写

| 特性 | Java | Python |
|------|------|--------|
| 读取文本文件 | `BufferedReader` + `FileReader` 或 `Files.readString()` | `open("f.txt").read()` 或 `Path("f.txt").read_text()` |
| 写入文本文件 | `BufferedWriter` + `FileWriter` 或 `Files.writeString()` | `open("f.txt", "w").write(text)` 或 `Path("f.txt").write_text(text)` |
| 逐行读取 | `reader.readLine()` 循环 | `for line in f:` 迭代 |
| 编码指定 | `new InputStreamReader(fis, "UTF-8")` | `open("f.txt", encoding="utf-8")` |
| 资源管理 | `try-with-resources` | `with open(...) as f:` |
| 二进制读写 | `FileInputStream` / `FileOutputStream` | `open("f.bin", "rb")` / `open("f.bin", "wb")` |

**Java 写法：**
```java
import java.io.*;
import java.nio.file.*;

// Java：读取文件需要多层包装
// 传统方式
try (BufferedReader reader = new BufferedReader(
        new InputStreamReader(
            new FileInputStream("data.txt"), "UTF-8"))) {
    String line;
    while ((line = reader.readLine()) != null) {
        System.out.println(line);
    }
}

// NIO 方式（Java 11+，简洁一些）
String content = Files.readString(Path.of("data.txt"));
List<String> lines = Files.readAllLines(Path.of("data.txt"));
```

**Python 写法：**
```python
# Python：一个 open() 搞定
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:  # 逐行迭代，内存友好
        print(line.strip())

# 一次性读取全部内容
content = open("data.txt").read()

# pathlib 方式（更现代）
from pathlib import Path
content = Path("data.txt").read_text(encoding="utf-8")
lines = Path("data.txt").read_text().splitlines()
```

### 路径操作

| 特性 | Java (`java.nio.file.Path`) | Python (`pathlib.Path`) |
|------|----------------------------|------------------------|
| 创建路径 | `Path.of("dir", "file.txt")` | `Path("dir") / "file.txt"` |
| 获取文件名 | `path.getFileName()` | `path.name` |
| 获取父目录 | `path.getParent()` | `path.parent` |
| 获取扩展名 | 无内置方法 | `path.suffix` |
| 文件是否存在 | `Files.exists(path)` | `path.exists()` |
| 是否为目录 | `Files.isDirectory(path)` | `path.is_dir()` |
| 列出目录 | `Files.list(path)` | `path.iterdir()` 或 `path.glob("*")` |
| 递归查找 | `Files.walk(path)` | `path.rglob("*.py")` |
| 绝对路径 | `path.toAbsolutePath()` | `path.resolve()` |

**Java 写法：**
```java
import java.nio.file.*;

Path dir = Path.of("src", "main", "java");
Path file = dir.resolve("App.java");
System.out.println(file.getFileName());   // App.java
System.out.println(file.getParent());     // src/main/java
System.out.println(Files.exists(file));   // true/false

// 递归遍历
Files.walk(Path.of("src"))
    .filter(p -> p.toString().endsWith(".java"))
    .forEach(System.out::println);
```

**Python 写法：**
```python
from pathlib import Path

dir_path = Path("src") / "main" / "python"  # / 运算符拼接路径
file_path = dir_path / "app.py"
print(file_path.name)      # app.py
print(file_path.parent)    # src/main/python
print(file_path.suffix)    # .py（Java 没有内置方法获取扩展名）
print(file_path.exists())  # True/False

# 递归查找所有 .py 文件
for py_file in Path("src").rglob("*.py"):
    print(py_file)
```

### 目录遍历

| 特性 | Java | Python |
|------|------|--------|
| 列出目录 | `Files.list(path)` | `os.listdir()` 或 `Path.iterdir()` |
| 递归遍历 | `Files.walk(path)` | `os.walk()` 或 `Path.rglob()` |
| 模式匹配 | `PathMatcher` + glob | `Path.glob()` / `Path.rglob()` |

## 实战代码

### 示例：文件操作完整演示

**文件：** `examples/file_ops_demo.py`

演示 Python 文件操作的完整知识体系：文件读写（open/read/write）、with 语句、pathlib 路径操作、os.walk 目录遍历、CSV/JSON 文件读写、错误处理（FileNotFoundError 等），并在注释中与 Java 对比。

**运行方式：**
```bash
python examples/file_ops_demo.py
```

**预期输出：**
```
========== 文件读写基础 ==========
--- 写入文件 ---
文件写入成功: demo_output.txt
--- 读取文件（三种方式）---
read(): Python 文件操作演示
第1行...
readline(): Python 文件操作演示
readlines(): ['Python 文件操作演示\n', '第1行: ...\n', ...]
--- 逐行迭代（内存友好）---
> Python 文件操作演示
> 第1行: 这是测试内容
...
--- 追加写入 ---
追加写入成功

========== pathlib 路径操作 ==========
--- 路径基本操作 ---
当前目录: /path/to/current
文件名: file_ops_demo.py
父目录: /path/to/examples
扩展名: .py
--- 路径拼接（/ 运算符）---
拼接结果: data/output/result.csv
--- 文件查找 ---
当前目录下的 .py 文件: [...]

========== os.walk 目录遍历 ==========
目录: .
  子目录: [...]
  文件: [...]

========== CSV 文件读写 ==========
--- 写入 CSV ---
CSV 写入成功: demo_data.csv
--- 读取 CSV ---
张三, 25, Python
李四, 30, Java
王五, 28, Go

========== JSON 文件读写 ==========
--- 写入 JSON ---
JSON 写入成功: demo_data.json
--- 读取 JSON ---
姓名: 张三, 技能: ['Python', 'Java']

========== 错误处理 ==========
--- FileNotFoundError ---
文件不存在: [Errno 2] No such file or directory: '不存在的文件.txt'
--- PermissionError ---
（跳过权限测试）
--- 编码错误处理 ---
使用 errors='replace' 处理编码错误

========== 清理临时文件 ==========
临时文件已清理
```

## 常见陷阱

### 1. 忘记关闭文件

Java 开发者习惯 `try-with-resources`，但在 Python 中可能忘记用 `with`。

```python
# ✗ 不推荐：忘记关闭文件
f = open("data.txt")
content = f.read()
# 忘记 f.close()，文件句柄泄漏！

# ✓ 推荐：始终使用 with 语句
with open("data.txt") as f:
    content = f.read()
# 自动关闭，即使发生异常
```

### 2. 文件编码问题

Java 默认使用平台编码，Python 3 在不同操作系统上默认编码不同（Windows 可能是 GBK）。

```python
# ✗ 危险：不指定编码，Windows 上可能用 GBK
with open("data.txt") as f:
    content = f.read()  # Windows 上可能乱码

# ✓ 推荐：始终显式指定编码
with open("data.txt", encoding="utf-8") as f:
    content = f.read()
```

### 3. 用 `os.path` 拼接路径时的分隔符问题

Java 有 `File.separator`，Python 的 `os.path.join()` 也能处理，但 `pathlib` 更优雅。

```python
# ✗ 不推荐：手动拼接路径
path = "dir" + "/" + "file.txt"  # Windows 上可能有问题

# ✓ 推荐：使用 pathlib
from pathlib import Path
path = Path("dir") / "file.txt"  # 自动处理分隔符
```

### 4. 大文件一次性读入内存

```python
# ✗ 危险：大文件会占用大量内存
with open("huge_file.txt") as f:
    content = f.read()  # 整个文件加载到内存

# ✓ 推荐：逐行迭代
with open("huge_file.txt") as f:
    for line in f:  # 逐行读取，内存友好
        process(line)
```

### 5. `w` 模式会清空文件

Java 的 `FileWriter` 默认也是覆盖模式，但 Python 开发者更容易忽略这一点。

```python
# ✗ 危险：w 模式会清空已有内容！
with open("log.txt", "w") as f:
    f.write("新内容")  # 原有内容全部丢失

# ✓ 追加模式
with open("log.txt", "a") as f:
    f.write("新内容\n")  # 追加到文件末尾
```

> 💻 **完整可运行代码：** [file_ops_demo.py](examples/file_ops_demo.py)

## 参考资料

- [Python 官方文档 - 文件读写](https://docs.python.org/zh-cn/3/tutorial/inputoutput.html#reading-and-writing-files)
- [Python 官方文档 - pathlib](https://docs.python.org/zh-cn/3/library/pathlib.html)
- [Python 官方文档 - os.path](https://docs.python.org/zh-cn/3/library/os.path.html)
- [Python 官方文档 - csv 模块](https://docs.python.org/zh-cn/3/library/csv.html)
- [Python 官方文档 - json 模块](https://docs.python.org/zh-cn/3/library/json.html)
- [Real Python - Reading and Writing Files](https://realpython.com/read-write-files-python/)
- [Real Python - Python pathlib](https://realpython.com/python-pathlib/)
