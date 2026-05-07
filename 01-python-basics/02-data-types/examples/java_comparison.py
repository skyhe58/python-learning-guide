#!/usr/bin/env python3
"""
Java 与 Python 类型系统对比

模块: 01-Python 基础
知识点: 数据类型与变量
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python java_comparison.py

描述:
    通过注释对比 Java 与 Python 在变量声明、类型推断、
    集合操作、字符串处理等方面的差异，帮助 Java 开发者
    快速理解 Python 的类型系统。
"""


def variable_declaration():
    """变量声明对比"""
    print("===== 变量声明对比 =====")

    # ---- Java 写法 ----
    # int age = 25;           // 必须声明类型
    # String name = "Alice";  // 必须声明类型
    # final int MAX = 100;    // final 表示常量

    # ---- Python 写法 ----
    age = 25          # 不需要声明类型，自动推断为 int
    name = "Alice"    # 自动推断为 str
    MAX = 100         # Python 没有 final，约定全大写表示常量

    print(f"Python 不需要声明类型: name = {name}, age = {age}")

    # ---- Java 中变量类型不能改变 ----
    # int x = 10;
    # x = "hello";  // 编译错误！不能把 String 赋给 int

    # ---- Python 中同一变量可以改变类型（动态类型） ----
    x = 10        # x 是 int
    x = "hello"   # x 变成了 str，完全合法
    print(f"同一变量可以改变类型: x 从 int(10) 变为 str({x})")
    print()


def integer_precision():
    """整数精度对比"""
    print("===== 整数精度对比 =====")

    # ---- Java 写法 ----
    # int x = Integer.MAX_VALUE;     // 2147483647（32位）
    # long y = Long.MAX_VALUE;       // 9223372036854775807（64位）
    # // 超过 long 范围需要用 BigInteger
    # BigInteger big = new BigInteger("999999999999999999999999999999");

    # ---- Python 写法 ----
    # Python 整数没有大小限制，自动扩展精度
    big = 10 ** 50  # 10 的 50 次方
    print(f"Python 大整数: {big}")
    print("Java 中这会溢出！Python 整数无大小限制")
    print()


def collections_comparison():
    """集合操作对比"""
    print("===== 集合操作对比 =====")

    # ---- Java List vs Python list ----
    # Java:
    #   List<String> fruits = new ArrayList<>();
    #   fruits.add("apple");
    #   fruits.add("banana");
    #   fruits.add("cherry");
    #   String first = fruits.get(0);
    #   int size = fruits.size();

    # Python:
    fruits = ["apple", "banana"]
    fruits.append("cherry")       # add() → append()
    first = fruits[0]             # get(0) → [0]
    size = len(fruits)            # size() → len()
    print(f"Python list（类似 ArrayList）: {fruits}")

    # ---- Java Map vs Python dict ----
    # Java:
    #   Map<String, Integer> scores = new HashMap<>();
    #   scores.put("Alice", 95);
    #   scores.put("Bob", 87);
    #   int score = scores.get("Alice");
    #   boolean has = scores.containsKey("Alice");

    # Python:
    scores = {"Alice": 95, "Bob": 87}
    scores["Charlie"] = 92        # put() → 直接赋值
    score = scores["Alice"]       # get() → []
    has = "Alice" in scores       # containsKey() → in
    print(f"Python dict（类似 HashMap）: {scores}")

    # ---- Java Set vs Python set ----
    # Java:
    #   Set<Integer> numbers = new HashSet<>(Arrays.asList(1, 2, 3, 4, 5));
    #   numbers.add(6);
    #   boolean contains = numbers.contains(3);

    # Python:
    numbers = {1, 2, 3, 4, 5}
    numbers.add(6)                # add() 方法名一样
    contains = 3 in numbers       # contains() → in
    print(f"Python set（类似 HashSet）: {numbers}")
    print()


def string_comparison():
    """字符串操作对比"""
    print("===== 字符串对比 =====")

    # ---- Java 字符串格式化 ----
    # String name = "Alice";
    # int age = 25;
    # String msg = String.format("Hello, %s! You are %d years old.", name, age);
    # // Java 15+ text blocks:
    # String text = """
    #     第一行
    #     第二行
    #     """;

    # ---- Python 字符串格式化 ----
    name = "Alice"
    age = 25

    # f-string（Python 3.6+，最推荐的方式）
    msg = f"Hello, {name}! You are {age} years old."
    print(f"Python f-string: {msg}")

    # 多行字符串（Python 一直支持，Java 13+ 才有 text blocks）
    text = """    这是第一行
    这是第二行
    这是第三行"""
    print(f"多行字符串（Java 13+ 才支持 text blocks）:\n{text}")

    # ---- Java 字符串方法 vs Python ----
    # Java:                    Python:
    # s.length()               len(s)
    # s.toUpperCase()          s.upper()
    # s.toLowerCase()          s.lower()
    # s.trim()                 s.strip()
    # s.substring(0, 5)        s[0:5]  （切片语法）
    # s.contains("abc")        "abc" in s
    # s.startsWith("He")       s.startswith("He")
    # s.replace("a", "b")      s.replace("a", "b")  （方法名一样）
    # s.split(",")             s.split(",")          （方法名一样）
    print()


def type_checking_comparison():
    """类型检查对比"""
    print("===== 类型检查对比 =====")

    # ---- Java 类型检查 ----
    # Object obj = 42;
    # if (obj instanceof Integer) { ... }
    # Class<?> cls = obj.getClass();

    # ---- Python 类型检查 ----
    obj = 42

    # type() — 获取精确类型（类似 Java 的 getClass()）
    print("Python 用 type() 和 isinstance() 检查类型")
    print(f"type(42) = {type(obj)}")

    # isinstance() — 检查类型（类似 Java 的 instanceof）
    # 支持检查多个类型（传入元组）
    print(f"isinstance(42, (int, float)) = {isinstance(obj, (int, float))}")

    # ---- Java 类型转换 ----
    # int x = Integer.parseInt("123");
    # String s = String.valueOf(456);
    # double d = (double) x;  // 强制转换

    # ---- Python 类型转换 ----
    # Python 使用类型名作为转换函数，更直观
    # int("123")    — 类似 Integer.parseInt()
    # str(456)      — 类似 String.valueOf()
    # float(42)     — 类似 (double) 强制转换
    print()


def type_annotation_comparison():
    """类型注解对比"""
    print("===== 类型注解对比 =====")

    # ---- Java：类型声明是强制的 ----
    # public String greet(String name, int age) {
    #     return String.format("Hello, %s! Age: %d", name, age);
    # }

    # ---- Python：类型注解是可选的（PEP 484） ----
    # 不加注解也完全合法
    def greet_simple(name, age):
        return f"Hello, {name}! Age: {age}"

    # 加上类型注解（推荐，提高可读性，IDE 可以做类型检查）
    def greet_typed(name: str, age: int) -> str:
        return f"Hello, {name}! Age: {age}"

    result1 = greet_simple("Alice", 25)
    result2 = greet_typed("Bob", 30)
    print(f"无注解函数: {result1}")
    print(f"有注解函数: {result2}")
    print("Python 类型注解不会在运行时强制检查，仅供 IDE 和 mypy 等工具使用")

    # Python 3.9+ 可以直接用内置类型作为泛型
    # Java: List<String>
    # Python: list[str]
    names: list[str] = ["Alice", "Bob"]
    scores: dict[str, int] = {"Alice": 95, "Bob": 87}
    print(f"list[str]: {names}")
    print(f"dict[str, int]: {scores}")
    print()


def main():
    """主函数：依次展示各项对比"""
    variable_declaration()
    integer_precision()
    collections_comparison()
    string_comparison()
    type_checking_comparison()
    type_annotation_comparison()


if __name__ == "__main__":
    main()
