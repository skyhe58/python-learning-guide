# 列表推导式与生成器

> **模块：** 01-Python 基础
> **难度：** 进阶
> **前置知识：** 文件操作（08-file-operations）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

**推导式（Comprehension）** 是 Python 最具特色的语法之一，它用一行简洁的表达式创建列表、字典或集合。Java 开发者可以把推导式理解为 **Stream API 的简写形式**——`[x*2 for x in range(10) if x > 3]` 等价于 Java 的 `IntStream.range(0, 10).filter(x -> x > 3).map(x -> x * 2).boxed().toList()`，但 Python 的写法明显更短更直观。

**生成器（Generator）** 是 Python 的惰性求值机制。生成器函数使用 `yield` 关键字，每次调用只产生一个值，不会一次性把所有结果加载到内存。这类似于 Java 的 `Stream`——都是惰性的、按需计算的。但 Python 的生成器语法更简单：把列表推导式的方括号 `[]` 换成圆括号 `()` 就变成了生成器表达式。

Python 标准库的 `itertools` 模块提供了大量高效的迭代器工具，功能类似 Java Stream API 的中间操作（`map`、`filter`、`flatMap`、`limit` 等），但以函数式工具的形式提供。掌握推导式 + 生成器 + itertools，就掌握了 Python 数据处理的核心武器。

### 核心概念一览

| 概念 | 说明 |
|------|------|
| 列表推导式 | `[expr for x in iterable if condition]` |
| 字典推导式 | `{key: value for x in iterable if condition}` |
| 集合推导式 | `{expr for x in iterable if condition}` |
| 生成器表达式 | `(expr for x in iterable if condition)` — 惰性求值 |
| 生成器函数 | 使用 `yield` 的函数，返回生成器对象 |
| `yield` | 暂停函数执行并产出一个值，下次调用时从暂停处继续 |
| `yield from` | 委托给另一个生成器（Python 3.3+） |
| `itertools` | 标准库迭代器工具模块 |
| `next()` | 获取迭代器/生成器的下一个值 |

## Java 对比

### 推导式 vs Stream API

| 特性 | Java Stream API | Python 推导式 |
|------|----------------|---------------|
| 过滤 | `.filter(x -> x > 3)` | `if x > 3`（推导式内） |
| 映射 | `.map(x -> x * 2)` | `x * 2`（推导式表达式部分） |
| 收集为列表 | `.collect(Collectors.toList())` | `[...]`（方括号即列表） |
| 收集为集合 | `.collect(Collectors.toSet())` | `{...}`（花括号即集合） |
| 收集为字典 | `.collect(Collectors.toMap(...))` | `{k: v ...}`（花括号 + 冒号） |
| 嵌套/扁平化 | `.flatMap(...)` | 嵌套 `for` 子句 |
| 惰性求值 | Stream 默认惰性 | 推导式立即求值，生成器表达式惰性 |

**Java 写法：**
```java
import java.util.*;
import java.util.stream.*;

List<Integer> numbers = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

// 过滤 + 映射 + 收集
List<Integer> result = numbers.stream()
    .filter(x -> x % 2 == 0)
    .map(x -> x * x)
    .collect(Collectors.toList());
// [4, 16, 36, 64, 100]

// 收集为 Map
Map<Integer, Integer> squareMap = numbers.stream()
    .collect(Collectors.toMap(x -> x, x -> x * x));

// 嵌套扁平化
List<List<Integer>> nested = List.of(List.of(1, 2), List.of(3, 4));
List<Integer> flat = nested.stream()
    .flatMap(Collection::stream)
    .collect(Collectors.toList());
// [1, 2, 3, 4]
```

**Python 写法：**
```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 过滤 + 映射（一行搞定）
result = [x * x for x in numbers if x % 2 == 0]
# [4, 16, 36, 64, 100]

# 字典推导式
square_map = {x: x * x for x in numbers}

# 嵌套扁平化
nested = [[1, 2], [3, 4]]
flat = [x for sublist in nested for x in sublist]
# [1, 2, 3, 4]
```

### 生成器 vs Stream

| 特性 | Java Stream | Python 生成器 |
|------|------------|---------------|
| 创建方式 | `Stream.of(...)` / `collection.stream()` | `yield` 函数 / 生成器表达式 |
| 惰性求值 | 是 | 是 |
| 一次性消费 | 是（Stream 只能遍历一次） | 是（生成器也只能遍历一次） |
| 无限序列 | `Stream.iterate(0, x -> x + 1)` | `def count(): yield n; n += 1` |
| 终端操作 | `.forEach()` / `.collect()` / `.count()` | `list()` / `for` 循环 / `next()` |
| 暂停/恢复 | 不支持 | `yield` 天然支持暂停和恢复 |

**Java 写法：**
```java
// Java：无限流
Stream<Integer> infiniteStream = Stream.iterate(0, x -> x + 1);
List<Integer> first10 = infiniteStream
    .limit(10)
    .collect(Collectors.toList());

// Java：自定义 Stream（较复杂）
Stream<Integer> fibonacci = Stream.iterate(
    new int[]{0, 1},
    f -> new int[]{f[1], f[0] + f[1]}
).map(f -> f[0]);
```

**Python 写法：**
```python
# Python：生成器函数（简洁直观）
def count(start=0):
    n = start
    while True:
        yield n
        n += 1

# 取前 10 个
from itertools import islice
first_10 = list(islice(count(), 10))

# 斐波那契生成器
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
```

### itertools vs Stream 中间操作

| 功能 | Java Stream | Python itertools |
|------|------------|-----------------|
| 取前 N 个 | `.limit(n)` | `itertools.islice(it, n)` |
| 跳过前 N 个 | `.skip(n)` | `itertools.islice(it, n, None)` |
| 链接多个 | `Stream.concat(s1, s2)` | `itertools.chain(it1, it2)` |
| 分组 | `Collectors.groupingBy(...)` | `itertools.groupby(sorted_it, key)` |
| 累积 | `.reduce(...)` | `itertools.accumulate(it)` |
| 笛卡尔积 | 嵌套 flatMap | `itertools.product(it1, it2)` |
| 排列组合 | 无内置 | `itertools.permutations` / `combinations` |
| 无限重复 | `Stream.generate(...)` | `itertools.repeat(val)` / `itertools.cycle(it)` |

## 实战代码

### 示例：推导式与生成器完整演示

**文件：** `examples/comprehensions_demo.py`

演示 Python 推导式与生成器的完整知识体系：列表推导式（含条件过滤、嵌套）、字典推导式、集合推导式、生成器函数（yield）、生成器表达式、itertools 常用函数，并在注释中与 Java Stream API 对比。

**运行方式：**
```bash
python examples/comprehensions_demo.py
```

**预期输出：**
```
========== 列表推导式 ==========
--- 基本用法 ---
平方数: [1, 4, 9, 16, 25]
--- 条件过滤 ---
偶数平方: [4, 16, 36, 64, 100]
--- 嵌套推导式 ---
扁平化: [1, 2, 3, 4, 5, 6]
九九乘法（部分）: ['1x1=1', '1x2=2', '1x3=3', ...]
--- 条件表达式 ---
奇偶标记: ['奇', '偶', '奇', '偶', '奇']

========== 字典推导式 ==========
平方字典: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
单词长度: {'hello': 5, 'world': 5, 'python': 6}
键值互换: {1: 'a', 2: 'b', 3: 'c'}

========== 集合推导式 ==========
首字母集合: {'P', 'J', 'G'}
去重平方: {0, 1, 4, 9}

========== 生成器函数 (yield) ==========
--- 基本生成器 ---
倒计时: 5 4 3 2 1
--- 斐波那契生成器 ---
前 10 个斐波那契数: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
--- yield from ---
扁平化结果: [1, 2, 3, 4, 5, 6]

========== 生成器表达式 ==========
生成器对象: <generator object ...>
求和（惰性）: 285
内存对比: 列表占用 >> 生成器占用

========== itertools 常用函数 ==========
--- chain（链接多个迭代器）---
chain: [1, 2, 3, 'a', 'b', 'c']
--- islice（切片）---
islice: [0, 1, 2, 3, 4]
--- product（笛卡尔积）---
product: [('A', 1), ('A', 2), ('B', 1), ('B', 2)]
--- groupby（分组）---
True: [2, 4, 6]
False: [1, 3, 5]
--- accumulate（累积）---
累积和: [1, 3, 6, 10, 15]
--- combinations / permutations ---
组合 C(3,2): [('a', 'b'), ('a', 'c'), ('b', 'c')]
排列 P(3,2): [('a', 'b'), ('a', 'c'), ('b', 'a'), ('b', 'c'), ('c', 'a'), ('c', 'b')]
```

## 常见陷阱

### 1. 推导式过于复杂，可读性差

推导式虽然简洁，但嵌套过深会严重影响可读性。

```python
# ✗ 不推荐：三层嵌套推导式，难以理解
result = [f(x, y, z) for x in xs for y in ys if g(y) for z in zs if h(x, z)]

# ✓ 推荐：超过两层嵌套时，改用普通循环
result = []
for x in xs:
    for y in ys:
        if g(y):
            for z in zs:
                if h(x, z):
                    result.append(f(x, y, z))
```

### 2. 生成器只能遍历一次

Java 的 Stream 也只能消费一次，但 Java 开发者可能不习惯 Python 生成器的这个特性。

```python
gen = (x * x for x in range(5))

list(gen)  # [0, 1, 4, 9, 16] — 第一次正常
list(gen)  # [] — 第二次为空！生成器已耗尽

# ✓ 如果需要多次使用，转为列表
squares = list(x * x for x in range(5))
```

### 3. 推导式中的变量泄漏（Python 2 遗留问题）

Python 3 中推导式有自己的作用域，不会泄漏变量。但 `for` 循环会。

```python
# Python 3：推导式不泄漏变量
[x for x in range(5)]
# print(x)  # NameError（推导式内的 x 不泄漏）

# 但 for 循环会泄漏！
for x in range(5):
    pass
print(x)  # 4 — 循环变量泄漏到外部作用域
```

### 4. 在推导式中使用 `walrus operator` 时的陷阱

Python 3.8 引入的海象运算符 `:=` 在推导式中使用时需要注意作用域。

```python
# ✓ 正确用法：避免重复计算
results = [y for x in data if (y := expensive_func(x)) > threshold]

# ✗ 注意：y 会泄漏到推导式外部！
print(y)  # 最后一个满足条件的 y 值
```

### 5. 生成器函数中 `return` 和 `yield` 的混淆

```python
# ✗ 注意：生成器函数中的 return 不返回值，而是触发 StopIteration
def bad_generator():
    yield 1
    return 2  # 这个 2 不会被 for 循环获取到！

for x in bad_generator():
    print(x)  # 只打印 1

# return 的值存储在 StopIteration 异常的 value 属性中
gen = bad_generator()
next(gen)  # 1
try:
    next(gen)
except StopIteration as e:
    print(e.value)  # 2
```

> 💻 **完整可运行代码：** [comprehensions_demo.py](examples/comprehensions_demo.py)

## 参考资料

- [Python 官方文档 - 列表推导式](https://docs.python.org/zh-cn/3/tutorial/datastructures.html#list-comprehensions)
- [Python 官方文档 - 生成器](https://docs.python.org/zh-cn/3/tutorial/classes.html#generators)
- [Python 官方文档 - itertools](https://docs.python.org/zh-cn/3/library/itertools.html)
- [Python 官方文档 - 生成器表达式](https://docs.python.org/zh-cn/3/reference/expressions.html#generator-expressions)
- [Real Python - List Comprehensions](https://realpython.com/list-comprehension-python/)
- [Real Python - Introduction to Python Generators](https://realpython.com/introduction-to-python-generators/)
