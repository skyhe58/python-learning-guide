# 类与面向对象

> **模块：** 01-Python 基础
> **难度：** 进阶
> **前置知识：** 函数与装饰器（04-functions-decorators）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

Python 是一门**一切皆对象**的语言。数字、字符串、函数、类本身——都是对象。这与 Java 中基本类型（int、boolean 等）不是对象的设计不同。Python 的 OOP 更加灵活和动态，核心理念是**鸭子类型（Duck Typing）**：不关心对象的类型，只关心对象是否具有所需的方法和属性——"如果它走起来像鸭子、叫起来像鸭子，那它就是鸭子"。

Python 支持**多继承**，通过 **MRO（Method Resolution Order，方法解析顺序）** 使用 C3 线性化算法来解决菱形继承问题。Java 只支持单继承（类），通过接口实现多态。Python 没有 `interface` 关键字，但提供了 `abc.ABC`（抽象基类）来实现类似的约束。

Python 的 OOP 还有一个显著特点：**没有真正的访问控制**。Java 有 `private`、`protected`、`public` 关键字来严格控制访问权限，Python 则依靠**命名约定**——单下划线 `_name` 表示"内部使用"，双下划线 `__name` 触发名称改写（Name Mangling）。Python 信奉"我们都是成年人"的哲学，靠约定而非强制。

### 核心概念一览

| 概念 | 说明 |
|------|------|
| `class` | 定义类，Python 3 中所有类默认继承 `object` |
| `__init__` | 构造方法（初始化方法），类似 Java 构造函数 |
| `self` | 实例方法的第一个参数，指向实例本身（类似 Java `this`，但必须显式声明） |
| 继承 | 支持单继承和多继承，使用 `class Child(Parent)` 语法 |
| `super()` | 调用父类方法，在多继承中遵循 MRO 顺序 |
| 鸭子类型 | 不检查类型，只检查行为（方法/属性是否存在） |
| 魔术方法 | `__str__`、`__repr__`、`__eq__` 等，定制对象行为 |
| `@dataclass` | Python 3.7+ 自动生成 `__init__`、`__repr__`、`__eq__` 等 |
| `ABC` | 抽象基类，强制子类实现指定方法 |
| `@property` | 将方法伪装为属性访问，替代 Java 的 getter/setter |

## Java 对比

### 类定义与构造函数

| 特性 | Java | Python |
|------|------|--------|
| 类定义 | `public class Dog { }` | `class Dog:` |
| 构造函数 | `public Dog(String name) { }` | `def __init__(self, name):` |
| `this` / `self` | `this` 隐式可用 | `self` 必须显式声明为第一个参数 |
| 实例变量声明 | 需要在类体中声明字段类型 | 在 `__init__` 中直接赋值 `self.name = name` |
| 多构造函数 | 构造函数重载 | 默认参数 / `@classmethod` 工厂方法 |

**Java 写法：**
```java
public class Dog {
    private String name;
    private int age;

    // 构造函数
    public Dog(String name, int age) {
        this.name = name;  // this 隐式可用
        this.age = age;
    }

    // 构造函数重载
    public Dog(String name) {
        this(name, 0);
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    @Override
    public String toString() {
        return "Dog{name='" + name + "', age=" + age + "}";
    }
}
```

**Python 写法：**
```python
class Dog:
    def __init__(self, name, age=0):  # 默认参数代替重载
        self.name = name   # self 必须显式声明
        self.age = age

    @classmethod
    def from_dict(cls, data):  # 工厂方法代替多构造函数
        return cls(data["name"], data.get("age", 0))

    def __str__(self):  # 等价于 Java toString()
        return f"Dog(name='{self.name}', age={self.age})"
```

### 继承与多态

| 特性 | Java | Python |
|------|------|--------|
| 单继承 | `class Dog extends Animal` | `class Dog(Animal):` |
| 多继承 | 不支持（只能实现多个接口） | 原生支持 `class C(A, B):` |
| 接口 | `interface Flyable { }` | 无 interface 关键字，用 ABC 或鸭子类型 |
| 抽象类 | `abstract class Shape { }` | `class Shape(ABC):` + `@abstractmethod` |
| 方法重写 | `@Override` 注解（可选） | 直接重新定义同名方法 |
| 调用父类 | `super.method()` | `super().method()` |
| 多态实现 | 通过接口/继承 + 方法重写 | 鸭子类型（不需要继承关系） |

**Java 写法：**
```java
// Java：接口 + 抽象类实现多态
public interface Drawable {
    void draw();
}

public abstract class Shape implements Drawable {
    public abstract double area();
}

public class Circle extends Shape {
    private double radius;
    public Circle(double radius) { this.radius = radius; }

    @Override
    public double area() { return Math.PI * radius * radius; }

    @Override
    public void draw() { System.out.println("Drawing circle"); }
}
```

**Python 写法：**
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def draw(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def draw(self):
        print("Drawing circle")

# 鸭子类型：不需要继承 Shape 也能当 Shape 用
class FakeShape:
    def area(self):
        return 42
    def draw(self):
        print("Drawing fake shape")
```

### 访问控制与属性

| 特性 | Java | Python |
|------|------|--------|
| `private` | `private int age;` | `self.__age`（名称改写，非真正私有） |
| `protected` | `protected int age;` | `self._age`（约定，无强制） |
| `public` | `public int age;` | `self.age`（默认公开） |
| getter/setter | `getAge()` / `setAge()` | `@property` / `@name.setter` |
| 常量 | `static final int MAX = 100;` | `MAX = 100`（约定全大写，无强制） |

### 魔术方法 vs Java 方法

| Python 魔术方法 | Java 对应 | 用途 |
|----------------|-----------|------|
| `__str__` | `toString()` | 用户友好的字符串表示 |
| `__repr__` | 无直接对应 | 开发者调试用的字符串表示 |
| `__eq__` | `equals()` | 相等性比较 |
| `__hash__` | `hashCode()` | 哈希值（用于 set/dict） |
| `__lt__` / `__gt__` | `compareTo()` | 大小比较（支持排序） |
| `__len__` | `size()` / `length()` | 获取长度 |
| `__getitem__` | `get(index)` | 下标访问 `obj[key]` |
| `__iter__` | `iterator()` | 支持 for 循环迭代 |
| `__add__` | 无（需要自定义方法） | 运算符重载 `+` |

### dataclass vs Java Record/Lombok

| 特性 | Java Record (16+) | Java + Lombok | Python @dataclass |
|------|-------------------|---------------|-------------------|
| 语法 | `record Point(int x, int y) {}` | `@Data class Point { }` | `@dataclass class Point:` |
| 自动生成 | 构造函数、equals、hashCode、toString | 全部 | `__init__`、`__repr__`、`__eq__` |
| 可变性 | 不可变 | 可变 | 默认可变，`frozen=True` 不可变 |
| 继承 | 不能继承 | 可以继承 | 可以继承 |
| 默认值 | 不支持 | 支持 | 支持 |

## 实战代码

### 示例：OOP 完整演示

**文件：** `examples/oop_demo.py`

演示 Python OOP 的完整知识体系：类定义与 `__init__`、`self` 参数、继承与 `super()`、多继承与 MRO、鸭子类型、魔术方法（`__str__`、`__repr__`、`__eq__`、`__lt__`、`__len__`、`__getitem__`）、`@dataclass`、访问控制命名约定、ABC 抽象基类，并在注释中与 Java 对比。

**运行方式：**
```bash
python examples/oop_demo.py
```

**预期输出：**
```
========== 类定义与 __init__ ==========
Dog(name='旺财', age=3, breed='中华田园犬')
旺财说: 汪汪！
旺财 今年 3 岁
工厂方法创建: Dog(name='小白', age=1, breed='萨摩耶')

========== self 参数 ==========
实例方法 — self 是: <__main__...Counter object at 0x...>
计数: 1
计数: 2
计数: 3

========== 继承与 super() ==========
--- 单继承 ---
父类 Person 初始化: 张三
子类 Employee 初始化: 工程师
Employee(name='张三', age=30, company='Python公司', position='工程师')
张三 在 Python公司 担任 工程师
--- super() 调用链 ---
（上面的输出已展示：先调用父类 Person 初始化，再调用子类 Employee 初始化）

========== 多继承与 MRO ==========
--- 多继承 ---
FlyingFish 的 MRO:
  → FlyingFish → Flyer → Swimmer → Animal → object
飞鱼在飞翔！
飞鱼在游泳！
飞鱼在吃东西

========== 鸭子类型 ==========
--- 不需要继承关系，只要有 area() 方法就行 ---
Circle 的面积: 78.54
Rectangle 的面积: 24
FakeShape 的面积: 42

========== 魔术方法 ==========
--- __str__ 和 __repr__ ---
str:  《Python编程》 ¥89.00
repr: Book('Python编程', '张三', 89.0)
--- __eq__ ---
book1 == book2: True
book1 == book3: False
--- __lt__（支持排序）---
排序结果: [《Java入门》 ¥59.00, 《Go语言》 ¥79.00, 《Python编程》 ¥89.00]
--- __len__ 和 __getitem__ ---
书架上有 3 本书
第一本: 《Python编程》 ¥89.00
最后一本: 《Go语言》 ¥79.00
遍历书架:
  - 《Python编程》 ¥89.00
  - 《Java入门》 ¥59.00
  - 《Go语言》 ¥79.00

========== dataclass ==========
--- 基本用法 ---
Point(x=3, y=4)
Point(x=0, y=0.0)
p1 == p2: False
p1 == Point(3, 4): True
--- frozen（不可变）---
Color(r=255, g=128, b=0)
不可变 dataclass 不能修改: cannot assign to field 'r'
--- field 和 __post_init__ ---
Student(name='李四', age=20, grades=[90, 85, 95], gpa=90.0)

========== 访问控制 ==========
公开属性: Python 银行
_protected 属性（约定内部使用）: 1000.0
__private 属性（名称改写）: 通过 _BankAccount__secret_key 访问 = SECRET123
@property: 余额 = ¥1000.00
存款后余额: ¥1500.00
取款后余额: ¥1200.00

========== ABC 抽象基类 ==========
--- 抽象基类强制子类实现方法 ---
不能实例化抽象类: Can't instantiate abstract class...
MySQL 连接已建立
MySQL 执行: SELECT * FROM users
MySQL 连接已关闭
--- isinstance 检查 ---
mysql 是 Database 的实例: True
```

## 常见陷阱

### 1. 忘记 `self` 参数

Java 的 `this` 是隐式的，Python 的 `self` 必须显式声明为实例方法的第一个参数。

```python
# ✗ 错误：忘记 self
class Dog:
    def bark():  # TypeError: bark() takes 0 positional arguments but 1 was given
        print("汪！")

# ✓ 正确：显式声明 self
class Dog:
    def bark(self):
        print("汪！")
```

### 2. 类变量 vs 实例变量混淆

Java 中 `static` 字段属于类，实例字段属于对象，界限清晰。Python 中类变量和实例变量的区别更微妙，尤其是可变类型。

```python
# ✗ 危险：可变类型作为类变量，所有实例共享同一个列表
class Student:
    grades = []  # 类变量！所有实例共享

s1 = Student()
s2 = Student()
s1.grades.append(90)
print(s2.grades)  # [90] — s2 也被影响了！

# ✓ 正确：在 __init__ 中创建实例变量
class Student:
    def __init__(self):
        self.grades = []  # 实例变量，每个实例独立
```

### 3. 多继承中 `super()` 的调用顺序

Java 只有单继承，`super` 总是指向唯一的父类。Python 多继承中 `super()` 遵循 MRO 顺序，可能不是你直觉中的"父类"。

```python
class A:
    def method(self):
        print("A")

class B(A):
    def method(self):
        print("B")
        super().method()  # 不一定调用 A！取决于 MRO

class C(A):
    def method(self):
        print("C")
        super().method()

class D(B, C):
    def method(self):
        print("D")
        super().method()

D().method()  # D → B → C → A（MRO 顺序）
```

### 4. `__eq__` 和 `__hash__` 必须配套

Java 中重写 `equals()` 必须同时重写 `hashCode()`，Python 也一样。定义了 `__eq__` 后，Python 会自动将 `__hash__` 设为 `None`，导致对象不能放入 `set` 或作为 `dict` 的 key。

```python
# ✗ 问题：定义了 __eq__ 但没定义 __hash__
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

p = Point(1, 2)
# {p}  # TypeError: unhashable type: 'Point'

# ✓ 正确：同时定义 __hash__
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __hash__(self):
        return hash((self.x, self.y))
```

### 5. 误以为双下划线 `__name` 是真正的 private

Java 的 `private` 是编译器强制的访问控制，Python 的 `__name` 只是名称改写（Name Mangling），仍然可以通过 `_ClassName__name` 访问。

```python
class Secret:
    def __init__(self):
        self.__password = "123456"

s = Secret()
# s.__password  # AttributeError
print(s._Secret__password)  # "123456" — 仍然可以访问！
```

> 💻 **完整可运行代码：** [oop_demo.py](examples/oop_demo.py)

## 参考资料

- [Python 官方文档 - 类](https://docs.python.org/zh-cn/3/tutorial/classes.html)
- [Python 官方文档 - 数据模型（魔术方法）](https://docs.python.org/zh-cn/3/reference/datamodel.html)
- [Python 官方文档 - dataclasses](https://docs.python.org/zh-cn/3/library/dataclasses.html)
- [Python 官方文档 - abc 模块](https://docs.python.org/zh-cn/3/library/abc.html)
- [Real Python - Object-Oriented Programming in Python](https://realpython.com/python3-object-oriented-programming/)
- [Real Python - Python Data Classes](https://realpython.com/python-data-classes/)
