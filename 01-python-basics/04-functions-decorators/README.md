# 函数与装饰器

> **模块：** 01-Python 基础
> **难度：** 入门
> **前置知识：** 控制流（03-control-flow）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

函数是 Python 中的**一等公民（First-Class Citizen）**。这意味着函数可以赋值给变量、作为参数传递给其他函数、作为返回值返回，甚至可以存储在数据结构中。这与 Java 中方法必须依附于类的设计截然不同——在 Python 中，函数本身就是对象。

**闭包（Closure）** 是理解装饰器的关键。当一个内部函数引用了外部函数的变量，并且外部函数已经返回时，内部函数仍然可以访问这些变量——这就是闭包。闭包让函数"记住"了它被创建时的环境。

**装饰器（Decorator）** 本质上是一个高阶函数：它接收一个函数作为参数，返回一个新函数。装饰器利用闭包的特性，在不修改原函数代码的前提下，为函数添加额外功能（如日志、计时、权限检查等）。`@decorator` 语法糖让这一切变得优雅简洁。

### 核心概念一览

| 概念 | 说明 |
|------|------|
| 一等公民 | 函数可以赋值、传参、返回，和普通变量一样使用 |
| `*args` / `**kwargs` | 可变位置参数 / 可变关键字参数，实现灵活的函数签名 |
| lambda | 匿名函数，适合简单的一行表达式 |
| 闭包 | 内部函数引用外部函数变量，函数"记住"创建时的环境 |
| 装饰器 | 高阶函数，接收函数并返回增强后的新函数 |
| `functools.wraps` | 保留被装饰函数的元信息（名称、文档字符串等） |

## Java 对比

### 函数 vs 方法

| 特性 | Java | Python |
|------|------|--------|
| 函数定义 | 方法必须定义在类中 | 函数可以独立存在，不依赖类 |
| 一等公民 | 方法不是一等公民（Java 8+ 有方法引用） | 函数是一等公民，可赋值、传参、返回 |
| 默认参数 | 不支持（需要方法重载） | 原生支持默认参数值 |
| 可变参数 | `Type... args`（仅一个） | `*args`（位置）+ `**kwargs`（关键字） |
| 返回多值 | 不支持（需要封装对象或数组） | 原生支持（返回 tuple） |
| Lambda | `(params) -> expression`（Java 8+） | `lambda params: expression` |
| 高阶函数 | 需要函数式接口（`Function<T,R>`） | 直接传递函数对象 |
| 装饰器 | 无（注解 `@Annotation` 是元数据，不改变行为） | `@decorator` 直接修改函数行为 |

### 函数定义对比

**Java 写法：**
```java
// Java：方法必须在类中定义
public class MathUtils {
    // 方法重载实现"默认参数"
    public static int add(int a, int b) {
        return a + b;
    }
    public static int add(int a, int b, int c) {
        return a + b + c;
    }

    // 可变参数（只能有一个，且必须在最后）
    public static int sum(int... numbers) {
        int total = 0;
        for (int n : numbers) total += n;
        return total;
    }
}
```

**Python 写法：**
```python
# Python：函数可以独立定义，不需要类
def add(a, b, c=0):  # c 有默认值，不需要重载
    return a + b + c

# 可变参数：*args 接收任意位置参数，**kwargs 接收任意关键字参数
def flexible(*args, **kwargs):
    print(f"位置参数: {args}")
    print(f"关键字参数: {kwargs}")

# 返回多个值（Java 需要封装对象）
def get_name_and_age():
    return "Alice", 25  # 返回 tuple

name, age = get_name_and_age()  # 解构赋值
```

### Lambda 对比

**Java 写法：**
```java
// Java 8+：Lambda 需要函数式接口
import java.util.*;
import java.util.function.*;
import java.util.stream.*;

// 需要声明函数式接口类型
Function<Integer, Integer> square = x -> x * x;
BiFunction<Integer, Integer, Integer> add = (a, b) -> a + b;

// 排序
List<String> names = Arrays.asList("Charlie", "Alice", "Bob");
names.sort((a, b) -> a.compareTo(b));
// 或使用方法引用
names.sort(Comparator.naturalOrder());

// Stream API
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
List<Integer> evens = numbers.stream()
    .filter(n -> n % 2 == 0)
    .collect(Collectors.toList());
```

**Python 写法：**
```python
# Python：lambda 更简洁，不需要函数式接口
square = lambda x: x * x
add = lambda a, b: a + b

# 排序
names = ["Charlie", "Alice", "Bob"]
names.sort(key=lambda name: name)  # 或直接 names.sort()

# 高阶函数（不需要 Stream API）
numbers = [1, 2, 3, 4, 5]
evens = list(filter(lambda n: n % 2 == 0, numbers))
# 更 Pythonic 的写法：列表推导式
evens = [n for n in numbers if n % 2 == 0]
```

### 装饰器 vs 注解

**Java 写法：**
```java
// Java 注解：只是元数据标记，不会改变方法行为
// 需要配合反射或框架（如 Spring AOP）才能实现类似装饰器的效果
@Override
public String toString() { return "..."; }

@Deprecated
public void oldMethod() { }

// Spring AOP 实现类似装饰器的功能（需要框架支持）
@Transactional
public void transferMoney() { }

@Cacheable("users")
public User getUser(Long id) { }
```

**Python 写法：**
```python
# Python 装饰器：直接修改函数行为，不需要框架
import functools, time

def timer(func):
    """计时装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} 耗时: {time.time() - start:.4f}s")
        return result
    return wrapper

@timer  # 等价于 slow_function = timer(slow_function)
def slow_function():
    time.sleep(1)
    return "done"
```

## 实战代码

### 示例 1：函数定义与高阶函数

**文件：** `examples/functions_demo.py`

演示 Python 函数的核心特性：函数定义、默认参数、`*args`/`**kwargs`、返回多值、lambda 表达式、高阶函数（map/filter/sorted），并在注释中与 Java 对比。

**运行方式：**
```bash
python examples/functions_demo.py
```

**预期输出：**
```
========== 函数定义与默认参数 ==========
greet('Alice') = Hello, Alice!
greet('Bob', 'Hi') = Hi, Bob!
add(1, 2) = 3
add(1, 2, 3) = 6

========== *args 和 **kwargs ==========
--- *args（可变位置参数）---
sum_all(1, 2, 3) = 6
sum_all(1, 2, 3, 4, 5) = 15
--- **kwargs（可变关键字参数）---
build_profile:
  name: Alice
  age: 25
  city: 北京
  job: engineer
--- 混合使用 ---
mixed(1, 2, 3, x=10, y=20):
  a = 1
  args = (2, 3)
  kwargs = {'x': 10, 'y': 20}

========== 返回多值 ==========
商: 3, 余数: 1
最小值: 1, 最大值: 99, 平均值: 42.0

========== Lambda 表达式 ==========
square(5) = 25
add(3, 4) = 7
条件 lambda: is_even(4) = True, is_even(3) = False

========== 高阶函数 ==========
--- map ---
平方: [1, 4, 9, 16, 25]
--- filter ---
偶数: [2, 4]
--- sorted ---
按名字排序: ['Alice', 'Bob', 'Charlie']
按年龄排序: [('Bob', 20), ('Alice', 25), ('Charlie', 30)]
--- 函数作为参数 ---
apply(5, square) = 25
apply(5, double) = 10

========== 函数是一等公民 ==========
函数赋值给变量: f(3) = 9
函数存储在字典中: ops['add'](10, 3) = 13
函数列表批量执行: [3, 4, 4]
```

### 示例 2：装饰器原理与实战

**文件：** `examples/decorators_demo.py`

演示装饰器的完整知识体系：从闭包到装饰器的演进、`@` 语法糖、带参数的装饰器、`functools.wraps`、常用内置装饰器（`@property`、`@staticmethod`、`@classmethod`）、实用装饰器示例（计时器、日志、重试）。

**运行方式：**
```bash
python examples/decorators_demo.py
```

**预期输出：**
```
========== 闭包基础 ==========
counter() = 1
counter() = 2
counter() = 3
闭包让函数"记住"了外部变量 count

========== 从闭包到装饰器 ==========
--- 手动装饰 ---
调用: say_hello()
Hello!
--- @语法糖（等价写法）---
调用: say_goodbye()
Goodbye!

========== functools.wraps 保留元信息 ==========
没有 @wraps: 函数名=wrapper, 文档=None
有 @wraps: 函数名=my_function, 文档=这是原始函数的文档

========== 带参数的装饰器 ==========
[INFO] 用户登录: login()
[DEBUG] 数据查询: query_data()

========== 实用装饰器：计时器 ==========
模拟耗时操作...
process_data 耗时: 0.50s

========== 实用装饰器：重试 ==========
尝试第 1 次...
操作失败: 模拟失败 (第1次)，1s 后重试...
尝试第 2 次...
操作失败: 模拟失败 (第2次)，1s 后重试...
尝试第 3 次...
第3次成功！

========== 内置装饰器：@property ==========
面积: 78.54
半径: 10, 面积: 314.16

========== 内置装饰器：@staticmethod 和 @classmethod ==========
静态方法 — 是否有效: True
类方法 — 创建实例: MathUtils(precision=4)
实例方法 — pi ≈ 3.1416

========== 装饰器叠加 ==========
调用: add(3, 5)
add 耗时: 0.0000s
结果: 8
```

## 常见陷阱

### 1. 可变默认参数（最经典的 Python 陷阱）

Java 没有默认参数，所以 Java 开发者第一次遇到这个问题会很困惑。Python 的默认参数在函数定义时只计算一次，如果默认值是可变对象（list、dict），所有调用会共享同一个对象。

```python
# ✗ 错误：可变默认参数
def append_to(item, target=[]):
    target.append(item)
    return target

print(append_to(1))  # [1]
print(append_to(2))  # [1, 2] — 不是 [2]！共享了同一个 list

# ✓ 正确：使用 None 作为默认值
def append_to(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target
```

### 2. lambda 只能写一行表达式

Java 的 Lambda 可以用 `{}` 包含多条语句，Python 的 lambda 只能包含一个表达式，不能有赋值、循环等语句。

```python
# ✗ 错误：lambda 不能包含语句
# f = lambda x: if x > 0: return x  # SyntaxError

# ✓ 正确：复杂逻辑用 def 定义
f = lambda x: x if x > 0 else -x  # 三元表达式可以

def complex_logic(x):  # 复杂逻辑用普通函数
    if x > 0:
        return x * 2
    return x * -1
```

### 3. 装饰器不用 `functools.wraps` 导致元信息丢失

不使用 `@functools.wraps` 时，被装饰函数的 `__name__`、`__doc__` 等属性会被替换为 wrapper 函数的属性，影响调试和文档生成。

```python
import functools

# ✗ 不推荐：丢失原函数信息
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# ✓ 推荐：保留原函数信息
def good_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### 4. 闭包中的变量绑定是延迟的

闭包捕获的是变量的引用，而非值。在循环中创建闭包时，所有闭包共享同一个循环变量。

```python
# ✗ 错误：所有函数都引用同一个 i
functions = []
for i in range(3):
    functions.append(lambda: i)
print([f() for f in functions])  # [2, 2, 2] — 不是 [0, 1, 2]！

# ✓ 正确：用默认参数捕获当前值
functions = []
for i in range(3):
    functions.append(lambda i=i: i)  # 默认参数在定义时求值
print([f() for f in functions])  # [0, 1, 2]
```

### 5. 混淆 `@decorator` 和 `@decorator()`

带参数的装饰器需要额外一层嵌套。忘记加括号或多加括号都会导致错误。

```python
# 不带参数的装饰器：直接 @decorator
@my_decorator
def func(): pass

# 带参数的装饰器：@decorator(args)，注意有括号
@my_decorator(level="INFO")
def func(): pass

# ✗ 错误：不带参数的装饰器加了括号
# @my_decorator()  # TypeError（除非装饰器专门处理了这种情况）
```

> 💻 **完整可运行代码：** [functions_demo.py](examples/functions_demo.py) | [decorators_demo.py](examples/decorators_demo.py)

## 参考资料

- [Python 官方文档 - 函数定义](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#defining-functions)
- [Python 官方文档 - 装饰器](https://docs.python.org/zh-cn/3/glossary.html#term-decorator)
- [Python 官方文档 - functools](https://docs.python.org/zh-cn/3/library/functools.html)
- [Real Python - Primer on Python Decorators](https://realpython.com/primer-on-python-decorators/)
- [Real Python - Python Lambda Functions](https://realpython.com/python-lambda/)
