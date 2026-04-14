#!/usr/bin/env python3
"""
Python 函数定义与高阶函数演示

模块: 01-Python 基础
知识点: 函数与装饰器
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python functions_demo.py

描述:
    演示 Python 函数的核心特性：
    1. 函数定义与默认参数
    2. *args 和 **kwargs（可变参数）
    3. 返回多值
    4. Lambda 表达式
    5. 高阶函数（map/filter/sorted）
    6. 函数作为一等公民
    每个部分都在注释中与 Java 进行对比。
"""


def demo_function_definition():
    """函数定义与默认参数"""
    print("=" * 10, "函数定义与默认参数", "=" * 10)

    # Java: 不支持默认参数，需要方法重载
    #   public String greet(String name) { return greet(name, "Hello"); }
    #   public String greet(String name, String greeting) { return greeting + ", " + name + "!"; }
    # Python: 直接使用默认参数，一个函数搞定
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"

    print(f"greet('Alice') = {greet('Alice')}")
    print(f"greet('Bob', 'Hi') = {greet('Bob', 'Hi')}")

    # Java: 方法重载实现不同参数个数
    # Python: 默认参数 + 灵活调用
    def add(a, b, c=0):
        return a + b + c

    print(f"add(1, 2) = {add(1, 2)}")
    print(f"add(1, 2, 3) = {add(1, 2, 3)}")
    print()


def demo_args_kwargs():
    """*args 和 **kwargs"""
    print("=" * 10, "*args 和 **kwargs", "=" * 10)

    # --- *args：可变位置参数 ---
    # Java: public static int sum(int... numbers) — 只能有一个可变参数
    # Python: *args 收集所有额外的位置参数为 tuple
    print("--- *args（可变位置参数）---")

    def sum_all(*args):
        """接收任意数量的位置参数"""
        return sum(args)  # args 是一个 tuple

    print(f"sum_all(1, 2, 3) = {sum_all(1, 2, 3)}")
    print(f"sum_all(1, 2, 3, 4, 5) = {sum_all(1, 2, 3, 4, 5)}")

    # --- **kwargs：可变关键字参数 ---
    # Java: 没有对应概念，最接近的是 Map<String, Object> 参数
    # Python: **kwargs 收集所有额外的关键字参数为 dict
    print("--- **kwargs（可变关键字参数）---")

    def build_profile(name, **kwargs):
        """接收必需参数 + 任意关键字参数"""
        profile = {"name": name}
        profile.update(kwargs)
        return profile

    result = build_profile("Alice", age=25, city="北京", job="engineer")
    print("build_profile:")
    for key, value in result.items():
        print(f"  {key}: {value}")

    # --- 混合使用 ---
    # 参数顺序：普通参数 → *args → **kwargs
    print("--- 混合使用 ---")

    def mixed(a, *args, **kwargs):
        print(f"mixed({a}, {', '.join(map(str, args))}, "
              f"{', '.join(f'{k}={v}' for k, v in kwargs.items())}):")
        print(f"  a = {a}")
        print(f"  args = {args}")
        print(f"  kwargs = {kwargs}")

    mixed(1, 2, 3, x=10, y=20)
    print()


def demo_multiple_return():
    """返回多值"""
    print("=" * 10, "返回多值", "=" * 10)

    # Java: 不能直接返回多个值，需要封装为对象或数组
    #   public class DivResult { int quotient; int remainder; }
    # Python: 直接返回 tuple，用解构赋值接收
    def divmod_custom(a, b):
        """返回商和余数"""
        return a // b, a % b  # 返回 tuple

    quotient, remainder = divmod_custom(10, 3)  # 解构赋值
    print(f"商: {quotient}, 余数: {remainder}")

    # 返回更多值
    def statistics(numbers):
        """返回最小值、最大值、平均值"""
        return min(numbers), max(numbers), sum(numbers) / len(numbers)

    data = [23, 1, 45, 99, 42]
    min_val, max_val, avg_val = statistics(data)
    print(f"最小值: {min_val}, 最大值: {max_val}, 平均值: {avg_val}")
    print()


def demo_lambda():
    """Lambda 表达式"""
    print("=" * 10, "Lambda 表达式", "=" * 10)

    # Java: Function<Integer, Integer> square = x -> x * x;
    # Python: lambda 更简洁，不需要函数式接口
    square = lambda x: x * x
    print(f"square(5) = {square(5)}")

    # Java: BiFunction<Integer, Integer, Integer> add = (a, b) -> a + b;
    add = lambda a, b: a + b
    print(f"add(3, 4) = {add(3, 4)}")

    # lambda 常用于简单的条件判断
    is_even = lambda n: n % 2 == 0
    print(f"条件 lambda: is_even(4) = {is_even(4)}, is_even(3) = {is_even(3)}")
    print()


def demo_higher_order_functions():
    """高阶函数（map/filter/sorted）"""
    print("=" * 10, "高阶函数", "=" * 10)

    numbers = [1, 2, 3, 4, 5]

    # --- map：对每个元素应用函数 ---
    # Java: numbers.stream().map(n -> n * n).collect(Collectors.toList())
    # Python: map() 或列表推导式
    print("--- map ---")
    squares = list(map(lambda x: x * x, numbers))
    print(f"平方: {squares}")
    # 更 Pythonic: [x * x for x in numbers]

    # --- filter：过滤元素 ---
    # Java: numbers.stream().filter(n -> n % 2 == 0).collect(Collectors.toList())
    print("--- filter ---")
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"偶数: {evens}")
    # 更 Pythonic: [x for x in numbers if x % 2 == 0]

    # --- sorted：排序（支持 key 参数）---
    # Java: names.sort(Comparator.naturalOrder())
    # Python: sorted() 返回新列表，key 参数指定排序依据
    print("--- sorted ---")
    names = ["Charlie", "Alice", "Bob"]
    print(f"按名字排序: {sorted(names)}")

    # 按自定义规则排序
    people = [("Alice", 25), ("Bob", 20), ("Charlie", 30)]
    by_age = sorted(people, key=lambda p: p[1])
    print(f"按年龄排序: {by_age}")

    # --- 函数作为参数 ---
    # Java: 需要函数式接口 Function<T, R>
    # Python: 直接传递函数对象
    print("--- 函数作为参数 ---")

    def apply(x, func):
        """接收一个值和一个函数，返回函数应用结果"""
        return func(x)

    def square(x):
        return x * x

    def double(x):
        return x * 2

    print(f"apply(5, square) = {apply(5, square)}")
    print(f"apply(5, double) = {apply(5, double)}")
    print()


def demo_first_class_functions():
    """函数是一等公民"""
    print("=" * 10, "函数是一等公民", "=" * 10)

    # 1. 函数赋值给变量
    # Java: 需要方法引用 Math::abs 或 Lambda
    # Python: 函数名本身就是变量
    def square(x):
        return x * x

    f = square  # 函数赋值给变量
    print(f"函数赋值给变量: f(3) = {f(3)}")

    # 2. 函数存储在数据结构中
    # Java: Map<String, Function<...>> — 需要泛型声明
    # Python: 直接存储
    ops = {
        "add": lambda a, b: a + b,
        "sub": lambda a, b: a - b,
        "mul": lambda a, b: a * b,
    }
    print(f"函数存储在字典中: ops['add'](10, 3) = {ops['add'](10, 3)}")

    # 3. 函数列表批量执行
    transforms = [
        lambda x: x + 1,
        lambda x: x * 2,
        lambda x: x ** 2,
    ]
    value = 2
    results = [t(value) for t in transforms]
    print(f"函数列表批量执行: {results}")
    print()


def main():
    """主函数：依次演示所有函数特性"""
    demo_function_definition()
    demo_args_kwargs()
    demo_multiple_return()
    demo_lambda()
    demo_higher_order_functions()
    demo_first_class_functions()


if __name__ == "__main__":
    main()
