# Python 与 Java 核心差异速查表

> **用途：** 面试高频对比话题速查
> **适用人群：** 有 Java 背景的 Python 学习者
> **最后更新：** 2025-07-15

---

## 1. 语法基础

| 特性 | Java | Python |
|------|------|--------|
| 语句结尾 | 分号 `;` 必须 | 无分号，换行即结束 |
| 代码块 | 花括号 `{}` | 缩进（4 空格） |
| 注释 | `//` 单行，`/* */` 多行 | `#` 单行，`"""` 多行 |
| 变量声明 | `int x = 10;`（需声明类型） | `x = 10`（动态类型） |
| 常量 | `final int X = 10;` | `X = 10`（约定大写，无强制） |
| 空值 | `null` | `None` |
| 布尔值 | `true` / `false` | `True` / `False`（首字母大写） |
| 入口函数 | `public static void main(String[] args)` | `if __name__ == "__main__":` |
| 类型转换 | `(int) 3.14` 强制转换 | `int(3.14)` 函数调用 |
| 三元运算符 | `x > 0 ? "正" : "非正"` | `"正" if x > 0 else "非正"` |
| 字符串格式化 | `String.format("%s is %d", name, age)` | `f"{name} is {age}"` |

### 代码对比

```java
// Java
public class Hello {
    public static void main(String[] args) {
        String name = "World";
        int count = 3;
        for (int i = 0; i < count; i++) {
            System.out.println("Hello, " + name + "!");
        }
    }
}
```

```python
# Python
def main():
    name = "World"
    count = 3
    for i in range(count):
        print(f"Hello, {name}!")

if __name__ == "__main__":
    main()
```

---

## 2. 数据类型

| 特性 | Java | Python |
|------|------|--------|
| 整数 | `int`（32位）/ `long`（64位） | `int`（无限精度） |
| 浮点数 | `float`（32位）/ `double`（64位） | `float`（64位，等同 Java double） |
| 字符串 | `String`（不可变） | `str`（不可变） |
| 字符 | `char`（单字符类型） | 无，单字符就是长度为 1 的 `str` |
| 数组 | `int[]` / `String[]` | `list`（动态类型，可混合） |
| 列表 | `ArrayList<T>` | `list` |
| 字典/映射 | `HashMap<K, V>` | `dict` |
| 集合 | `HashSet<T>` | `set` |
| 元组 | 无原生支持 | `tuple`（不可变序列） |
| 枚举 | `enum` 关键字 | `enum.Enum` 类 |
| 可选值 | `Optional<T>` | 直接用 `None` + 类型提示 `Optional[T]` |

### 类型系统对比

```java
// Java：静态类型，编译时检查
int x = 10;
String s = "hello";
List<Integer> nums = new ArrayList<>();
// x = "hello";  // 编译错误！
```

```python
# Python：动态类型，运行时检查
x = 10
s = "hello"
nums = [1, 2, 3]
x = "hello"  # 完全合法！

# Python 3.5+ 类型提示（可选，不强制）
x: int = 10
s: str = "hello"
nums: list[int] = [1, 2, 3]
```

---

## 3. 面向对象

| 特性 | Java | Python |
|------|------|--------|
| 类定义 | `class Foo { }` | `class Foo:` |
| 构造函数 | `public Foo(args)` | `def __init__(self, args):` |
| this/self | `this`（隐式） | `self`（显式，必须写） |
| 继承 | `extends`（单继承） | `class Sub(Base):`（支持多继承） |
| 接口 | `interface` + `implements` | 无接口，用抽象类 `ABC` 或鸭子类型 |
| 抽象类 | `abstract class` | `from abc import ABC, abstractmethod` |
| 访问控制 | `public/private/protected` | 约定 `_private`、`__mangled`（无强制） |
| 静态方法 | `static` 关键字 | `@staticmethod` 装饰器 |
| 类方法 | 无直接等价 | `@classmethod` 装饰器 |
| getter/setter | 手写或 Lombok | `@property` 装饰器 |
| 数据类 | `record`（Java 16+） | `@dataclass`（Python 3.7+） |
| 运算符重载 | 不支持（除 `+` 字符串拼接） | 魔术方法 `__add__`, `__eq__` 等 |
| 多态 | 接口 + 继承 | 鸭子类型（duck typing） |

### 类定义对比

```java
// Java
public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() { return name; }
    public int getAge() { return age; }

    @Override
    public String toString() {
        return "Person{name=" + name + ", age=" + age + "}";
    }
}
```

```python
# Python（使用 dataclass 最简洁）
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int

    def __str__(self):
        return f"Person(name={self.name}, age={self.age})"
```

---

## 4. 异常处理

| 特性 | Java | Python |
|------|------|--------|
| 语法 | `try/catch/finally` | `try/except/finally` |
| 额外子句 | 无 | `else`（无异常时执行） |
| 受检异常 | 有（必须声明或捕获） | 无（所有异常都是非受检的） |
| 异常基类 | `Throwable` → `Exception` / `Error` | `BaseException` → `Exception` |
| 自定义异常 | `extends Exception` | `class MyError(Exception): pass` |
| 资源管理 | `try-with-resources` | `with` 语句 |
| 多异常捕获 | `catch (A \| B e)` | `except (A, B) as e:` |
| 异常链 | `throw new B(a)` | `raise B() from a` |

### 异常处理对比

```java
// Java
try {
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("除零错误: " + e.getMessage());
} finally {
    System.out.println("清理");
}
```

```python
# Python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"除零错误: {e}")
else:
    print("没有异常时执行")  # Java 没有这个
finally:
    print("清理")
```

---

## 5. 集合操作

| 操作 | Java | Python |
|------|------|--------|
| 创建列表 | `List.of(1, 2, 3)` | `[1, 2, 3]` |
| 创建字典 | `Map.of("a", 1)` | `{"a": 1}` |
| 创建集合 | `Set.of(1, 2, 3)` | `{1, 2, 3}` |
| 列表追加 | `list.add(item)` | `list.append(item)` |
| 列表长度 | `list.size()` | `len(list)` |
| 字典取值 | `map.get(key)` | `dict[key]` 或 `dict.get(key)` |
| 遍历 | `for (var item : list)` | `for item in list:` |
| 带索引遍历 | 手动计数或 IntStream | `for i, item in enumerate(list):` |
| 排序 | `Collections.sort(list)` | `list.sort()` 或 `sorted(list)` |
| 过滤 | `stream.filter(x -> x > 0)` | `[x for x in list if x > 0]` |
| 映射 | `stream.map(x -> x * 2)` | `[x * 2 for x in list]` |
| 切片 | `list.subList(1, 3)` | `list[1:3]` |
| 解包 | 无 | `a, b, c = [1, 2, 3]` |
| 字典合并 | `map1.putAll(map2)` | `{**d1, **d2}` 或 `d1 \| d2`（3.9+） |

### 集合操作对比

```java
// Java Stream API
List<Integer> nums = List.of(1, 2, 3, 4, 5);
List<Integer> result = nums.stream()
    .filter(x -> x % 2 == 0)
    .map(x -> x * x)
    .collect(Collectors.toList());
// [4, 16]
```

```python
# Python 列表推导式
nums = [1, 2, 3, 4, 5]
result = [x * x for x in nums if x % 2 == 0]
# [4, 16]
```

---

## 6. 并发编程

| 特性 | Java | Python |
|------|------|--------|
| 线程 | `Thread` / `Runnable` | `threading.Thread` |
| 线程池 | `ExecutorService` | `concurrent.futures.ThreadPoolExecutor` |
| 进程池 | `ProcessBuilder` | `concurrent.futures.ProcessPoolExecutor` |
| 异步 | `CompletableFuture` | `asyncio` / `async/await` |
| 锁 | `synchronized` / `ReentrantLock` | `threading.Lock` |
| GIL | 无（真正并行） | 有（CPython 限制多线程并行） |
| 原子操作 | `AtomicInteger` 等 | `queue.Queue`（线程安全） |
| 协程 | 虚拟线程（Java 21+） | `async def` / `await` |

### 并发模型选择

```
Python 并发选择指南:
├── CPU 密集型 → multiprocessing（绕过 GIL）
├── IO 密集型
│   ├── 少量并发 → threading
│   └── 大量并发 → asyncio
└── 混合型 → concurrent.futures
```

```
Java 并发选择指南:
├── 传统多线程 → ExecutorService
├── 异步编程 → CompletableFuture
├── 响应式 → Project Reactor / RxJava
└── 轻量级 → 虚拟线程（Java 21+）
```

---

## 7. 包管理与项目结构

| 特性 | Java | Python |
|------|------|--------|
| 包管理器 | Maven / Gradle | pip / poetry / conda |
| 依赖文件 | `pom.xml` / `build.gradle` | `requirements.txt` / `pyproject.toml` |
| 包仓库 | Maven Central | PyPI |
| 虚拟环境 | 不需要（依赖隔离在项目内） | `venv` / `conda`（强烈推荐） |
| 包导入 | `import java.util.List;` | `from collections import OrderedDict` |
| 包结构 | 目录 + `package` 声明 | 目录 + `__init__.py` |
| 构建工具 | Maven / Gradle | setuptools / poetry / hatch |
| 发布 | `mvn deploy` | `twine upload` / `poetry publish` |

### 项目结构对比

```
# Java (Maven)                    # Python
my-project/                       my-project/
├── pom.xml                       ├── pyproject.toml
├── src/                          ├── src/
│   ├── main/                     │   └── my_package/
│   │   └── java/                 │       ├── __init__.py
│   │       └── com/example/      │       ├── main.py
│   │           └── App.java      │       └── utils.py
│   └── test/                     ├── tests/
│       └── java/                 │   ├── __init__.py
│           └── com/example/      │   └── test_main.py
│               └── AppTest.java  ├── requirements.txt
└── target/                       └── README.md
```

---

## 8. 函数与 Lambda

| 特性 | Java | Python |
|------|------|--------|
| 函数定义 | 必须在类中（方法） | `def func():` 独立函数 |
| Lambda | `(x) -> x * 2`（可多行） | `lambda x: x * 2`（仅单表达式） |
| 函数式接口 | `Function<T, R>` | 函数就是一等公民 |
| 默认参数 | 不支持（用重载） | `def f(x, y=10):` |
| 可变参数 | `String... args` | `*args, **kwargs` |
| 返回多值 | 不支持（用对象/数组） | `return a, b, c`（返回 tuple） |
| 装饰器 | 无（用注解 + AOP） | `@decorator` |
| 闭包 | Lambda 引用 effectively final 变量 | `nonlocal` 可修改外层变量 |

---

## 9. 文件与 IO

| 特性 | Java | Python |
|------|------|--------|
| 文件读取 | `Files.readString(path)` | `Path("f").read_text()` |
| 文件写入 | `Files.writeString(path, content)` | `Path("f").write_text(content)` |
| 逐行读取 | `BufferedReader.readLine()` | `for line in open("f"):` |
| 路径操作 | `java.nio.file.Path` | `pathlib.Path` |
| 目录遍历 | `Files.walk()` | `Path.iterdir()` / `os.walk()` |
| 资源管理 | `try-with-resources` | `with open() as f:` |
| 序列化 | `Serializable` / Jackson | `pickle` / `json` |
| 临时文件 | `Files.createTempFile()` | `tempfile.NamedTemporaryFile()` |

---

## 10. 测试

| 特性 | Java | Python |
|------|------|--------|
| 测试框架 | JUnit 5 | pytest |
| 断言 | `assertEquals(expected, actual)` | `assert actual == expected` |
| 测试注解/标记 | `@Test` | 函数名以 `test_` 开头 |
| 参数化测试 | `@ParameterizedTest` | `@pytest.mark.parametrize` |
| Mock | Mockito | `unittest.mock` / `pytest-mock` |
| 测试夹具 | `@BeforeEach` / `@AfterEach` | `@pytest.fixture` |
| 覆盖率 | JaCoCo | `pytest-cov` |
| 运行测试 | `mvn test` / `gradle test` | `pytest` |

### 测试代码对比

```java
// Java (JUnit 5)
@Test
void testAdd() {
    assertEquals(3, Calculator.add(1, 2));
}

@ParameterizedTest
@CsvSource({"1, 2, 3", "0, 0, 0", "-1, 1, 0"})
void testAddParameterized(int a, int b, int expected) {
    assertEquals(expected, Calculator.add(a, b));
}
```

```python
# Python (pytest)
def test_add():
    assert add(1, 2) == 3

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
```

---

## 11. 常见面试对比话题

### 为什么 Python 比 Java 慢？

| 因素 | Java | Python |
|------|------|--------|
| 执行方式 | JIT 编译（字节码 → 机器码） | 解释执行（CPython） |
| 类型检查 | 编译时静态检查 | 运行时动态检查 |
| 内存管理 | JVM 优化的 GC | 引用计数 + 分代 GC |
| GIL | 无 | 有（限制多线程并行） |

### 什么时候选 Python？什么时候选 Java？

| 场景 | 推荐 | 原因 |
|------|------|------|
| 快速原型 / 脚本 | Python | 语法简洁，开发速度快 |
| 数据分析 / AI | Python | 生态完善（NumPy, PyTorch） |
| 大型企业应用 | Java | 类型安全，性能好，生态成熟 |
| 微服务 | 都可以 | Java: Spring Boot; Python: FastAPI |
| 运维自动化 | Python | 标准库丰富，脚本能力强 |
| Android 开发 | Java/Kotlin | 原生支持 |
| 高并发服务 | Java | 真正的多线程并行 |

---

## 12. 速记口诀

```
Python vs Java 速记:

语法: 分号花括号 → 缩进换行
类型: 静态声明 → 动态推断
OOP:  单继承接口 → 多继承鸭子
异常: 受检非受检 → 全部非受检
并发: 真并行 → GIL 限制
包管: Maven/Gradle → pip/poetry
测试: JUnit → pytest
入口: main 方法 → __name__ 守卫
```
