#!/usr/bin/env python3
"""
Python 装饰器原理与实战演示

模块: 01-Python 基础
知识点: 函数与装饰器
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python decorators_demo.py

描述:
    演示装饰器的完整知识体系：
    1. 闭包基础（装饰器的前置知识）
    2. 从闭包到装饰器的演进
    3. functools.wraps 保留元信息
    4. 带参数的装饰器
    5. 实用装饰器示例（计时器、重试）
    6. 常用内置装饰器（@property、@staticmethod、@classmethod）
    7. 装饰器叠加
    每个部分都在注释中与 Java 进行对比。
"""

import functools
import math
import time


# ============================================================
# 第一部分：闭包基础
# ============================================================

def demo_closure():
    """闭包基础 — 装饰器的前置知识"""
    print("=" * 10, "闭包基础", "=" * 10)

    # 闭包：内部函数引用了外部函数的变量
    # Java 中没有直接对应概念（最接近的是匿名内部类捕获 effectively final 变量）
    def make_counter():
        count = 0  # 外部函数的局部变量

        def counter():
            nonlocal count  # 声明使用外部变量（类似 Java 的 effectively final 限制的突破）
            count += 1
            return count

        return counter  # 返回内部函数

    counter = make_counter()
    print(f"counter() = {counter()}")  # 1
    print(f"counter() = {counter()}")  # 2
    print(f"counter() = {counter()}")  # 3
    print("闭包让函数\"记住\"了外部变量 count")
    print()


# ============================================================
# 第二部分：从闭包到装饰器
# ============================================================

def demo_basic_decorator():
    """从闭包到装饰器"""
    print("=" * 10, "从闭包到装饰器", "=" * 10)

    # 装饰器本质：接收函数，返回增强后的新函数
    # Java 中没有对应语法，最接近的是 Spring AOP 的切面编程
    def log_call(func):
        """简单的日志装饰器"""
        def wrapper(*args, **kwargs):
            print(f"调用: {func.__name__}()")
            return func(*args, **kwargs)
        return wrapper

    # --- 手动装饰（装饰器的本质）---
    print("--- 手动装饰 ---")

    def say_hello():
        print("Hello!")

    say_hello = log_call(say_hello)  # 手动装饰
    say_hello()

    # --- @语法糖（等价写法，更优雅）---
    print("--- @语法糖（等价写法）---")

    @log_call  # 等价于 say_goodbye = log_call(say_goodbye)
    def say_goodbye():
        print("Goodbye!")

    say_goodbye()
    print()


# ============================================================
# 第三部分：functools.wraps
# ============================================================

def demo_functools_wraps():
    """functools.wraps 保留元信息"""
    print("=" * 10, "functools.wraps 保留元信息", "=" * 10)

    # 不使用 @wraps 的装饰器
    def bad_decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    # 使用 @wraps 的装饰器
    def good_decorator(func):
        @functools.wraps(func)  # 保留原函数的 __name__、__doc__ 等
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    @bad_decorator
    def func_without_wraps():
        """这是原始函数的文档"""
        pass

    @good_decorator
    def my_function():
        """这是原始函数的文档"""
        pass

    print(f"没有 @wraps: 函数名={func_without_wraps.__name__}, "
          f"文档={func_without_wraps.__doc__}")
    print(f"有 @wraps: 函数名={my_function.__name__}, "
          f"文档={my_function.__doc__}")
    print()


# ============================================================
# 第四部分：带参数的装饰器
# ============================================================

def demo_decorator_with_args():
    """带参数的装饰器"""
    print("=" * 10, "带参数的装饰器", "=" * 10)

    # 带参数的装饰器需要三层嵌套：
    # 外层：接收装饰器参数
    # 中层：接收被装饰函数
    # 内层：实际的 wrapper
    def log(level="INFO"):
        """带日志级别参数的装饰器"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                print(f"[{level}] {func.__doc__ or func.__name__}: {func.__name__}()")
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @log(level="INFO")
    def login():
        """用户登录"""
        pass

    @log(level="DEBUG")
    def query_data():
        """数据查询"""
        pass

    login()
    query_data()
    print()


# ============================================================
# 第五部分：实用装饰器
# ============================================================

def demo_timer_decorator():
    """实用装饰器：计时器"""
    print("=" * 10, "实用装饰器：计时器", "=" * 10)

    def timer(func):
        """测量函数执行时间的装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            print(f"{func.__name__} 耗时: {elapsed:.2f}s")
            return result
        return wrapper

    @timer
    def process_data():
        """模拟耗时操作"""
        print("模拟耗时操作...")
        time.sleep(0.5)
        return "完成"

    process_data()
    print()


def demo_retry_decorator():
    """实用装饰器：重试"""
    print("=" * 10, "实用装饰器：重试", "=" * 10)

    def retry(max_attempts=3, delay=1):
        """自动重试装饰器"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(1, max_attempts + 1):
                    try:
                        print(f"尝试第 {attempt} 次...")
                        return func(*args, **kwargs)
                    except Exception as e:
                        if attempt == max_attempts:
                            print(f"已达最大重试次数 {max_attempts}，抛出异常")
                            raise
                        print(f"操作失败: {e}，{delay}s 后重试...")
                        time.sleep(delay)
            return wrapper
        return decorator

    # 模拟一个不稳定的操作（前两次失败，第三次成功）
    call_count = 0

    @retry(max_attempts=3, delay=1)
    def unstable_operation():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError(f"模拟失败 (第{call_count}次)")
        return f"第{call_count}次成功！"

    result = unstable_operation()
    print(result)
    print()


# ============================================================
# 第六部分：内置装饰器
# ============================================================

def demo_property_decorator():
    """内置装饰器：@property"""
    print("=" * 10, "内置装饰器：@property", "=" * 10)

    # Java: 使用 getter/setter 方法
    #   public double getArea() { return Math.PI * radius * radius; }
    #   public void setRadius(double r) { this.radius = r; }
    # Python: @property 让方法像属性一样访问
    class Circle:
        def __init__(self, radius):
            self._radius = radius

        @property
        def radius(self):
            """获取半径（getter）"""
            return self._radius

        @radius.setter
        def radius(self, value):
            """设置半径（setter），带验证"""
            if value < 0:
                raise ValueError("半径不能为负数")
            self._radius = value

        @property
        def area(self):
            """计算面积（只读属性，没有 setter）"""
            return math.pi * self._radius ** 2

    c = Circle(5)
    print(f"面积: {c.area:.2f}")  # 像属性一样访问，不需要 c.area()

    c.radius = 10  # 像属性一样赋值，自动调用 setter
    print(f"半径: {c.radius}, 面积: {c.area:.2f}")
    print()


def demo_static_class_methods():
    """内置装饰器：@staticmethod 和 @classmethod"""
    print("=" * 10, "内置装饰器：@staticmethod 和 @classmethod", "=" * 10)

    # Java: static 方法和工厂方法
    # Python: @staticmethod 和 @classmethod
    class MathUtils:
        def __init__(self, precision=2):
            self.precision = precision

        @staticmethod
        def is_valid_number(value):
            """静态方法：不需要访问实例或类（类似 Java static 方法）"""
            return isinstance(value, (int, float)) and not math.isnan(value)

        @classmethod
        def create_high_precision(cls):
            """类方法：接收类本身作为第一个参数（常用于工厂方法）"""
            return cls(precision=4)

        def round_pi(self):
            """实例方法：可以访问 self"""
            return round(math.pi, self.precision)

        def __repr__(self):
            return f"MathUtils(precision={self.precision})"

    # 静态方法：通过类名调用
    print(f"静态方法 — 是否有效: {MathUtils.is_valid_number(3.14)}")

    # 类方法：工厂模式创建实例
    utils = MathUtils.create_high_precision()
    print(f"类方法 — 创建实例: {utils}")

    # 实例方法
    print(f"实例方法 — pi ≈ {utils.round_pi()}")
    print()


# ============================================================
# 第七部分：装饰器叠加
# ============================================================

def demo_stacked_decorators():
    """装饰器叠加"""
    print("=" * 10, "装饰器叠加", "=" * 10)

    def log_call(func):
        """日志装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"调用: {func.__name__}{args}")
            result = func(*args, **kwargs)
            print(f"结果: {result}")
            return result
        return wrapper

    def timer(func):
        """计时装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            print(f"{func.__name__} 耗时: {time.time() - start:.4f}s")
            return result
        return wrapper

    # 装饰器叠加：从下往上应用
    # 等价于 add = log_call(timer(add))
    @log_call
    @timer
    def add(a, b):
        return a + b

    add(3, 5)
    print()


def main():
    """主函数：依次演示所有装饰器特性"""
    demo_closure()
    demo_basic_decorator()
    demo_functools_wraps()
    demo_decorator_with_args()
    demo_timer_decorator()
    demo_retry_decorator()
    demo_property_decorator()
    demo_static_class_methods()
    demo_stacked_decorators()


if __name__ == "__main__":
    main()
