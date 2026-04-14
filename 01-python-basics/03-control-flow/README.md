# 控制流

> **模块：** 01-Python 基础
> **难度：** 入门
> **前置知识：** 数据类型与变量（02-data-types）
> **Python 版本：** >= 3.9（match-case 需要 >= 3.10）
> **最后验证日期：** 2025-07-15

## 概念说明

控制流是程序逻辑的骨架。对于 Java 开发者来说，Python 控制流最大的不同在于：**用缩进代替花括号来定义代码块**。这不仅是语法差异，更是一种"强制代码整洁"的设计哲学——缩进不对，程序直接报错。

Python 的控制流语句比 Java 更简洁、更灵活。没有传统的 `switch-case`，但 Python 3.10 引入了更强大的 `match-case`（结构化模式匹配），支持类型匹配、解构赋值等高级特性。`for` 循环天然就是 `for-in` 遍历，不需要索引变量。此外，Python 的 `for` 和 `while` 循环都支持 `else` 子句——这是 Java 中完全没有的特性，循环正常结束（没有被 `break` 中断）时执行 `else` 块。

Python 还提供了简洁的三元表达式（条件表达式）`x if condition else y`，以及 `for-in` 配合 `enumerate()`、`zip()` 等内置函数的强大遍历能力，让代码更加 Pythonic。

### Python 控制流特点一览

| 特点 | 说明 |
|------|------|
| 缩进定义代码块 | 用 4 个空格缩进代替 `{}`，缩进错误会导致 `IndentationError` |
| 没有传统 switch | Python 3.10+ 引入 `match-case`（结构化模式匹配） |
| for-in 遍历 | `for` 循环天然遍历可迭代对象，无需索引 |
| 循环 else 子句 | `for/while` 可接 `else`，循环正常结束时执行 |
| 三元表达式 | `x if condition else y`，一行搞定简单条件 |
| 海象运算符 | `:=`（Python 3.8+），在表达式中赋值 |

## Java 对比

### 条件语句对比

| 特性 | Java | Python |
|------|------|--------|
| 条件语句 | `if (condition) { }` | `if condition:` |
| 多分支 | `else if` | `elif` |
| 条件不需要括号 | 必须加 `()` | 不需要 `()` |
| 代码块 | `{ }` 花括号 | 缩进（4 空格） |
| switch/match | `switch-case`（值匹配） | `match-case`（模式匹配，3.10+） |
| 三元表达式 | `condition ? a : b` | `a if condition else b` |

**Java 写法：**
```java
// Java：if-else
int score = 85;
String grade;
if (score >= 90) {
    grade = "A";
} else if (score >= 80) {
    grade = "B";
} else if (score >= 70) {
    grade = "C";
} else {
    grade = "D";
}

// Java：switch-case
int day = 3;
switch (day) {
    case 1: System.out.println("Monday"); break;
    case 2: System.out.println("Tuesday"); break;
    case 3: System.out.println("Wednesday"); break;
    default: System.out.println("Other");
}

// Java：三元表达式
String result = (score >= 60) ? "及格" : "不及格";
```

**Python 写法：**
```python
# Python：if-elif-else
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "D"

# Python：match-case（3.10+）
day = 3
match day:
    case 1: print("Monday")
    case 2: print("Tuesday")
    case 3: print("Wednesday")
    case _: print("Other")  # _ 是通配符，类似 default

# Python：三元表达式（条件表达式）
result = "及格" if score >= 60 else "不及格"
```

### 循环语句对比

| 特性 | Java | Python |
|------|------|--------|
| 传统 for | `for (int i = 0; i < n; i++)` | 无（用 `for i in range(n)` 替代） |
| 增强 for | `for (String s : list)` | `for s in list:` |
| 带索引遍历 | 手动维护索引或用 `IntStream` | `for i, v in enumerate(list):` |
| 并行遍历 | 无内置支持 | `for a, b in zip(list1, list2):` |
| while | `while (condition) { }` | `while condition:` |
| 循环 else | 无 | `for/while ... else:` |
| do-while | `do { } while (condition);` | 无（用 `while True` + `break` 替代） |

**Java 写法：**
```java
// Java：传统 for 循环
for (int i = 0; i < 5; i++) {
    System.out.println(i);
}

// Java：增强 for 循环
List<String> fruits = Arrays.asList("apple", "banana", "cherry");
for (String fruit : fruits) {
    System.out.println(fruit);
}

// Java：遍历 Map
Map<String, Integer> scores = Map.of("Alice", 95, "Bob", 87);
for (Map.Entry<String, Integer> entry : scores.entrySet()) {
    System.out.println(entry.getKey() + ": " + entry.getValue());
}

// Java：while 循环
int count = 0;
while (count < 5) {
    System.out.println(count);
    count++;
}
```

**Python 写法：**
```python
# Python：for-in + range（替代传统 for）
for i in range(5):
    print(i)

# Python：直接遍历列表
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Python：遍历字典
scores = {"Alice": 95, "Bob": 87}
for name, score in scores.items():
    print(f"{name}: {score}")

# Python：while 循环
count = 0
while count < 5:
    print(count)
    count += 1
```

### match-case vs switch-case 对比

**Java 写法：**
```java
// Java 14+：switch 表达式
String description = switch (statusCode) {
    case 200 -> "OK";
    case 404 -> "Not Found";
    case 500 -> "Server Error";
    default -> "Unknown: " + statusCode;
};

// Java：switch 只能匹配值
```

**Python 写法：**
```python
# Python 3.10+：match-case 支持模式匹配
match status_code:
    case 200: description = "OK"
    case 404: description = "Not Found"
    case 500: description = "Server Error"
    case code: description = f"Unknown: {code}"  # 捕获变量

# match-case 还支持结构化匹配（Java switch 做不到）
match point:
    case (0, 0): print("原点")
    case (x, 0): print(f"X 轴上，x={x}")
    case (0, y): print(f"Y 轴上，y={y}")
    case (x, y): print(f"点 ({x}, {y})")
```

## 实战代码

### 示例 1：控制流综合演示

**文件：** `examples/control_flow_demo.py`

演示 Python 控制流的所有核心特性：if/elif/else 条件判断、for 循环（遍历 list/dict/range/enumerate/zip）、while 循环、match-case 模式匹配、break/continue/else、三元表达式，并在注释中与 Java 对比。

**运行方式：**
```bash
python examples/control_flow_demo.py
```

**预期输出：**
```
========== if/elif/else 条件判断 ==========
分数 85 的等级: B
18 是成年人

========== for 循环遍历 ==========
--- 遍历列表 ---
水果: apple
水果: banana
水果: cherry
--- 遍历字典 ---
Alice: 95
Bob: 87
Charlie: 92
--- range() 生成序列 ---
0 1 2 3 4
--- enumerate() 带索引遍历 ---
索引 0: apple
索引 1: banana
索引 2: cherry
--- zip() 并行遍历 ---
Alice 的成绩是 95
Bob 的成绩是 87
Charlie 的成绩是 92

========== while 循环 ==========
倒计时: 5
倒计时: 4
倒计时: 3
倒计时: 2
倒计时: 1
发射！

========== match-case 模式匹配（Python 3.10+） ==========
200 -> OK
404 -> Not Found
500 -> Server Error
302 -> Unknown status: 302
--- 结构化模式匹配 ---
(0, 0) -> 原点
(3, 0) -> X 轴上，x=3
(0, 5) -> Y 轴上，y=5
(2, 7) -> 点 (2, 7)

========== break/continue/else ==========
--- break 示例 ---
找到目标: cherry
--- continue 示例 ---
奇数: 1
奇数: 3
奇数: 5
奇数: 7
奇数: 9
--- 循环 else 示例 ---
在列表中未找到负数（循环正常结束）
在列表中找到负数: -1（循环被 break 中断，else 不执行）

========== 三元表达式（条件表达式） ==========
85 分 -> 及格
15 岁 -> 未成年
```

## 常见陷阱

### 1. 缩进错误（IndentationError）

Java 开发者习惯用花括号定义代码块，缩进只是美观。但在 Python 中，**缩进就是语法**，混用空格和 Tab 会导致难以排查的错误。

```python
# ✗ 错误：缩进不一致
if True:
    print("4 空格")
      print("6 空格")  # IndentationError!

# ✓ 正确：统一使用 4 个空格
if True:
    print("4 空格")
    print("4 空格")
```

> **建议：** 在 IDE 中设置 Tab 自动转换为 4 个空格。

### 2. 忘记冒号

Python 的 `if`、`for`、`while`、`def`、`class` 等语句末尾都需要冒号 `:`，Java 开发者容易遗漏。

```python
# ✗ 错误：缺少冒号
if score >= 60
    print("及格")  # SyntaxError!

# ✓ 正确
if score >= 60:
    print("及格")
```

### 3. `==` 和 `=` 混淆

Java 中条件语句必须用 `()`，编译器会检查。Python 没有括号保护，更容易在 `if` 中误用 `=`。

```python
# ✗ 错误：赋值而非比较
# if x = 5:  # SyntaxError（Python 不允许在 if 中直接赋值）

# ✓ 正确
if x == 5:
    print("等于 5")

# 如果确实需要在条件中赋值，使用海象运算符 :=（Python 3.8+）
if (n := len(data)) > 10:
    print(f"数据量 {n} 超过 10")
```

### 4. 循环中修改列表

Java 开发者知道在增强 for 循环中修改集合会抛出 `ConcurrentModificationException`。Python 不会报错，但结果可能出乎意料。

```python
# ✗ 危险：遍历时修改列表
numbers = [1, 2, 3, 4, 5]
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)
print(numbers)  # [1, 3, 5]？不一定！可能是 [1, 3, 5] 也可能漏删

# ✓ 正确：使用列表推导式创建新列表
numbers = [1, 2, 3, 4, 5]
numbers = [n for n in numbers if n % 2 != 0]
print(numbers)  # [1, 3, 5]
```

### 5. 误解 `for-else` 的含义

`for-else` 中的 `else` 不是"循环条件为假时执行"，而是"循环正常结束（没有被 `break` 中断）时执行"。

```python
# else 在循环正常结束时执行
for i in range(5):
    if i == 10:  # 永远不会触发 break
        break
else:
    print("循环正常结束，else 执行")  # 会执行

# else 在 break 中断时不执行
for i in range(5):
    if i == 3:
        break
else:
    print("不会执行")  # 不会执行，因为循环被 break 中断了
```

### 6. range() 不包含结束值

Java 开发者习惯 `for (int i = 0; i < 5; i++)`，Python 的 `range(5)` 同样不包含 5，但 `range(1, 5)` 容易误以为包含 5。

```python
# range(5) 生成 0, 1, 2, 3, 4（不包含 5）
# range(1, 5) 生成 1, 2, 3, 4（不包含 5）
# range(0, 10, 2) 生成 0, 2, 4, 6, 8（步长为 2）

for i in range(1, 5):
    print(i)  # 1, 2, 3, 4（不包含 5！）
```

> 💻 **完整可运行代码：** [control_flow_demo.py](examples/control_flow_demo.py)

## 参考资料

- [Python 官方文档 - 控制流](https://docs.python.org/zh-cn/3/tutorial/controlflow.html)
- [Python 官方文档 - match 语句](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#the-match-statement)
- [PEP 634 - Structural Pattern Matching](https://peps.python.org/pep-0634/)
- [Real Python - Conditional Statements](https://realpython.com/python-conditional-statements/)
- [Real Python - Python for Loop](https://realpython.com/python-for-loop/)
