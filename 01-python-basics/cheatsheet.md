# Python 基础 速查卡片

> 本速查卡片总结 Python 基础模块的核心语法、常用操作、常见陷阱和面试高频考点。
> 适合日常开发快速查阅和面试前快速回顾。

---

## 核心概念

| 概念 | 说明 | 示例 |
|------|------|------|
| 动态类型 | 变量无需声明类型，运行时确定 | `x = 10; x = "hello"` |
| 一切皆对象 | 函数、类、模块都是对象 | `type(print)` → `<class 'builtin_function_or_method'>` |
| 缩进语法 | 用缩进代替花括号表示代码块 | 4 个空格为标准缩进 |
| 鸭子类型 | 关注行为而非类型 | 只要有 `__iter__` 就能 for 循环 |
| GIL | 全局解释器锁，同一时刻只有一个线程执行 Python 字节码 | 多线程适合 IO 密集型，多进程适合 CPU 密集型 |
| 可变 vs 不可变 | list/dict/set 可变；int/str/tuple 不可变 | `a = [1]; b = a; b.append(2)` → a 也变了 |
| 推导式 | 简洁创建集合的语法糖 | `[x**2 for x in range(5)]` |
| 装饰器 | 不修改函数代码的前提下增强功能 | `@functools.wraps` |
| 上下文管理器 | `with` 语句自动管理资源 | `with open("f.txt") as f:` |
| dataclass | 自动生成 `__init__`/`__repr__`/`__eq__` | `@dataclass class Point:` |

## 常用语法

### 变量与赋值

```python
# 多重赋值
a, b, c = 1, 2, 3

# 交换变量（无需临时变量）
a, b = b, a

# 解包赋值
first, *rest = [1, 2, 3, 4]   # first=1, rest=[2,3,4]

# 类型注解（仅提示，不强制）
name: str = "hello"
nums: list[int] = [1, 2, 3]
```

### 字符串操作

```python
s = "Hello, Python"

s.upper()                  # "HELLO, PYTHON"
s.lower()                  # "hello, python"
s.strip()                  # 去除首尾空白
s.split(", ")              # ["Hello", "Python"]
", ".join(["a", "b"])      # "a, b"
s.replace("Python", "World")  # "Hello, World"
s.startswith("Hello")      # True
s.find("Python")           # 7（索引位置）

# f-string 格式化（推荐）
name, age = "张三", 25
f"{name} 今年 {age} 岁"
f"{3.14159:.2f}"           # "3.14"
f"{1000000:,}"             # "1,000,000"

# 多行字符串
text = """第一行
第二行
第三行"""
```

### 列表（list）

```python
nums = [1, 2, 3, 4, 5]

nums.append(6)             # 末尾添加
nums.insert(0, 0)          # 指定位置插入
nums.pop()                 # 弹出末尾元素
nums.remove(3)             # 删除第一个匹配值
nums.sort()                # 原地排序
sorted(nums, reverse=True) # 返回新列表

# 切片
nums[1:3]                  # [2, 3]
nums[::-1]                 # 反转列表
nums[::2]                  # 步长为 2

# 列表推导式
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
```

### 字典（dict）

```python
d = {"name": "张三", "age": 25}

d["name"]                  # "张三"
d.get("phone", "未知")     # 安全获取，有默认值
d["phone"] = "138xxx"      # 添加/修改
d.pop("age")               # 删除并返回值
d.keys()                   # 所有键
d.values()                 # 所有值
d.items()                  # 所有键值对

# 字典推导式
squares = {x: x**2 for x in range(5)}

# 合并字典（Python 3.9+）
merged = d1 | d2
```

### 元组与集合

```python
# 元组（不可变）
point = (3, 4)
x, y = point              # 解包

# 命名元组
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
p.x                        # 3

# 集合
s = {1, 2, 3}
s.add(4)
s.discard(2)               # 删除（不存在不报错）
s1 & s2                    # 交集
s1 | s2                    # 并集
s1 - s2                    # 差集
```

### 控制流

```python
# 条件表达式（三元运算符）
result = "偶数" if x % 2 == 0 else "奇数"

# for 循环 + enumerate
for i, item in enumerate(["a", "b", "c"]):
    print(f"{i}: {item}")

# for 循环 + zip
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# while + else（循环正常结束时执行 else）
while condition:
    if found:
        break
else:
    print("未找到")

# match-case（Python 3.10+）
match command:
    case "quit":
        exit()
    case "hello":
        print("你好")
    case _:
        print("未知命令")
```

### 函数

```python
# 默认参数
def greet(name, greeting="你好"):
    return f"{greeting}, {name}"

# *args 和 **kwargs
def func(*args, **kwargs):
    print(args)    # 元组
    print(kwargs)  # 字典

# lambda 表达式
square = lambda x: x ** 2
sorted(items, key=lambda x: x["age"])

# 类型注解
def add(a: int, b: int) -> int:
    return a + b

# 仅关键字参数（* 之后的参数必须用关键字传递）
def connect(host, port, *, timeout=30):
    pass
```

### 装饰器

```python
import functools

def timer(func):
    """计时装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} 耗时 {time.time() - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)

# 带参数的装饰器
def repeat(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello():
    print("Hello")
```

### 类与面向对象

```python
from dataclasses import dataclass

# 基本类定义
class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        raise NotImplementedError

# 继承
class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name}: 汪汪！"

# @dataclass（推荐用于数据类）
@dataclass
class Point:
    x: float
    y: float

    def distance(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

# 常用魔术方法
# __init__    构造方法
# __repr__    开发者友好的字符串表示
# __str__     用户友好的字符串表示
# __len__     len() 调用
# __eq__      == 比较
# __lt__      < 比较（支持排序）
# __getitem__ 下标访问 obj[key]
# __iter__    迭代支持
# __enter__/__exit__  上下文管理器
```

### 异常处理

```python
# 基本结构
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"错误: {e}")
except (TypeError, ValueError):
    print("类型或值错误")
else:
    print("无异常时执行")
finally:
    print("始终执行")

# 自定义异常
class BusinessError(Exception):
    def __init__(self, message: str, code: int = 0):
        super().__init__(message)
        self.code = code

# 上下文管理器
from contextlib import contextmanager

@contextmanager
def managed_resource():
    print("获取资源")
    try:
        yield "resource"
    finally:
        print("释放资源")

with managed_resource() as r:
    print(f"使用 {r}")
```

### 文件操作

```python
# 读文件
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()        # 读取全部
    lines = f.readlines()     # 按行读取为列表

# 写文件
with open("file.txt", "w", encoding="utf-8") as f:
    f.write("Hello\n")

# JSON 读写
import json
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# pathlib（推荐）
from pathlib import Path
p = Path("data") / "file.txt"
p.exists()
p.read_text(encoding="utf-8")
p.write_text("内容", encoding="utf-8")
p.parent.mkdir(parents=True, exist_ok=True)
```

### 推导式与生成器

```python
# 列表推导式
[x**2 for x in range(10) if x % 2 == 0]

# 字典推导式
{k: v for k, v in items if v > 0}

# 集合推导式
{x % 3 for x in range(10)}

# 生成器表达式（惰性求值，节省内存）
gen = (x**2 for x in range(1000000))
next(gen)  # 0
next(gen)  # 1

# 生成器函数
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

list(fibonacci(10))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

---

## 常见陷阱

- ⚠️ **可变默认参数** — 函数默认参数使用可变对象（如 list/dict）会在调用间共享状态
  ```python
  # ❌ 错误
  def add_item(item, lst=[]):
      lst.append(item)
      return lst
  add_item(1)  # [1]
  add_item(2)  # [1, 2]  ← 不是 [2]！

  # ✅ 正确
  def add_item(item, lst=None):
      if lst is None:
          lst = []
      lst.append(item)
      return lst
  ```

- ⚠️ **浅拷贝 vs 深拷贝** — 赋值和切片只是浅拷贝，嵌套对象仍共享引用
  ```python
  import copy
  a = [[1, 2], [3, 4]]
  b = a[:]           # 浅拷贝：b[0] 和 a[0] 是同一个列表
  c = copy.deepcopy(a)  # 深拷贝：完全独立
  ```

- ⚠️ **`==` vs `is`** — `==` 比较值，`is` 比较对象身份（内存地址）
  ```python
  a = [1, 2, 3]
  b = [1, 2, 3]
  a == b   # True（值相等）
  a is b   # False（不是同一个对象）

  # 例外：小整数缓存（-5 到 256）
  x = 256
  y = 256
  x is y   # True（缓存复用）
  ```

- ⚠️ **闭包中的循环变量** — 闭包捕获的是变量引用，不是值
  ```python
  # ❌ 错误：所有函数都返回 4
  funcs = [lambda: i for i in range(5)]
  funcs[0]()  # 4

  # ✅ 正确：用默认参数捕获当前值
  funcs = [lambda i=i: i for i in range(5)]
  funcs[0]()  # 0
  ```

- ⚠️ **字符串不可变** — 字符串拼接会创建新对象，大量拼接用 `join`
  ```python
  # ❌ 慢（每次创建新字符串）
  s = ""
  for word in words:
      s += word

  # ✅ 快
  s = "".join(words)
  ```

- ⚠️ **for 循环中修改列表** — 遍历时修改列表会导致意外行为
  ```python
  # ❌ 错误
  nums = [1, 2, 3, 4, 5]
  for n in nums:
      if n % 2 == 0:
          nums.remove(n)  # 跳过元素！

  # ✅ 正确：用推导式创建新列表
  nums = [n for n in nums if n % 2 != 0]
  ```

- ⚠️ **全局变量修改** — 函数内修改全局变量需要 `global` 声明
  ```python
  count = 0
  def increment():
      global count   # 不加 global 会报 UnboundLocalError
      count += 1
  ```

---

## 面试高频考点

- **Python 的 GIL 是什么？对多线程有什么影响？**
  GIL（全局解释器锁）保证同一时刻只有一个线程执行 Python 字节码。多线程适合 IO 密集型任务，CPU 密集型应使用多进程（`multiprocessing`）。

- **`is` 和 `==` 的区别？**
  `is` 比较对象身份（id），`==` 比较值。判断 `None` 用 `is None`。

- **深拷贝和浅拷贝的区别？**
  浅拷贝只复制顶层对象，嵌套对象仍共享引用；深拷贝递归复制所有层级。

- **Python 的可变类型和不可变类型？**
  可变：list、dict、set；不可变：int、float、str、tuple、frozenset。不可变类型可作为 dict 的 key。

- **装饰器的原理和应用场景？**
  装饰器本质是高阶函数，接收函数返回函数。常用于日志、权限校验、缓存（`@functools.lru_cache`）、重试等。

- **`*args` 和 `**kwargs` 的作用？**
  `*args` 收集位置参数为元组，`**kwargs` 收集关键字参数为字典。常用于装饰器和函数转发。

- **列表推导式和生成器表达式的区别？**
  列表推导式 `[...]` 立即生成完整列表；生成器表达式 `(...)` 惰性求值，节省内存。

- **`__init__` 和 `__new__` 的区别？**
  `__new__` 创建实例（类方法），`__init__` 初始化实例（实例方法）。单例模式常重写 `__new__`。

- **Python 如何实现多态？**
  鸭子类型：不检查类型，只关注对象是否有所需方法。无需接口声明，任何实现了相同方法的对象都可互换使用。

- **`with` 语句的原理？**
  上下文管理器协议：对象实现 `__enter__` 和 `__exit__` 方法。`with` 确保资源在使用后被正确释放。

- **Python 与 Java 的主要区别？**
  动态类型 vs 静态类型、解释执行 vs 编译执行、GIL vs 真正多线程、pip vs Maven/Gradle、缩进 vs 花括号。
