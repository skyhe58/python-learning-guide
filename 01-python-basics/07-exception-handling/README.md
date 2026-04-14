# 异常处理

> **模块：** 01-Python 基础
> **难度：** 入门
> **前置知识：** 模块与包管理（06-modules-packages）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

Python 的异常处理机制与 Java 类似，都使用 `try/except`（Java 中是 `try/catch`）来捕获和处理运行时错误。但两者在设计哲学上有本质区别：Java 区分**受检异常（Checked Exception）**和**非受检异常（Unchecked Exception）**，编译器强制要求处理受检异常；Python 则**没有受检异常的概念**，所有异常都是非受检的，是否捕获完全由开发者决定。

Python 的异常处理还有一个 Java 没有的特性：`try/except/else` 中的 `else` 子句——当 `try` 块没有抛出异常时执行。这让"正常流程"和"异常处理"的分离更加清晰。此外，Python 的 `with` 语句（上下文管理器）是资源管理的首选方式，类似 Java 7 引入的 `try-with-resources`，但更加通用和灵活。

Python 遵循 **EAFP（Easier to Ask Forgiveness than Permission）** 原则——先尝试执行，出错再处理；而 Java 更倾向于 **LBYL（Look Before You Leap）**——先检查条件再执行。这种哲学差异深刻影响了两种语言的异常处理风格。

### 核心概念一览

| 概念 | 说明 |
|------|------|
| `try/except` | 捕获异常，类似 Java 的 `try/catch` |
| `except Exception as e` | 捕获特定异常并绑定到变量 |
| `finally` | 无论是否异常都会执行的清理代码 |
| `else` | `try` 块没有异常时执行（Java 没有对应语法） |
| `raise` | 主动抛出异常，类似 Java 的 `throw` |
| `raise ... from ...` | 异常链，保留原始异常信息 |
| 自定义异常 | 继承 `Exception` 类创建自定义异常 |
| `with` 语句 | 上下文管理器，自动管理资源（类似 Java try-with-resources） |
| `__enter__` / `__exit__` | 上下文管理器协议的两个魔术方法 |
| `contextlib` | 标准库模块，提供上下文管理器工具 |

## Java 对比

### 异常体系

| 特性 | Java | Python |
|------|------|--------|
| 异常基类 | `Throwable`（分 `Exception` 和 `Error`） | `BaseException`（分 `Exception` 和系统退出类） |
| 受检异常 | 有（`IOException` 等，编译器强制处理） | **无**（所有异常都是非受检的） |
| 非受检异常 | `RuntimeException` 及其子类 | 所有异常 |
| 捕获语法 | `try/catch/finally` | `try/except/else/finally` |
| 多异常捕获 | `catch (IOException \| SQLException e)` | `except (IOError, ValueError) as e` |
| 抛出异常 | `throw new Exception("msg")` | `raise Exception("msg")` |
| 异常链 | `throw new Exception("msg", cause)` | `raise Exception("msg") from cause` |
| 声明异常 | `throws IOException`（方法签名） | 无需声明（可用文档说明） |
| 资源管理 | `try-with-resources`（Java 7+） | `with` 语句 |

**Java 写法：**
```java
// Java：受检异常必须处理或声明
import java.io.*;

public class ExceptionDemo {
    // 方法签名必须声明受检异常
    public String readFile(String path) throws IOException {
        // try-with-resources 自动关闭资源
        try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
            return reader.readLine();
        } catch (FileNotFoundException e) {
            System.err.println("文件不存在: " + e.getMessage());
            throw e;  // 重新抛出
        } catch (IOException e) {
            System.err.println("读取失败: " + e.getMessage());
            throw new RuntimeException("读取文件失败", e);  // 异常链
        } finally {
            System.out.println("清理完成");
        }
    }
}
```

**Python 写法：**
```python
# Python：无受检异常，无需在函数签名声明
def read_file(path: str) -> str:
    try:
        with open(path, "r") as f:  # with 自动关闭文件
            return f.readline()
    except FileNotFoundError as e:
        print(f"文件不存在: {e}")
        raise  # 重新抛出
    except IOError as e:
        print(f"读取失败: {e}")
        raise RuntimeError("读取文件失败") from e  # 异常链
    else:
        print("读取成功")  # Java 没有 else 子句
    finally:
        print("清理完成")
```

### 自定义异常

| 特性 | Java | Python |
|------|------|--------|
| 定义方式 | `class MyException extends Exception { }` | `class MyException(Exception): pass` |
| 构造函数 | 需要显式定义构造函数 | 可以直接继承，无需额外代码 |
| 异常层级 | 通常创建完整的异常层级树 | 更简洁，按需创建 |
| 异常信息 | `getMessage()` 方法 | `str(e)` 或 `e.args` |

**Java 写法：**
```java
// Java：自定义异常需要较多样板代码
public class BusinessException extends Exception {
    private final int errorCode;

    public BusinessException(String message, int errorCode) {
        super(message);
        this.errorCode = errorCode;
    }

    public BusinessException(String message, int errorCode, Throwable cause) {
        super(message, cause);
        this.errorCode = errorCode;
    }

    public int getErrorCode() { return errorCode; }
}
```

**Python 写法：**
```python
# Python：自定义异常非常简洁
class BusinessError(Exception):
    """业务异常"""
    def __init__(self, message: str, error_code: int):
        super().__init__(message)
        self.error_code = error_code

# 使用
raise BusinessError("余额不足", error_code=4001)
```

### 资源管理对比

| 特性 | Java try-with-resources | Python with 语句 |
|------|------------------------|-------------------|
| 接口要求 | 实现 `AutoCloseable` 接口 | 实现 `__enter__` 和 `__exit__` 方法 |
| 语法 | `try (Resource r = new Resource()) { }` | `with Resource() as r:` |
| 多资源 | `try (R1 r1 = ...; R2 r2 = ...) { }` | `with R1() as r1, R2() as r2:` |
| 自定义 | 实现 `close()` 方法 | 实现 `__enter__`/`__exit__` 或用 `@contextmanager` |
| 灵活性 | 仅用于资源关闭 | 可用于任意"进入/退出"场景（锁、事务、临时状态等） |

**Java 写法：**
```java
// Java：try-with-resources
try (Connection conn = DriverManager.getConnection(url);
     PreparedStatement stmt = conn.prepareStatement(sql)) {
    ResultSet rs = stmt.executeQuery();
    // 处理结果
}  // conn 和 stmt 自动关闭
```

**Python 写法：**
```python
# Python：with 语句
import sqlite3

with sqlite3.connect("test.db") as conn:
    cursor = conn.cursor()
    cursor.execute(sql)
    # 处理结果
# conn 自动关闭（实际上是自动提交/回滚事务）
```

## 实战代码

### 示例：异常处理完整演示

**文件：** `examples/exception_demo.py`

演示 Python 异常处理的完整知识体系：try/except/finally/else、多异常捕获、异常链（raise from）、自定义异常类、上下文管理器（`__enter__`/`__exit__`）、`contextlib.contextmanager`，并在注释中与 Java 对比。

**运行方式：**
```bash
python examples/exception_demo.py
```

**预期输出：**
```
========== try/except/finally/else ==========
--- 基本用法 ---
捕获到异常: division by zero
finally: 无论如何都会执行
--- else 子句 ---
结果: 5.0
else: 没有异常时执行
finally: 清理完成

========== 多异常捕获 ==========
--- 捕获多种异常 ---
值错误: invalid literal for int() with base 10: 'abc'
--- 分别处理不同异常 ---
索引越界: list index out of range
键不存在: 'z'

========== 异常链 (raise from) ==========
--- 异常链演示 ---
转换后的异常: 数据处理失败: 配置格式错误
原始异常: Expecting value: line 1 column 1 (char 0)

========== 自定义异常 ==========
--- 自定义异常层级 ---
捕获到业务异常: 余额不足，需要 1000.00，当前 500.00
错误代码: 4001
--- 自定义异常的继承 ---
捕获到应用异常: 余额不足，需要 1000.00，当前 500.00

========== 上下文管理器 (with) ==========
--- 自定义上下文管理器（类实现）---
[Timer] 开始计时...
执行一些操作...
[Timer] 结束，耗时: 0.10 秒
--- contextlib.contextmanager ---
[TempDir] 创建临时目录: /tmp/xxx
在临时目录中工作...
[TempDir] 清理临时目录: /tmp/xxx
```

## 常见陷阱

### 1. 捕获过于宽泛的异常

Java 开发者习惯 `catch (Exception e)` 捕获所有异常，在 Python 中这是一个坏习惯，因为它会吞掉 `KeyboardInterrupt`（Ctrl+C）和 `SystemExit` 等系统异常。

```python
# ✗ 危险：捕获所有异常，包括 KeyboardInterrupt
try:
    do_something()
except:  # 裸 except，捕获一切！
    pass   # 静默吞掉所有异常

# ✗ 不推荐：Exception 也会捕获太多
try:
    do_something()
except Exception:
    pass

# ✓ 推荐：捕获具体的异常类型
try:
    do_something()
except (ValueError, TypeError) as e:
    print(f"参数错误: {e}")
```

### 2. 在 `except` 中丢失原始异常信息

Java 的异常链通过构造函数传递 `cause`，Python 需要使用 `raise ... from ...` 语法。

```python
# ✗ 错误：丢失原始异常信息
try:
    data = json.loads(text)
except json.JSONDecodeError:
    raise ValueError("数据格式错误")  # 原始异常信息丢失！

# ✓ 正确：使用 raise from 保留异常链
try:
    data = json.loads(text)
except json.JSONDecodeError as e:
    raise ValueError("数据格式错误") from e  # 保留原始异常
```

### 3. 混淆 `else` 和 `finally` 的执行时机

Java 没有 `try/else`，Java 开发者容易混淆 `else` 和 `finally` 的区别。

```python
try:
    result = do_something()
except SomeError:
    print("出错了")       # 只在异常时执行
else:
    print("成功了")       # 只在没有异常时执行（Java 没有这个！）
finally:
    print("总是执行")     # 无论如何都执行
```

### 4. `with` 语句中的异常被吞掉

如果上下文管理器的 `__exit__` 方法返回 `True`，异常会被静默吞掉。

```python
class SilentManager:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        return True  # 返回 True 会吞掉异常！

with SilentManager():
    raise ValueError("这个异常会被吞掉！")
# 不会报错，异常被静默处理了

# ✓ 正确：__exit__ 返回 None 或 False，让异常正常传播
class ProperManager:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"发生异常: {exc_val}")
        return False  # 不吞掉异常
```

### 5. 忘记 Python 没有受检异常

Java 开发者习惯在方法签名中声明 `throws`，Python 没有这个机制。应该在文档字符串中说明可能抛出的异常。

```python
# ✓ 推荐：在 docstring 中说明异常
def divide(a: float, b: float) -> float:
    """除法运算。

    Args:
        a: 被除数
        b: 除数

    Returns:
        商

    Raises:
        ZeroDivisionError: 当除数为 0 时
        TypeError: 当参数不是数字时
    """
    return a / b
```

> 💻 **完整可运行代码：** [exception_demo.py](examples/exception_demo.py)

## 参考资料

- [Python 官方文档 - 错误和异常](https://docs.python.org/zh-cn/3/tutorial/errors.html)
- [Python 官方文档 - 内置异常](https://docs.python.org/zh-cn/3/library/exceptions.html)
- [Python 官方文档 - with 语句](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#the-with-statement)
- [Python 官方文档 - contextlib](https://docs.python.org/zh-cn/3/library/contextlib.html)
- [Real Python - Python Exceptions](https://realpython.com/python-exceptions/)
- [Real Python - Context Managers](https://realpython.com/python-with-statement/)
