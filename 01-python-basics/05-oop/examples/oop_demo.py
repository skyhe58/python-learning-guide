#!/usr/bin/env python3
"""
Python 类与面向对象编程完整演示

模块: 01-Python 基础
知识点: 类与面向对象
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python oop_demo.py

描述:
    演示 Python OOP 的完整知识体系：
    1. 类定义与 __init__（vs Java 构造函数）
    2. self 参数（vs Java this）
    3. 继承与 super()（vs Java extends/super）
    4. 多继承与 MRO（Java 不支持多继承）
    5. 鸭子类型（vs Java 接口）
    6. 魔术方法（vs Java toString/equals/compareTo）
    7. dataclass（vs Java record/Lombok）
    8. 访问控制（_private 约定 vs Java private/protected/public）
    9. ABC 抽象基类（vs Java abstract class/interface）
    每个部分都在注释中与 Java 进行对比。
"""

import math
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from functools import total_ordering


# ============================================================
# 1. 类定义与 __init__
# ============================================================

def demo_class_definition():
    """类定义与 __init__"""
    print("=" * 10, "类定义与 __init__", "=" * 10)

    # Java:
    #   public class Dog {
    #       private String name;
    #       private int age;
    #       private String breed;
    #       public Dog(String name, int age, String breed) {
    #           this.name = name;
    #           this.age = age;
    #           this.breed = breed;
    #       }
    #       // 构造函数重载
    #       public Dog(String name) { this(name, 0, "未知"); }
    #   }
    #
    # Python: 不需要声明字段类型，用默认参数代替构造函数重载

    class Dog:
        # 类变量（类似 Java static 字段）
        species = "犬科"

        def __init__(self, name, age=0, breed="未知"):
            """构造方法 — 类似 Java 构造函数，但用 self 代替 this"""
            self.name = name      # 实例变量，直接赋值即可
            self.age = age
            self.breed = breed

        @classmethod
        def from_dict(cls, data):
            """工厂方法 — Java 中通常用静态工厂方法或构造函数重载"""
            return cls(data["name"], data.get("age", 0), data.get("breed", "未知"))

        def bark(self):
            """实例方法"""
            return f"{self.name}说: 汪汪！"

        def __str__(self):
            return f"Dog(name='{self.name}', age={self.age}, breed='{self.breed}')"

    dog = Dog("旺财", 3, "中华田园犬")
    print(dog)
    print(dog.bark())
    print(f"{dog.name} 今年 {dog.age} 岁")

    # 工厂方法创建
    dog2 = Dog.from_dict({"name": "小白", "age": 1, "breed": "萨摩耶"})
    print(f"工厂方法创建: {dog2}")
    print()


# ============================================================
# 2. self 参数
# ============================================================

def demo_self():
    """self 参数演示"""
    print("=" * 10, "self 参数", "=" * 10)

    # Java: this 是隐式的，不需要声明
    #   public void increment() { this.count++; }
    #
    # Python: self 必须显式声明为第一个参数
    #   self 只是约定名称，理论上可以用任何名字（但强烈建议用 self）

    class Counter:
        def __init__(self):
            self.count = 0

        def increment(self):
            """self 指向调用该方法的实例"""
            self.count += 1
            return self.count

    c = Counter()
    print(f"实例方法 — self 是: {c}")
    print(f"计数: {c.increment()}")
    print(f"计数: {c.increment()}")
    print(f"计数: {c.increment()}")
    print()


# ============================================================
# 3. 继承与 super()
# ============================================================

def demo_inheritance():
    """继承与 super()"""
    print("=" * 10, "继承与 super()", "=" * 10)

    # Java:
    #   public class Person {
    #       protected String name;
    #       protected int age;
    #       public Person(String name, int age) { ... }
    #   }
    #   public class Employee extends Person {
    #       private String company;
    #       public Employee(String name, int age, String company) {
    #           super(name, age);  // 调用父类构造函数
    #           this.company = company;
    #       }
    #   }

    class Person:
        def __init__(self, name, age):
            print(f"父类 Person 初始化: {name}")
            self.name = name
            self.age = age

        def introduce(self):
            return f"{self.name}, {self.age}岁"

        def __str__(self):
            return f"Person(name='{self.name}', age={self.age})"

    class Employee(Person):
        def __init__(self, name, age, company, position):
            super().__init__(name, age)  # 调用父类 __init__
            print(f"子类 Employee 初始化: {position}")
            self.company = company
            self.position = position

        def introduce(self):
            """方法重写 — Java 中用 @Override 注解"""
            return f"{self.name} 在 {self.company} 担任 {self.position}"

        def __str__(self):
            return (f"Employee(name='{self.name}', age={self.age}, "
                    f"company='{self.company}', position='{self.position}')")

    print("--- 单继承 ---")
    emp = Employee("张三", 30, "Python公司", "工程师")
    print(emp)
    print(emp.introduce())
    print("--- super() 调用链 ---")
    print("（上面的输出已展示：先调用父类 Person 初始化，再调用子类 Employee 初始化）")
    print()


# ============================================================
# 4. 多继承与 MRO
# ============================================================

def demo_multiple_inheritance():
    """多继承与 MRO（方法解析顺序）"""
    print("=" * 10, "多继承与 MRO", "=" * 10)

    # Java: 不支持多继承（类），只能实现多个接口
    #   public class FlyingFish implements Flyable, Swimmable { }
    #
    # Python: 原生支持多继承，通过 MRO（C3 线性化）解决菱形继承

    class Animal:
        def eat(self):
            return "在吃东西"

    class Flyer(Animal):
        def move(self):
            return "在飞翔！"

    class Swimmer(Animal):
        def move(self):
            return "在游泳！"

    # 多继承：同时继承 Flyer 和 Swimmer
    class FlyingFish(Flyer, Swimmer):
        def fly(self):
            # 调用 Flyer 的 move
            return f"飞鱼{Flyer.move(self)}"

        def swim(self):
            # 调用 Swimmer 的 move
            return f"飞鱼{Swimmer.move(self)}"

    print("--- 多继承 ---")
    ff = FlyingFish()

    # MRO：方法解析顺序
    print("FlyingFish 的 MRO:")
    for cls in FlyingFish.__mro__:
        print(f"  → {cls.__name__}", end="")
    print()

    print(ff.fly())
    print(ff.swim())
    print(f"飞鱼{ff.eat()}")
    print()


# ============================================================
# 5. 鸭子类型
# ============================================================

def demo_duck_typing():
    """鸭子类型"""
    print("=" * 10, "鸭子类型", "=" * 10)

    # Java: 多态需要通过接口或继承关系
    #   public interface HasArea { double area(); }
    #   public void printArea(HasArea shape) { ... }
    #
    # Python: 鸭子类型 — 不关心类型，只关心是否有 area() 方法
    #   "如果它走起来像鸭子、叫起来像鸭子，那它就是鸭子"

    class Circle:
        def __init__(self, radius):
            self.radius = radius

        def area(self):
            return round(math.pi * self.radius ** 2, 2)

    class Rectangle:
        def __init__(self, width, height):
            self.width = width
            self.height = height

        def area(self):
            return self.width * self.height

    # 这个类没有继承任何基类，但它有 area() 方法
    class FakeShape:
        def area(self):
            return 42

    def print_area(shape):
        """不检查类型，只要有 area() 方法就行"""
        print(f"{type(shape).__name__} 的面积: {shape.area()}")

    print("--- 不需要继承关系，只要有 area() 方法就行 ---")
    print_area(Circle(5))
    print_area(Rectangle(4, 6))
    print_area(FakeShape())  # 没有继承关系也能用！
    print()


# ============================================================
# 6. 魔术方法
# ============================================================

def demo_magic_methods():
    """魔术方法（特殊方法 / dunder methods）"""
    print("=" * 10, "魔术方法", "=" * 10)

    # Java 对应关系：
    #   __str__    → toString()
    #   __repr__   → 无直接对应（调试用）
    #   __eq__     → equals()
    #   __hash__   → hashCode()
    #   __lt__     → compareTo() < 0
    #   __len__    → size() / length()
    #   __getitem__ → get(index)

    @total_ordering  # 只需定义 __eq__ 和 __lt__，自动生成其他比较方法
    class Book:
        def __init__(self, title, author, price):
            self.title = title
            self.author = author
            self.price = price

        def __str__(self):
            """用户友好的字符串 — 类似 Java toString()"""
            return f"《{self.title}》 ¥{self.price:.2f}"

        def __repr__(self):
            """开发者调试用 — Java 没有直接对应"""
            return f"Book('{self.title}', '{self.author}', {self.price})"

        def __eq__(self, other):
            """相等比较 — 类似 Java equals()"""
            if not isinstance(other, Book):
                return NotImplemented
            return self.title == other.title and self.author == other.author

        def __lt__(self, other):
            """小于比较 — 类似 Java compareTo() < 0"""
            if not isinstance(other, Book):
                return NotImplemented
            return self.price < other.price

        def __hash__(self):
            """哈希值 — 类似 Java hashCode()，定义了 __eq__ 就必须定义"""
            return hash((self.title, self.author))

    # __str__ 和 __repr__
    print("--- __str__ 和 __repr__ ---")
    book1 = Book("Python编程", "张三", 89.0)
    print(f"str:  {book1}")          # 调用 __str__
    print(f"repr: {book1!r}")        # 调用 __repr__

    # __eq__
    print("--- __eq__ ---")
    book2 = Book("Python编程", "张三", 99.0)  # 同书不同价
    book3 = Book("Java入门", "李四", 59.0)
    print(f"book1 == book2: {book1 == book2}")  # True（按 title+author 比较）
    print(f"book1 == book3: {book1 == book3}")  # False

    # __lt__（支持排序）
    print("--- __lt__（支持排序）---")
    books = [book1, book3, Book("Go语言", "王五", 79.0)]
    sorted_books = sorted(books)  # 按价格排序（__lt__ 定义了排序规则）
    print(f"排序结果: [{', '.join(str(b) for b in sorted_books)}]")

    # __len__ 和 __getitem__
    print("--- __len__ 和 __getitem__ ---")

    class BookShelf:
        """书架 — 演示 __len__ 和 __getitem__"""
        def __init__(self):
            self._books = []

        def add(self, book):
            self._books.append(book)

        def __len__(self):
            """len(shelf) — 类似 Java size()"""
            return len(self._books)

        def __getitem__(self, index):
            """shelf[0] — 类似 Java get(index)"""
            return self._books[index]

        def __iter__(self):
            """支持 for book in shelf — 类似 Java iterator()"""
            return iter(self._books)

    shelf = BookShelf()
    shelf.add(book1)
    shelf.add(book3)
    shelf.add(Book("Go语言", "王五", 79.0))

    print(f"书架上有 {len(shelf)} 本书")
    print(f"第一本: {shelf[0]}")
    print(f"最后一本: {shelf[-1]}")
    print("遍历书架:")
    for book in shelf:
        print(f"  - {book}")
    print()


# ============================================================
# 7. dataclass（Python 3.7+）
# ============================================================

def demo_dataclass():
    """dataclass 装饰器"""
    print("=" * 10, "dataclass", "=" * 10)

    # Java Record (16+):
    #   public record Point(int x, int y) { }
    #   // 自动生成构造函数、equals、hashCode、toString
    #
    # Java + Lombok:
    #   @Data public class Point { private int x; private int y; }
    #
    # Python @dataclass: 自动生成 __init__、__repr__、__eq__

    # --- 基本用法 ---
    print("--- 基本用法 ---")

    @dataclass
    class Point:
        x: float
        y: float = 0.0  # 默认值

    p1 = Point(3, 4)
    p2 = Point(0)       # y 使用默认值 0.0
    print(p1)            # 自动生成 __repr__
    print(p2)
    print(f"p1 == p2: {p1 == p2}")              # 自动生成 __eq__
    print(f"p1 == Point(3, 4): {p1 == Point(3, 4)}")  # True

    # --- frozen：不可变 dataclass（类似 Java Record）---
    print("--- frozen（不可变）---")

    @dataclass(frozen=True)
    class Color:
        r: int
        g: int
        b: int

    color = Color(255, 128, 0)
    print(color)
    try:
        color.r = 0  # 不可变，会抛出异常
    except AttributeError as e:
        print(f"不可变 dataclass 不能修改: {e}")

    # --- field 和 __post_init__ ---
    print("--- field 和 __post_init__ ---")

    @dataclass
    class Student:
        name: str
        age: int
        grades: list = field(default_factory=list)  # 可变默认值用 field
        gpa: float = field(init=False)  # 不在 __init__ 中，由 __post_init__ 计算

        def __post_init__(self):
            """__init__ 之后自动调用，用于计算派生字段"""
            self.gpa = sum(self.grades) / len(self.grades) if self.grades else 0.0

    student = Student("李四", 20, [90, 85, 95])
    print(student)
    print()


# ============================================================
# 8. 访问控制
# ============================================================

def demo_access_control():
    """访问控制（命名约定 vs Java 访问修饰符）"""
    print("=" * 10, "访问控制", "=" * 10)

    # Java:
    #   public String name;       // 公开
    #   protected double balance; // 受保护
    #   private String secretKey; // 私有
    #
    # Python: 没有真正的访问控制，靠命名约定
    #   self.name          → 公开（类似 Java public）
    #   self._balance      → 约定内部使用（类似 Java protected）
    #   self.__secret_key  → 名称改写（类似 Java private，但不是真正私有）

    class BankAccount:
        def __init__(self, bank_name, balance, secret_key):
            self.bank_name = bank_name          # 公开
            self._balance = balance              # 约定：内部使用
            self.__secret_key = secret_key       # 名称改写：_BankAccount__secret_key

        @property
        def balance(self):
            """@property — 替代 Java 的 getter"""
            return self._balance

        def deposit(self, amount):
            """存款"""
            if amount > 0:
                self._balance += amount
            return self._balance

        def withdraw(self, amount):
            """取款"""
            if 0 < amount <= self._balance:
                self._balance -= amount
            return self._balance

    account = BankAccount("Python 银行", 1000.0, "SECRET123")

    # 公开属性：直接访问
    print(f"公开属性: {account.bank_name}")

    # _protected：可以访问，但约定不应该从外部访问
    print(f"_protected 属性（约定内部使用）: {account._balance}")

    # __private：名称改写，不能直接用 account.__secret_key 访问
    # 但可以通过 _ClassName__attr 访问（Python 没有真正的 private）
    print(f"__private 属性（名称改写）: "
          f"通过 _BankAccount__secret_key 访问 = {account._BankAccount__secret_key}")

    # @property：像属性一样访问方法
    print(f"@property: 余额 = ¥{account.balance:.2f}")
    account.deposit(500)
    print(f"存款后余额: ¥{account.balance:.2f}")
    account.withdraw(300)
    print(f"取款后余额: ¥{account.balance:.2f}")
    print()


# ============================================================
# 9. ABC 抽象基类
# ============================================================

def demo_abc():
    """ABC 抽象基类"""
    print("=" * 10, "ABC 抽象基类", "=" * 10)

    # Java:
    #   public abstract class Database {
    #       public abstract void connect();
    #       public abstract ResultSet execute(String sql);
    #       public abstract void close();
    #   }
    #   // 或者用接口
    #   public interface Database {
    #       void connect();
    #       ResultSet execute(String sql);
    #       void close();
    #   }
    #
    # Python: 使用 abc.ABC + @abstractmethod
    #   没有 interface 关键字，ABC 同时扮演抽象类和接口的角色

    class Database(ABC):
        """抽象基类 — 类似 Java abstract class 或 interface"""

        @abstractmethod
        def connect(self):
            """子类必须实现"""
            pass

        @abstractmethod
        def execute(self, sql):
            """子类必须实现"""
            pass

        @abstractmethod
        def close(self):
            """子类必须实现"""
            pass

        def ping(self):
            """非抽象方法 — 子类可以直接使用（接口中的 default 方法）"""
            return "pong"

    class MySQLDatabase(Database):
        """具体实现类"""

        def connect(self):
            print("MySQL 连接已建立")

        def execute(self, sql):
            print(f"MySQL 执行: {sql}")
            return []

        def close(self):
            print("MySQL 连接已关闭")

    print("--- 抽象基类强制子类实现方法 ---")

    # 不能实例化抽象类
    try:
        db = Database()
    except TypeError as e:
        print(f"不能实例化抽象类: {str(e)[:40]}")

    # 具体子类可以实例化
    mysql = MySQLDatabase()
    mysql.connect()
    mysql.execute("SELECT * FROM users")
    mysql.close()

    # isinstance 检查
    print("--- isinstance 检查 ---")
    print(f"mysql 是 Database 的实例: {isinstance(mysql, Database)}")
    print()


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数：依次演示所有 OOP 特性"""
    demo_class_definition()
    demo_self()
    demo_inheritance()
    demo_multiple_inheritance()
    demo_duck_typing()
    demo_magic_methods()
    demo_dataclass()
    demo_access_control()
    demo_abc()


if __name__ == "__main__":
    main()
