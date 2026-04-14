# 初级面试题集

> **模块：** 08-面试与复习
> **难度：** 初级
> **适用阶段：** 完成第一阶段（Python 基础）后复习
> **Python 版本：** >= 3.9

本题集覆盖 Python 基础语法、数据类型、控制流、函数等初级面试高频考点。每道题包含参考答案、详细解析和关联模块链接。

---

## 题目 1：Python 有哪些基本数据类型？可变类型和不可变类型分别有哪些？

**考察知识点：** 数据类型、可变性（mutability）

### 参考答案

Python 的基本数据类型分为两大类：

| 分类 | 类型 | 说明 |
|------|------|------|
| **不可变类型** | `int`, `float`, `bool`, `str`, `tuple`, `frozenset`, `bytes` | 创建后值不可修改 |
| **可变类型** | `list`, `dict`, `set`, `bytearray` | 创建后可以原地修改 |

```python
# 不可变类型：修改会创建新对象
a = "hello"
print(id(a))       # 例如 140234567890
a = a + " world"
print(id(a))       # 不同的 id，说明是新对象

# 可变类型：原地修改，id 不变
b = [1, 2, 3]
print(id(b))       # 例如 140234567900
b.append(4)
print(id(b))       # 相同的 id，说明是同一个对象
```

### 详细解析

不可变类型的"不可变"指的是对象本身的值不能被修改。当你对不可变对象做"修改"操作时（如字符串拼接），Python 实际上创建了一个新对象。这个特性使得不可变类型可以作为字典的键和集合的元素（因为它们的哈希值不会变）。

可变类型可以原地修改，这意味着多个变量引用同一个可变对象时，通过一个变量的修改会影响到其他变量——这是 Python 中最常见的"坑"之一。

**关联模块：** [02-数据类型与变量](../../01-python-basics/02-data-types/)

---

## 题目 2：`==` 和 `is` 的区别是什么？

**考察知识点：** 对象比较、身份标识

### 参考答案

```python
# == 比较值是否相等（调用 __eq__ 方法）
# is 比较是否是同一个对象（比较内存地址 id）

a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True  — 值相等
print(a is b)   # False — 不是同一个对象
print(a is c)   # True  — c 和 a 指向同一个对象

# 特殊情况：小整数缓存（-5 到 256）
x = 256
y = 256
print(x is y)   # True  — Python 缓存了小整数

x = 257
y = 257
print(x is y)   # False — 超出缓存范围（在交互式环境中）

# 最佳实践：判断 None 用 is
value = None
if value is None:      # ✓ 推荐
    print("是 None")
if value == None:      # ✗ 不推荐（可能被 __eq__ 覆盖）
    print("是 None")
```

### 详细解析

`==` 是值比较运算符，底层调用对象的 `__eq__` 方法，可以被自定义类重写。`is` 是身份比较运算符，比较两个对象的内存地址（`id()`），不可被重写。

Python 对小整数（-5 到 256）和短字符串做了缓存优化（interning），所以在这个范围内 `is` 可能返回 `True`，但不应依赖这个行为。

**面试追问：** 为什么判断 `None` 要用 `is` 而不是 `==`？因为 `==` 可能被类的 `__eq__` 方法覆盖，而 `is` 直接比较身份，更安全可靠。

**关联模块：** [02-数据类型与变量](../../01-python-basics/02-data-types/)

---

## 题目 3：列表推导式是什么？和普通 for 循环有什么区别？

**考察知识点：** 列表推导式、Pythonic 编程风格

### 参考答案

```python
# 普通 for 循环
squares = []
for x in range(10):
    if x % 2 == 0:
        squares.append(x ** 2)
# squares = [0, 4, 16, 36, 64]

# 列表推导式（等价写法，更简洁）
squares = [x ** 2 for x in range(10) if x % 2 == 0]

# 字典推导式
word_lengths = {w: len(w) for w in ["hello", "world", "python"]}
# {'hello': 5, 'world': 5, 'python': 6}

# 集合推导式
unique_lengths = {len(w) for w in ["hello", "world", "python"]}
# {5, 6}

# 生成器表达式（惰性求值，节省内存）
total = sum(x ** 2 for x in range(1000000))
```

### 详细解析

列表推导式是 Python 特有的语法糖，比等价的 for 循环更简洁，通常也更快（因为底层用 C 实现的循环）。但过于复杂的推导式会降低可读性，建议嵌套不超过两层。

生成器表达式使用圆括号 `()`，不会一次性生成所有元素，而是按需计算，适合处理大数据量。

**Java 对比：** Java 8 的 Stream API 提供了类似功能：
```java
List<Integer> squares = IntStream.range(0, 10)
    .filter(x -> x % 2 == 0)
    .map(x -> x * x)
    .boxed()
    .collect(Collectors.toList());
```

**关联模块：** [09-列表推导式与生成器](../../01-python-basics/09-comprehensions-generators/)

---

## 题目 4：Python 装饰器是什么？请手写一个简单的装饰器。

**考察知识点：** 装饰器、闭包、高阶函数

### 参考答案

```python
import functools
import time


def timer(func):
    """计时装饰器：测量函数执行时间。"""
    @functools.wraps(func)  # 保留原函数的元信息
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} 执行耗时: {elapsed:.4f} 秒")
        return result
    return wrapper


@timer
def slow_function(n):
    """模拟耗时操作。"""
    total = sum(range(n))
    return total


# 调用（自动计时）
result = slow_function(1000000)
# 输出: slow_function 执行耗时: 0.0312 秒


# 带参数的装饰器
def retry(max_attempts=3):
    """重试装饰器：失败时自动重试。"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    print(f"第 {attempt} 次失败: {e}，重试中...")
        return wrapper
    return decorator


@retry(max_attempts=3)
def unstable_api_call():
    """模拟不稳定的 API 调用。"""
    import random
    if random.random() < 0.7:
        raise ConnectionError("连接失败")
    return "成功"
```

### 详细解析

装饰器本质上是一个接受函数作为参数并返回新函数的高阶函数。`@decorator` 语法是 `func = decorator(func)` 的语法糖。

关键点：
1. `functools.wraps` 保留原函数的 `__name__`、`__doc__` 等元信息
2. `*args, **kwargs` 使装饰器适用于任意参数的函数
3. 带参数的装饰器需要三层嵌套（外层接收参数，中层接收函数，内层是 wrapper）

**Java 对比：** Java 没有装饰器语法，类似功能通过注解 + AOP（如 Spring `@Transactional`）或代理模式实现。

**关联模块：** [04-函数与装饰器](../../01-python-basics/04-functions-decorators/)

---

## 题目 5：什么是 GIL？它对 Python 多线程有什么影响？

**考察知识点：** GIL（全局解释器锁）、并发编程

### 参考答案

```python
import threading
import time

# GIL 的影响演示

# CPU 密集型任务：多线程不会加速
def cpu_bound(n):
    """CPU 密集型：计算密集循环。"""
    total = 0
    for i in range(n):
        total += i * i
    return total

# 单线程
start = time.time()
cpu_bound(10_000_000)
cpu_bound(10_000_000)
single_time = time.time() - start

# 多线程（由于 GIL，不会更快）
start = time.time()
t1 = threading.Thread(target=cpu_bound, args=(10_000_000,))
t2 = threading.Thread(target=cpu_bound, args=(10_000_000,))
t1.start()
t2.start()
t1.join()
t2.join()
multi_time = time.time() - start

print(f"单线程: {single_time:.2f}s")
print(f"多线程: {multi_time:.2f}s")  # 几乎相同甚至更慢

# IO 密集型任务：多线程有效（GIL 在 IO 等待时释放）
# 解决方案：
# - CPU 密集型 → multiprocessing（多进程）
# - IO 密集型 → threading 或 asyncio
# - 混合型 → concurrent.futures
```

### 详细解析

GIL（Global Interpreter Lock）是 CPython 解释器中的一个互斥锁，确保同一时刻只有一个线程执行 Python 字节码。这意味着：

| 场景 | 多线程效果 | 推荐方案 |
|------|-----------|---------|
| CPU 密集型 | ❌ 无加速（受 GIL 限制） | `multiprocessing` 多进程 |
| IO 密集型 | ✅ 有效加速（IO 等待时释放 GIL） | `threading` 或 `asyncio` |

GIL 是 CPython 的实现细节，不是 Python 语言规范的一部分。Jython（Java 实现）和 PyPy（部分版本）没有 GIL。Python 3.13 引入了实验性的 free-threaded 模式（`--disable-gil`）。

**Java 对比：** Java 的 JVM 没有 GIL，多线程可以真正并行执行。Java 通过 `synchronized`、`ReentrantLock` 等机制处理线程安全。

**关联模块：** [10-Python 与 Java 核心差异](../../01-python-basics/10-java-python-diff/)

---

## 题目 6：深拷贝和浅拷贝的区别是什么？

**考察知识点：** 对象拷贝、引用语义

### 参考答案

```python
import copy

# 原始对象（嵌套列表）
original = [[1, 2, 3], [4, 5, 6], {"key": "value"}]

# 浅拷贝：只复制第一层，内部对象仍是引用
shallow = copy.copy(original)
# 等价写法: shallow = original[:] 或 shallow = list(original)

# 深拷贝：递归复制所有层级
deep = copy.deepcopy(original)

# 修改内部对象
original[0].append(999)
original[2]["key"] = "modified"

print(f"original: {original}")
# [[1, 2, 3, 999], [4, 5, 6], {'key': 'modified'}]

print(f"shallow:  {shallow}")
# [[1, 2, 3, 999], [4, 5, 6], {'key': 'modified'}]  ← 受影响！

print(f"deep:     {deep}")
# [[1, 2, 3], [4, 5, 6], {'key': 'value'}]  ← 不受影响
```

### 详细解析

| 操作 | 行为 | 内部对象 |
|------|------|---------|
| 赋值 `b = a` | 不拷贝，只是新增引用 | 共享 |
| 浅拷贝 `copy.copy(a)` | 创建新容器，但内部元素仍是引用 | 共享 |
| 深拷贝 `copy.deepcopy(a)` | 递归创建所有对象的副本 | 独立 |

浅拷贝的常见方式：`list[:]`、`list()`、`dict.copy()`、`copy.copy()`。

**面试追问：** 什么时候用深拷贝？当对象包含嵌套的可变对象（如列表中的列表），且你需要完全独立的副本时。

**关联模块：** [02-数据类型与变量](../../01-python-basics/02-data-types/)

---

## 题目 7：`*args` 和 `**kwargs` 是什么？

**考察知识点：** 函数参数、可变参数

### 参考答案

```python
def demo(*args, **kwargs):
    """
    *args  — 收集所有位置参数为一个 tuple
    **kwargs — 收集所有关键字参数为一个 dict
    """
    print(f"args = {args}")       # tuple
    print(f"kwargs = {kwargs}")   # dict

demo(1, 2, 3, name="Alice", age=25)
# args = (1, 2, 3)
# kwargs = {'name': 'Alice', 'age': 25}


# 实际应用 1：装饰器中传递任意参数
def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"调用 {func.__name__}({args}, {kwargs})")
        return func(*args, **kwargs)
    return wrapper


# 实际应用 2：解包操作
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
print(add(*nums))       # 解包列表 → add(1, 2, 3) = 6

config = {"a": 10, "b": 20, "c": 30}
print(add(**config))    # 解包字典 → add(a=10, b=20, c=30) = 60


# Python 参数顺序规则
def full_example(pos, /, normal, *args, kw_only, **kwargs):
    """
    pos       — 仅位置参数（/ 之前）
    normal    — 普通参数
    *args     — 可变位置参数
    kw_only   — 仅关键字参数（* 或 *args 之后）
    **kwargs  — 可变关键字参数
    """
    pass
```

### 详细解析

`*args` 和 `**kwargs` 是 Python 的可变参数机制。`*` 和 `**` 是解包运算符，`args` 和 `kwargs` 只是约定俗成的名字。

Python 函数参数的完整顺序：位置参数 → `*args` → 关键字参数 → `**kwargs`。Python 3.8+ 还支持 `/` 分隔符标记仅位置参数。

**Java 对比：** Java 使用 `...`（varargs）实现可变参数，但只支持一种类型且只能有一个：`void method(String... args)`。Python 的 `*args` + `**kwargs` 更灵活。

**关联模块：** [04-函数与装饰器](../../01-python-basics/04-functions-decorators/)

---

## 题目 8：`with` 语句的作用是什么？如何自定义上下文管理器？

**考察知识点：** 上下文管理器、资源管理

### 参考答案

```python
# with 语句确保资源正确释放（即使发生异常）
with open("file.txt", "r") as f:
    content = f.read()
# 离开 with 块后，文件自动关闭（即使读取时出错）


# 自定义上下文管理器 — 方式 1：类实现
class Timer:
    """计时上下文管理器。"""
    def __enter__(self):
        import time
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.elapsed = time.time() - self.start
        print(f"耗时: {self.elapsed:.4f} 秒")
        return False  # 不抑制异常

with Timer() as t:
    total = sum(range(1000000))
# 输出: 耗时: 0.0234 秒


# 自定义上下文管理器 — 方式 2：contextmanager 装饰器
from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    """资源管理示例。"""
    print(f"获取资源: {name}")
    try:
        yield name  # yield 之前是 __enter__，之后是 __exit__
    finally:
        print(f"释放资源: {name}")

with managed_resource("数据库连接") as res:
    print(f"使用资源: {res}")
# 获取资源: 数据库连接
# 使用资源: 数据库连接
# 释放资源: 数据库连接
```

### 详细解析

`with` 语句是 Python 的上下文管理协议，通过 `__enter__` 和 `__exit__` 两个魔术方法实现。它确保资源在使用后被正确释放，即使发生异常。

`__exit__` 方法接收异常信息（`exc_type`, `exc_val`, `exc_tb`），返回 `True` 会抑制异常，返回 `False`（默认）会让异常继续传播。

**Java 对比：** Java 7 引入了 try-with-resources，功能类似：
```java
try (FileReader fr = new FileReader("file.txt")) {
    // 使用资源
} // 自动调用 fr.close()
```

**关联模块：** [07-异常处理](../../01-python-basics/07-exception-handling/) | [08-文件操作](../../01-python-basics/08-file-operations/)

---

## 题目 9：Python 2 和 Python 3 的主要区别有哪些？

**考察知识点：** Python 版本差异

### 参考答案

| 特性 | Python 2 | Python 3 |
|------|----------|----------|
| print | `print "hello"`（语句） | `print("hello")`（函数） |
| 整数除法 | `3 / 2 = 1`（截断） | `3 / 2 = 1.5`（真除法） |
| 字符串 | `str` 是字节，`unicode` 是文本 | `str` 是文本（Unicode），`bytes` 是字节 |
| range | `range()` 返回列表 | `range()` 返回迭代器 |
| 输入 | `raw_input()` | `input()` |
| 异常语法 | `except Exception, e:` | `except Exception as e:` |
| 字典方法 | `.keys()` 返回列表 | `.keys()` 返回视图 |
| 类 | 经典类和新式类 | 只有新式类（默认继承 `object`） |
| 编码声明 | 需要 `# -*- coding: utf-8 -*-` | 默认 UTF-8 |
| 维护状态 | **2020 年已停止维护** | 当前活跃版本 |

```python
# Python 3 的关键改进

# 1. 真除法
print(3 / 2)    # 1.5（Python 3）
print(3 // 2)   # 1（整数除法，两个版本都支持）

# 2. f-string（Python 3.6+）
name = "World"
print(f"Hello, {name}!")

# 3. 类型提示（Python 3.5+）
def greet(name: str) -> str:
    return f"Hello, {name}"

# 4. walrus 运算符（Python 3.8+）
if (n := len("hello")) > 3:
    print(f"长度 {n} 大于 3")

# 5. match-case（Python 3.10+）
match status:
    case 200:
        print("OK")
    case 404:
        print("Not Found")
```

### 详细解析

Python 2 已于 2020 年 1 月 1 日正式停止维护（EOL）。所有新项目都应使用 Python 3。面试中问这个问题主要考察候选人是否了解 Python 的发展历史和关键变化。

最重要的变化是字符串处理：Python 3 中 `str` 默认是 Unicode 文本，这解决了 Python 2 中令人头疼的编码问题。

**关联模块：** [10-Python 与 Java 核心差异](../../01-python-basics/10-java-python-diff/)

---

## 题目 10：解释 Python 的命名空间和作用域规则（LEGB）。

**考察知识点：** 作用域、命名空间、LEGB 规则

### 参考答案

```python
# LEGB 规则：Python 按以下顺序查找变量
# L - Local（局部作用域）
# E - Enclosing（外层函数作用域，闭包）
# G - Global（模块全局作用域）
# B - Built-in（内置作用域）

x = "global"  # G: 全局

def outer():
    x = "enclosing"  # E: 外层函数

    def inner():
        x = "local"  # L: 局部
        print(x)     # 输出 "local"（优先找 L）

    inner()
    print(x)  # 输出 "enclosing"

outer()
print(x)  # 输出 "global"


# global 和 nonlocal 关键字
count = 0

def increment():
    global count       # 声明使用全局变量
    count += 1

def make_counter():
    n = 0
    def counter():
        nonlocal n     # 声明使用外层函数变量
        n += 1
        return n
    return counter

c = make_counter()
print(c())  # 1
print(c())  # 2
print(c())  # 3
```

### 详细解析

Python 使用 LEGB 规则解析变量名。当你引用一个变量时，Python 按 L → E → G → B 的顺序查找，找到第一个匹配就停止。

关键点：
- 在函数内部赋值会创建局部变量（即使全局有同名变量）
- `global` 关键字让函数内部可以修改全局变量
- `nonlocal` 关键字让内层函数可以修改外层函数的变量（闭包场景）
- Python 没有块级作用域（`if`/`for` 内定义的变量在块外仍可访问）

**Java 对比：** Java 有块级作用域（`{}`），变量在块外不可访问。Java 没有闭包中修改外部变量的 `nonlocal` 等价物（lambda 中引用的变量必须是 effectively final）。

**关联模块：** [04-函数与装饰器](../../01-python-basics/04-functions-decorators/) | [06-模块与包管理](../../01-python-basics/06-modules-packages/)
