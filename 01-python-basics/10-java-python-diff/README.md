# Python 与 Java 核心差异总结

> **模块：** 01-Python 基础
> **难度：** 入门
> **前置知识：** 无（总结性文档）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

本文档系统性地总结 Python 与 Java 在语言设计、运行机制、生态工具等方面的核心差异。作为 Java 开发者转向 Python 的"速查地图"，帮助你快速建立两种语言之间的对应关系，避免因思维惯性踩坑。

每个对比维度都以表格形式呈现，辅以关键代码片段说明。建议在学习各知识点时回来查阅对应章节，加深理解。

---

## 1. 语言哲学与设计理念

| 维度 | Java | Python |
|------|------|--------|
| 设计哲学 | "Write Once, Run Anywhere"（一次编写，到处运行） | "There should be one obvious way to do it"（应该有一种显而易见的方式） |
| 类型系统 | 静态类型，编译时检查 | 动态类型，运行时检查 |
| 编程范式 | 面向对象为主（一切皆类） | 多范式（OOP + 函数式 + 过程式） |
| 代码风格 | 显式、冗长、严格 | 简洁、灵活、"Pythonic" |
| 错误处理哲学 | LBYL（Look Before You Leap，先检查再执行） | EAFP（Easier to Ask Forgiveness than Permission，先执行再处理异常） |
| 访问控制 | 编译器强制（`private`/`protected`/`public`） | 命名约定（`_`/`__`，"我们都是成年人"） |
| 代码规范 | Java Code Conventions / Google Java Style | PEP 8 |

```python
# EAFP 风格（Python 推荐）
try:
    value = my_dict[key]
except KeyError:
    value = default_value

# LBYL 风格（Java 习惯）
if key in my_dict:
    value = my_dict[key]
else:
    value = default_value

# 更 Pythonic 的写法
value = my_dict.get(key, default_value)
```

---

## 2. 类型系统

| 特性 | Java | Python |
|------|------|--------|
| 类型检查时机 | 编译时（静态类型） | 运行时（动态类型） |
| 变量声明 | 必须声明类型：`int x = 10;` | 无需声明：`x = 10` |
| 类型推断 | `var x = 10;`（Java 10+，局部变量） | 天然支持，变量无类型 |
| 基本类型 | `int`, `double`, `boolean` 等（非对象） | **一切皆对象**，`int`, `float`, `bool` 都是对象 |
| 自动装箱 | `int` ↔ `Integer` 自动转换 | 不需要，`int` 本身就是对象 |
| 泛型 | `List<String>`（类型擦除） | 无泛型，但有 Type Hints：`list[str]` |
| 类型注解 | 强制（编译器检查） | 可选（仅文档和工具用，运行时不检查） |
| 空值 | `null`（可能 NPE） | `None`（是一个真实的单例对象） |
| 类型转换 | 强制转换 `(int) x` | 构造函数 `int(x)` |

```java
// Java：静态类型，编译时检查
String name = "张三";
int age = 25;
List<String> skills = new ArrayList<>();
// name = 123;  // 编译错误！
```

```python
# Python：动态类型，运行时检查
name = "张三"
age = 25
skills = []
name = 123  # 完全合法！变量只是标签

# Type Hints（可选，不影响运行）
name: str = "张三"
age: int = 25
skills: list[str] = []
```

---

## 3. 内存管理与垃圾回收

| 特性 | Java | Python |
|------|------|--------|
| 内存管理 | JVM 自动管理（堆/栈分离） | CPython 解释器自动管理 |
| GC 算法 | 分代收集（Young/Old/Perm）、G1、ZGC 等 | **引用计数** + 分代收集（处理循环引用） |
| GC 触发 | 自动或 `System.gc()`（建议） | 引用计数归零立即回收；分代 GC 定期运行 |
| 内存泄漏风险 | 对象引用未释放、集合持有引用 | 循环引用（GC 可处理）、C 扩展中的引用 |
| 对象创建 | `new Object()`（堆上分配） | 直接调用 `Object()`（无 `new` 关键字） |
| 值传递/引用传递 | 值传递（对象传递引用的副本） | "传对象引用"（类似 Java 的对象传递方式） |
| 不可变对象 | `String`、包装类不可变 | `str`、`tuple`、`frozenset`、`int` 不可变 |
| 弱引用 | `WeakReference<T>` | `weakref` 模块 |

```python
# Python 引用计数演示
import sys

a = [1, 2, 3]
print(sys.getrefcount(a))  # 2（a 本身 + getrefcount 参数）

b = a          # 引用计数 +1
print(sys.getrefcount(a))  # 3

del b          # 引用计数 -1
print(sys.getrefcount(a))  # 2
```

---

## 4. 并发模型

| 特性 | Java | Python |
|------|------|--------|
| 线程 | `Thread` / `ExecutorService` | `threading.Thread` / `ThreadPoolExecutor` |
| **GIL** | 无（真正的多线程并行） | **有 GIL**（全局解释器锁，同一时刻只有一个线程执行 Python 字节码） |
| CPU 密集型并行 | 多线程即可 | 必须用 `multiprocessing`（多进程）绕过 GIL |
| IO 密集型并发 | 多线程 / NIO / Reactor | 多线程（GIL 在 IO 时释放）/ `asyncio` |
| 异步编程 | `CompletableFuture` / Reactor / Virtual Threads (21+) | `asyncio` + `async/await` |
| 线程池 | `Executors.newFixedThreadPool(n)` | `concurrent.futures.ThreadPoolExecutor(n)` |
| 进程池 | `ProcessBuilder` | `concurrent.futures.ProcessPoolExecutor(n)` |
| 锁 | `synchronized` / `ReentrantLock` | `threading.Lock` / `threading.RLock` |
| 原子操作 | `AtomicInteger` 等 | GIL 保证部分操作原子性（但不应依赖） |
| 协程 | Virtual Threads（Java 21+） | `asyncio` 协程（`async def` / `await`） |

```java
// Java：真正的多线程并行
ExecutorService executor = Executors.newFixedThreadPool(4);
for (int i = 0; i < 10; i++) {
    executor.submit(() -> cpuIntensiveTask());  // 4 个线程真正并行
}
```

```python
# Python：CPU 密集型必须用多进程
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(cpu_intensive_task) for _ in range(10)]
    # 4 个进程真正并行（绕过 GIL）

# IO 密集型可以用 asyncio
import asyncio

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        return await asyncio.gather(*tasks)
```

### GIL 影响总结

| 场景 | Java | Python |
|------|------|--------|
| CPU 密集型 | 多线程 ✅ | 多线程 ❌（GIL 限制）→ 用多进程 |
| IO 密集型 | 多线程 ✅ | 多线程 ✅（GIL 在 IO 时释放）/ asyncio ✅ |
| 网络并发 | NIO / Netty | asyncio / gevent |

---

## 5. 包管理与依赖管理

| 特性 | Java (Maven/Gradle) | Python (pip/poetry) |
|------|---------------------|---------------------|
| 包管理器 | Maven / Gradle | pip / poetry / pipenv |
| 中央仓库 | Maven Central | PyPI (pypi.org) |
| 依赖文件 | `pom.xml` / `build.gradle` | `requirements.txt` / `pyproject.toml` |
| 版本锁定 | `pom.xml` 中指定版本 | `requirements.txt` 精确版本 / `poetry.lock` |
| 依赖隔离 | 项目级（每个项目独立的依赖树） | **虚拟环境**（`venv` / `conda`） |
| 依赖冲突 | Maven 自动解析（最近优先） | pip 不自动解析（可能冲突） |
| 构建工具 | Maven / Gradle（编译+打包+测试） | setuptools / poetry / flit（打包） |
| 打包格式 | `.jar` / `.war` / `.ear` | `.whl`（wheel）/ `.tar.gz` |
| 发布 | `mvn deploy` | `twine upload` / `poetry publish` |
| 脚本运行 | `java -jar app.jar` | `python app.py` |

```bash
# Java 项目初始化
mvn archetype:generate -DgroupId=com.example -DartifactId=myapp
# 依赖在 pom.xml 中声明，mvn install 自动下载

# Python 项目初始化
python -m venv .venv          # 创建虚拟环境
source .venv/bin/activate     # 激活虚拟环境
pip install -r requirements.txt  # 安装依赖
```

---

## 6. 项目结构

### Java 典型项目结构（Maven）

```
my-java-project/
├── pom.xml
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/
│   │   │       ├── App.java
│   │   │       ├── controller/
│   │   │       ├── service/
│   │   │       └── model/
│   │   └── resources/
│   │       └── application.properties
│   └── test/
│       └── java/
│           └── com/example/
│               └── AppTest.java
└── target/                    # 编译输出
```

### Python 典型项目结构

```
my-python-project/
├── pyproject.toml             # 或 setup.py + requirements.txt
├── README.md
├── src/                       # 或直接在根目录放包
│   └── mypackage/
│       ├── __init__.py
│       ├── app.py
│       ├── controllers/
│       ├── services/
│       └── models/
├── tests/
│   ├── __init__.py
│   ├── test_app.py
│   └── conftest.py            # pytest 配置
├── .venv/                     # 虚拟环境（不提交到 Git）
└── .env                       # 环境变量
```

### 关键差异

| 维度 | Java | Python |
|------|------|--------|
| 包声明 | `package com.example;`（文件头声明） | 目录 + `__init__.py`（文件系统即包） |
| 一个文件一个类 | 强制（public class 与文件名一致） | 一个文件可包含多个类、函数 |
| 入口点 | `public static void main(String[] args)` | `if __name__ == "__main__":` |
| 编译 | 必须编译为 `.class` | 解释执行，无需编译 |
| 测试位置 | `src/test/` 镜像 `src/main/` | `tests/` 目录或与源码同目录 |
| 配置文件 | `application.properties` / `.yml` | `.env` / `config.py` / `.toml` |

---

## 7. 错误处理

| 特性 | Java | Python |
|------|------|--------|
| 异常基类 | `Throwable` → `Exception` / `Error` | `BaseException` → `Exception` |
| 受检异常 | 有（`IOException` 等，必须处理或声明） | **无**（所有异常都是非受检的） |
| 捕获语法 | `try/catch/finally` | `try/except/else/finally` |
| `else` 子句 | 无 | 有（`try` 无异常时执行） |
| 异常声明 | `throws IOException`（方法签名） | 无需声明（文档约定） |
| 资源管理 | `try-with-resources`（`AutoCloseable`） | `with` 语句（`__enter__`/`__exit__`） |
| 异常链 | `new Exception("msg", cause)` | `raise Exception("msg") from cause` |
| 空指针 | `NullPointerException` | `AttributeError` / `TypeError` |

---

## 8. 编码风格

| 维度 | Java (Google Style / Oracle) | Python (PEP 8) |
|------|------------------------------|-----------------|
| 缩进 | 4 空格（或 2 空格） | **4 空格**（强制，缩进即语法） |
| 大括号 | `{ }` 包裹代码块 | **无大括号**，用缩进表示代码块 |
| 分号 | 必须 `;` 结尾 | **无分号**（可选但不推荐） |
| 命名 - 类 | `PascalCase`：`MyClass` | `PascalCase`：`MyClass` |
| 命名 - 方法/函数 | `camelCase`：`getUserName()` | `snake_case`：`get_user_name()` |
| 命名 - 变量 | `camelCase`：`userName` | `snake_case`：`user_name` |
| 命名 - 常量 | `UPPER_SNAKE_CASE`：`MAX_SIZE` | `UPPER_SNAKE_CASE`：`MAX_SIZE` |
| 命名 - 包 | `lowercase`：`com.example` | `lowercase`：`mypackage` |
| 私有成员 | `private` 关键字 | `_` 前缀（约定）/ `__` 前缀（名称改写） |
| 行长度 | 100-120 字符 | 79 字符（PEP 8）/ 实际常用 120 |
| 文档注释 | `/** Javadoc */` | `"""docstring"""` |
| 导入排序 | 标准库 → 第三方 → 项目内 | 标准库 → 第三方 → 项目内（isort 工具） |
| 格式化工具 | google-java-format / Spotless | black / autopep8 / ruff |
| 静态检查 | SpotBugs / PMD / Checkstyle | flake8 / pylint / mypy / ruff |

```java
// Java 风格
public class UserService {
    private static final int MAX_RETRY = 3;

    public String getUserName(int userId) {
        // camelCase 方法名和变量名
        String userName = findById(userId);
        return userName;
    }
}
```

```python
# Python 风格 (PEP 8)
class UserService:
    MAX_RETRY = 3  # 常量用 UPPER_SNAKE_CASE

    def get_user_name(self, user_id: int) -> str:
        # snake_case 方法名和变量名
        user_name = self._find_by_id(user_id)
        return user_name

    def _find_by_id(self, user_id: int) -> str:
        """内部方法用 _ 前缀标记"""
        ...
```

---

## 9. 数据结构对比

| 数据结构 | Java | Python |
|----------|------|--------|
| 动态数组 | `ArrayList<T>` | `list` |
| 链表 | `LinkedList<T>` | `collections.deque`（双端队列） |
| 哈希表 | `HashMap<K, V>` | `dict` |
| 有序哈希表 | `LinkedHashMap<K, V>` | `dict`（Python 3.7+ 保持插入顺序） |
| 树形映射 | `TreeMap<K, V>` | `sortedcontainers.SortedDict`（第三方） |
| 集合 | `HashSet<T>` | `set` |
| 有序集合 | `TreeSet<T>` | `sortedcontainers.SortedSet`（第三方） |
| 不可变列表 | `List.of(1, 2, 3)` | `tuple`：`(1, 2, 3)` |
| 不可变集合 | `Set.of(1, 2, 3)` | `frozenset({1, 2, 3})` |
| 队列 | `Queue<T>` / `Deque<T>` | `collections.deque` / `queue.Queue` |
| 优先队列 | `PriorityQueue<T>` | `heapq` 模块 |
| 栈 | `Stack<T>`（或用 `Deque`） | `list`（`append`/`pop`） |
| 枚举 | `enum Color { RED, GREEN }` | `enum.Enum` |
| 记录/数据类 | `record Point(int x, int y)` | `@dataclass` / `NamedTuple` |

---

## 10. 常用框架对比

| 领域 | Java | Python |
|------|------|--------|
| Web 全栈 | Spring Boot | Django |
| Web API | Spring WebFlux / Javalin | FastAPI / Flask |
| ORM | Hibernate / MyBatis | SQLAlchemy / Django ORM |
| 任务队列 | Spring Async + RabbitMQ | Celery |
| 定时任务 | Quartz / Spring @Scheduled | APScheduler / Celery Beat |
| 消息队列 | Spring AMQP / Kafka Client | pika / kafka-python |
| 微服务 | Spring Cloud / gRPC | FastAPI + gRPC / Nameko |
| 测试 | JUnit / Mockito / TestNG | pytest / unittest / mock |
| 日志 | SLF4J + Logback / Log4j2 | logging（标准库） |
| HTTP 客户端 | OkHttp / RestTemplate / WebClient | requests / httpx / aiohttp |
| CLI 工具 | picocli / JCommander | argparse / click / typer |
| 数据处理 | Apache Spark (Java API) | pandas / numpy |
| 机器学习 | DL4J / Weka | scikit-learn / PyTorch / TensorFlow |

---

## 11. 运行与部署

| 特性 | Java | Python |
|------|------|--------|
| 运行环境 | JVM（JRE/JDK） | CPython 解释器 |
| 编译 | `.java` → `.class`（字节码） | 无需编译（解释执行，可选 `.pyc` 缓存） |
| 运行命令 | `java -jar app.jar` | `python app.py` |
| 打包部署 | `.jar` / `.war` + 应用服务器 | Docker / 直接部署 / WSGI/ASGI 服务器 |
| 性能 | JIT 编译，接近原生性能 | 解释执行，较慢（可用 Cython/PyPy 加速） |
| 启动速度 | 较慢（JVM 启动开销） | 较快（解释器轻量） |
| 内存占用 | 较高（JVM 基础开销） | 较低 |
| 跨平台 | JVM 跨平台 | 解释器跨平台 |
| 版本管理 | SDKMAN / jenv | pyenv / conda |

---

## 12. 快速对照速查表

### 语法速查

| 功能 | Java | Python |
|------|------|--------|
| 打印 | `System.out.println("hi")` | `print("hi")` |
| 字符串格式化 | `String.format("Hi %s", name)` | `f"Hi {name}"` |
| 三元运算 | `x > 0 ? "正" : "负"` | `"正" if x > 0 else "负"` |
| 空值检查 | `if (obj != null)` | `if obj is not None` |
| 类型检查 | `obj instanceof String` | `isinstance(obj, str)` |
| 遍历带索引 | `for (int i = 0; i < list.size(); i++)` | `for i, item in enumerate(list)` |
| 遍历字典 | `for (Map.Entry<K,V> e : map.entrySet())` | `for k, v in dict.items()` |
| 列表切片 | `list.subList(1, 3)` | `list[1:3]` |
| 多返回值 | 返回对象或数组 | `return a, b`（元组解包） |
| 交换变量 | `int t = a; a = b; b = t;` | `a, b = b, a` |
| 列表排序 | `Collections.sort(list)` | `list.sort()` 或 `sorted(list)` |
| 字符串连接 | `String.join(", ", list)` | `", ".join(list)` |
| 文件读取 | `Files.readString(Path.of("f"))` | `Path("f").read_text()` |
| Lambda | `(x) -> x * 2` | `lambda x: x * 2` |
| 主函数 | `public static void main(String[] args)` | `if __name__ == "__main__":` |

---

## 总结：Java 开发者转 Python 的关键心态转变

1. **从"类型安全"到"鸭子类型"** — 不再依赖编译器检查类型，而是信任对象的行为
2. **从"显式声明"到"约定优于配置"** — 不再需要 `private`/`public`，用 `_` 前缀约定
3. **从"一切皆类"到"函数也是一等公民"** — 函数可以赋值、传参、返回
4. **从"冗长但清晰"到"简洁即美"** — 拥抱推导式、解包、f-string 等 Pythonic 写法
5. **从"编译时发现错误"到"测试驱动"** — 没有编译器兜底，更依赖单元测试和类型检查工具
6. **从"多线程并行"到"GIL 约束"** — CPU 密集型任务需要多进程或 C 扩展
7. **从"Maven 管一切"到"虚拟环境隔离"** — 养成为每个项目创建虚拟环境的习惯

## 参考资料

- [Python 官方文档](https://docs.python.org/zh-cn/3/)
- [PEP 8 — Python 代码风格指南](https://peps.python.org/pep-0008/)
- [PEP 20 — The Zen of Python](https://peps.python.org/pep-0020/)
- [Real Python — Python vs Java](https://realpython.com/oop-in-python-vs-java/)
- [Python 官方文档 - 并发执行](https://docs.python.org/zh-cn/3/library/concurrency.html)
