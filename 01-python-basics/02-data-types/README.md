# 数据类型与变量

> **模块：** 01-Python 基础
> **难度：** 入门
> **前置知识：** 环境搭建（01-environment-setup）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

数据类型是编程语言的基石。对于 Java 开发者来说，最大的思维转变在于：**Python 是动态类型语言，变量不需要声明类型，类型在运行时自动推断。** 这意味着同一个变量可以在不同时刻指向不同类型的对象。

Python 的类型系统遵循"鸭子类型"（Duck Typing）哲学——"如果它走起来像鸭子、叫起来像鸭子，那它就是鸭子"。与 Java 的编译期类型检查不同，Python 更关注对象的行为（方法和属性），而非对象的类型声明。

Python 内置了丰富的数据类型，涵盖数值、序列、映射、集合和特殊类型。这些类型大多比 Java 对应类型更灵活、更易用，但也带来了一些需要注意的陷阱（如可变对象作为默认参数）。

### Python 内置数据类型概览

| 分类 | 类型 | 说明 | 是否可变 |
|------|------|------|----------|
| 数值 | `int` | 整数（无大小限制） | 不可变 |
| 数值 | `float` | 浮点数 | 不可变 |
| 数值 | `bool` | 布尔值（`True`/`False`） | 不可变 |
| 序列 | `str` | 字符串（Unicode） | 不可变 |
| 序列 | `list` | 列表（有序、可重复） | **可变** |
| 序列 | `tuple` | 元组（有序、可重复） | 不可变 |
| 映射 | `dict` | 字典（键值对） | **可变** |
| 集合 | `set` | 集合（无序、不重复） | **可变** |
| 集合 | `frozenset` | 冻结集合 | 不可变 |
| 特殊 | `None` | 空值（类似 Java 的 `null`） | — |

## Java 对比

### 类型系统对比

| 特性 | Java | Python |
|------|------|--------|
| 类型系统 | 静态类型（编译期检查） | 动态类型（运行时推断） |
| 变量声明 | 必须声明类型：`int x = 10;` | 直接赋值：`x = 10` |
| 类型推断 | Java 10+ `var`（仅局部变量） | 所有变量自动推断 |
| 基本类型 | 有原始类型（`int`）和包装类（`Integer`） | 一切皆对象，无原始类型 |
| 整数范围 | `int` 32位，`long` 64位 | 无限精度（自动扩展） |
| 空值 | `null` | `None` |
| 类型注解 | 强制（编译器检查） | 可选（仅提示，不强制） |
| 字符串 | 不可变（`String`），可变（`StringBuilder`） | 不可变（`str`） |

### 数据类型对照表

| Java 类型 | Python 类型 | 说明 |
|-----------|-------------|------|
| `int` / `Integer` | `int` | Python 整数无大小限制 |
| `double` / `Double` | `float` | Python 浮点数为双精度 |
| `boolean` / `Boolean` | `bool` | Python 用 `True`/`False`（首字母大写） |
| `String` | `str` | 都是不可变的 |
| `ArrayList<T>` | `list` | Python list 可混合存储不同类型 |
| `HashMap<K,V>` | `dict` | Python 3.7+ dict 保持插入顺序 |
| `int[]` / `T[]` | `tuple` | tuple 不可变，更接近 Java 数组的不可变性 |
| `HashSet<T>` | `set` | 用法基本一致 |
| `null` | `None` | Python 用 `is None` 判断 |

### 变量声明对比

**Java 写法：**
```java
// Java：必须声明类型
int age = 25;
String name = "Alice";
double price = 19.99;
boolean isActive = true;
List<String> names = new ArrayList<>();
Map<String, Integer> scores = new HashMap<>();

// Java 10+ 类型推断（仅局部变量）
var count = 100;  // 编译器推断为 int
```

**Python 写法：**
```python
# Python：直接赋值，类型自动推断
age = 25
name = "Alice"
price = 19.99
is_active = True
names = ["Alice", "Bob", "Charlie"]
scores = {"Alice": 95, "Bob": 87}

# Python 类型注解（可选，不强制）
count: int = 100
```

### 集合操作对比

**Java 写法：**
```java
// Java：创建和操作集合
import java.util.*;

// List
List<String> fruits = new ArrayList<>(Arrays.asList("apple", "banana"));
fruits.add("cherry");
String first = fruits.get(0);
int size = fruits.size();

// Map
Map<String, Integer> ages = new HashMap<>();
ages.put("Alice", 25);
ages.put("Bob", 30);
int aliceAge = ages.get("Alice");
boolean hasAlice = ages.containsKey("Alice");

// 遍历 Map
for (Map.Entry<String, Integer> entry : ages.entrySet()) {
    System.out.println(entry.getKey() + ": " + entry.getValue());
}
```

**Python 写法：**
```python
# Python：创建和操作集合

# list
fruits = ["apple", "banana"]
fruits.append("cherry")
first = fruits[0]
size = len(fruits)

# dict
ages = {"Alice": 25, "Bob": 30}
alice_age = ages["Alice"]
has_alice = "Alice" in ages

# 遍历 dict
for name, age in ages.items():
    print(f"{name}: {age}")
```

### 字符串操作对比

**Java 写法：**
```java
// Java 字符串操作
String s = "Hello, World!";
int len = s.length();
String upper = s.toUpperCase();
String sub = s.substring(0, 5);
boolean contains = s.contains("World");
String[] parts = s.split(", ");

// 字符串拼接
String name = "Alice";
String greeting = "Hello, " + name + "!";           // 拼接
String formatted = String.format("Hello, %s!", name); // 格式化
```

**Python 写法：**
```python
# Python 字符串操作
s = "Hello, World!"
length = len(s)
upper = s.upper()
sub = s[:5]              # 切片语法
contains = "World" in s  # in 运算符
parts = s.split(", ")

# 字符串拼接
name = "Alice"
greeting = f"Hello, {name}!"     # f-string（推荐）
formatted = "Hello, {}!".format(name)  # format 方法
```

## 实战代码

### 示例 1：数据类型演示

**文件：** `examples/data_types_demo.py`

演示 Python 所有内置数据类型的创建、操作和类型检查，包括 int、float、str、bool、list、dict、tuple、set、None。

**运行方式：**
```bash
python examples/data_types_demo.py
```

**预期输出：**
```
========== 数值类型 ==========
整数: 42, 类型: <class 'int'>
大整数: 999999999999999999999, 类型: <class 'int'>
浮点数: 3.14, 类型: <class 'float'>
布尔值: True, 类型: <class 'bool'>
布尔值是 int 的子类: True

========== 字符串类型 ==========
字符串: Hello, Python!, 类型: <class 'str'>
长度: 14
大写: HELLO, PYTHON!
切片 [0:5]: Hello
f-string: 我叫 Alice，今年 25 岁

========== 列表（list） ==========
列表: [1, 'hello', 3.14, True], 类型: <class 'list'>
第一个元素: 1
追加后: [1, 'hello', 3.14, True, 'new']
列表可以混合类型（Java ArrayList<Object> 类似）

========== 字典（dict） ==========
字典: {'name': 'Alice', 'age': 25, 'city': '北京'}, 类型: <class 'dict'>
name = Alice
遍历: name -> Alice, age -> 25, city -> 北京

========== 元组（tuple） ==========
元组: (1, 2, 3, 'hello'), 类型: <class 'tuple'>
元组不可变，类似 Java 的不可变数组

========== 集合（set） ==========
集合: {1, 2, 3, 4, 5}, 类型: <class 'set'>
交集: {3, 4, 5}
并集: {1, 2, 3, 4, 5, 6, 7}

========== None 类型 ==========
None 值: None, 类型: <class 'NoneType'>
判断 None 用 is: True

========== 类型检查与转换 ==========
type(42) = <class 'int'>
isinstance(42, int) = True
isinstance(True, int) = True（bool 是 int 的子类！）
int('123') = 123
str(456) = '456'
list('abc') = ['a', 'b', 'c']
```

### 示例 2：Java 与 Python 类型系统对比

**文件：** `examples/java_comparison.py`

通过注释对比 Java 与 Python 在变量声明、类型推断、集合操作、字符串处理等方面的差异。

**运行方式：**
```bash
python examples/java_comparison.py
```

**预期输出：**
```
===== 变量声明对比 =====
Python 不需要声明类型: name = Alice, age = 25
同一变量可以改变类型: x 从 int(10) 变为 str(hello)

===== 整数精度对比 =====
Python 大整数: 100000000000000000000000000000000000000000000000000
Java 中这会溢出！Python 整数无大小限制

===== 集合操作对比 =====
Python list（类似 ArrayList）: ['apple', 'banana', 'cherry']
Python dict（类似 HashMap）: {'Alice': 95, 'Bob': 87, 'Charlie': 92}
Python set（类似 HashSet）: {1, 2, 3, 4, 5}

===== 字符串对比 =====
Python f-string: Hello, Alice! You are 25 years old.
多行字符串（Java 13+ 才支持 text blocks）:
    这是第一行
    这是第二行
    这是第三行

===== 类型检查对比 =====
Python 用 type() 和 isinstance() 检查类型
type(42) = <class 'int'>
isinstance(42, (int, float)) = True
```

## 常见陷阱

### 1. 可变默认参数（最经典的 Python 陷阱）

Java 开发者不会遇到这个问题，因为 Java 方法参数没有默认值。但在 Python 中，**可变对象（如 list、dict）作为函数默认参数时，会在所有调用之间共享**。

```python
# ✗ 错误：可变默认参数
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item("a"))  # ['a']
print(add_item("b"))  # ['a', 'b'] — 不是 ['b']！

# ✓ 正确：使用 None 作为默认值
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### 2. 浅拷贝 vs 深拷贝

Java 开发者熟悉 `clone()` 方法的浅拷贝问题，Python 中同样存在。

```python
import copy

# 浅拷贝：嵌套对象仍然共享引用
original = [[1, 2], [3, 4]]
shallow = original.copy()  # 或 list(original) 或 original[:]
shallow[0].append(99)
print(original)  # [[1, 2, 99], [3, 4]] — 原始列表也被修改了！

# 深拷贝：完全独立的副本
deep = copy.deepcopy(original)
deep[0].append(100)
print(original)  # [[1, 2, 99], [3, 4]] — 原始列表不受影响
```

### 3. `==` vs `is` 的区别

Java 开发者习惯用 `==` 比较基本类型、用 `.equals()` 比较对象。Python 中 `==` 比较值，`is` 比较身份（内存地址）。

```python
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)   # True — 值相等
print(a is b)   # False — 不是同一个对象

# 判断 None 必须用 is
x = None
print(x is None)    # ✓ 正确
print(x == None)    # ✗ 不推荐（虽然也能工作）
```

### 4. 整数缓存陷阱

Python 对小整数（-5 到 256）做了缓存优化，这可能导致 `is` 比较出现意外结果。

```python
a = 256
b = 256
print(a is b)  # True — 缓存范围内

a = 257
b = 257
print(a is b)  # False — 超出缓存范围（不同对象）
# 永远用 == 比较值，用 is 只比较 None
```

### 5. 字典键的可变性要求

Java 的 `HashMap` 允许任何对象作为键（只要实现了 `hashCode` 和 `equals`）。Python 的 `dict` 要求键必须是**不可变类型**（hashable）。

```python
# ✓ 正确：不可变类型作为键
d = {
    "name": "Alice",      # str — 不可变
    42: "answer",          # int — 不可变
    (1, 2): "tuple key",  # tuple — 不可变
}

# ✗ 错误：可变类型不能作为键
# d = {[1, 2]: "list key"}  # TypeError: unhashable type: 'list'
```

### 6. 布尔值的真假判断

Python 的真假判断比 Java 更宽泛。Java 中只有 `boolean` 类型可以用于条件判断，Python 中几乎所有类型都有"真假"概念。

```python
# 以下值在 Python 中被视为 False（"假值"）
# False, 0, 0.0, "", [], {}, set(), None

# Java 开发者注意：空集合在 Python 中是 False！
if []:
    print("不会执行")
if [1]:
    print("会执行")  # 非空列表为 True
```

> 💻 **完整可运行代码：** [data_types_demo.py](examples/data_types_demo.py) | [java_comparison.py](examples/java_comparison.py)

## 参考资料

- [Python 官方文档 - 内置类型](https://docs.python.org/zh-cn/3/library/stdtypes.html)
- [Python 官方文档 - 数据模型](https://docs.python.org/zh-cn/3/reference/datamodel.html)
- [Real Python - Basic Data Types](https://realpython.com/python-data-types/)
- [Python 类型注解指南](https://docs.python.org/zh-cn/3/library/typing.html)
