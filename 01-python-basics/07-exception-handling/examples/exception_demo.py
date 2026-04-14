#!/usr/bin/env python3
"""
Python 异常处理完整演示

模块: 01-Python 基础
知识点: 异常处理
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python exception_demo.py

描述:
    演示 Python 异常处理的核心知识：
    1. try/except/finally/else 基本用法
    2. 多异常捕获
    3. 异常链（raise from）
    4. 自定义异常类
    5. 上下文管理器（__enter__/__exit__）
    6. contextlib.contextmanager
    每个部分都在注释中与 Java 进行对比。
"""

import json
import time
import tempfile
import shutil
from contextlib import contextmanager


# ============================================================
# 1. try/except/finally/else
# ============================================================

def demo_try_except():
    """try/except/finally/else 基本用法"""
    print("=" * 10, "try/except/finally/else", "=" * 10)

    # Java:
    #   try {
    #       int result = 10 / 0;
    #   } catch (ArithmeticException e) {
    #       System.out.println("捕获: " + e.getMessage());
    #   } finally {
    #       System.out.println("finally 执行");
    #   }
    #   // Java 没有 else 子句！

    # --- 基本用法 ---
    print("--- 基本用法 ---")
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        # 类似 Java: catch (ArithmeticException e)
        print(f"捕获到异常: {e}")
    finally:
        # 类似 Java: finally { }
        print("finally: 无论如何都会执行")

    # --- else 子句（Java 没有！）---
    print("--- else 子句 ---")
    try:
        result = 10 / 2
    except ZeroDivisionError as e:
        print(f"捕获到异常: {e}")
    else:
        # Python 独有：try 块没有异常时执行
        # 好处：将"正常逻辑"和"异常处理"清晰分离
        print(f"结果: {result}")
        print("else: 没有异常时执行")
    finally:
        print("finally: 清理完成")

    print()


# ============================================================
# 2. 多异常捕获
# ============================================================

def demo_multiple_exceptions():
    """多异常捕获"""
    print("=" * 10, "多异常捕获", "=" * 10)

    # Java:
    #   // Java 7+ 多异常捕获
    #   try { ... }
    #   catch (IOException | SQLException e) { ... }
    #
    # Python: 用元组捕获多种异常

    # --- 捕获多种异常（合并处理）---
    print("--- 捕获多种异常 ---")
    test_values = ["abc", "123", None]
    for val in test_values:
        try:
            result = int(val)
            print(f"转换成功: {val} -> {result}")
        except (ValueError, TypeError) as e:
            # 类似 Java: catch (NumberFormatException | NullPointerException e)
            print(f"{type(e).__name__}: {e}")

    # --- 分别处理不同异常 ---
    print("--- 分别处理不同异常 ---")
    data = {"a": 1, "b": 2}
    test_cases = [
        lambda: [1, 2, 3][10],       # IndexError
        lambda: data["z"],            # KeyError
    ]
    for case in test_cases:
        try:
            case()
        except IndexError as e:
            print(f"索引越界: {e}")
        except KeyError as e:
            print(f"键不存在: {e}")

    print()


# ============================================================
# 3. 异常链 (raise from)
# ============================================================

def demo_exception_chaining():
    """异常链（raise from）"""
    print("=" * 10, "异常链 (raise from)", "=" * 10)

    # Java:
    #   try { ... }
    #   catch (IOException e) {
    #       throw new RuntimeException("处理失败", e);  // 传递 cause
    #   }
    #
    # Python: raise NewException("msg") from original_exception

    def process_config(text: str) -> dict:
        """解析配置文本，演示异常链"""
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            # raise ... from e 保留原始异常信息
            # 类似 Java: throw new ConfigException("msg", e);
            raise ValueError(f"配置格式错误") from e

    print("--- 异常链演示 ---")
    try:
        process_config("not valid json")
    except ValueError as e:
        print(f"转换后的异常: 数据处理失败: {e}")
        # __cause__ 属性保存原始异常（类似 Java 的 getCause()）
        if e.__cause__:
            print(f"原始异常: {e.__cause__}")

    print()


# ============================================================
# 4. 自定义异常
# ============================================================

def demo_custom_exceptions():
    """自定义异常类"""
    print("=" * 10, "自定义异常", "=" * 10)

    # Java:
    #   public class AppException extends Exception {
    #       private int errorCode;
    #       public AppException(String msg, int code) {
    #           super(msg); this.errorCode = code;
    #       }
    #   }
    #
    # Python: 继承 Exception，简洁得多

    # --- 定义异常层级 ---
    class AppError(Exception):
        """应用异常基类"""
        pass

    class BusinessError(AppError):
        """业务异常"""
        def __init__(self, message: str, error_code: int):
            super().__init__(message)
            self.error_code = error_code

    class InsufficientBalanceError(BusinessError):
        """余额不足异常"""
        def __init__(self, required: float, current: float):
            message = f"余额不足，需要 {required:.2f}，当前 {current:.2f}"
            super().__init__(message, error_code=4001)
            self.required = required
            self.current = current

    # --- 使用自定义异常 ---
    print("--- 自定义异常层级 ---")
    try:
        raise InsufficientBalanceError(required=1000.0, current=500.0)
    except BusinessError as e:
        print(f"捕获到业务异常: {e}")
        print(f"错误代码: {e.error_code}")

    # --- 异常继承链：可以用父类捕获子类异常 ---
    print("--- 自定义异常的继承 ---")
    try:
        raise InsufficientBalanceError(required=1000.0, current=500.0)
    except AppError as e:
        # 用基类 AppError 也能捕获子类 InsufficientBalanceError
        # 类似 Java: catch (AppException e) 也能捕获子类
        print(f"捕获到应用异常: {e}")

    print()


# ============================================================
# 5. 上下文管理器 (with 语句)
# ============================================================

def demo_context_manager():
    """上下文管理器（with 语句）"""
    print("=" * 10, "上下文管理器 (with)", "=" * 10)

    # Java:
    #   // Java 7+ try-with-resources，要求实现 AutoCloseable
    #   try (Connection conn = getConnection()) {
    #       // 使用 conn
    #   }  // 自动调用 conn.close()
    #
    # Python:
    #   with 语句更通用，不仅限于"关闭资源"
    #   可以用于任何"进入/退出"场景：锁、事务、临时状态等

    # --- 自定义上下文管理器（类实现）---
    class Timer:
        """计时器上下文管理器"""
        def __init__(self, name: str = "Timer"):
            self.name = name
            self.start_time = None

        def __enter__(self):
            """进入 with 块时调用（类似 Java AutoCloseable 的构造）"""
            self.start_time = time.time()
            print(f"[{self.name}] 开始计时...")
            return self  # 返回值绑定到 as 变量

        def __exit__(self, exc_type, exc_val, exc_tb):
            """退出 with 块时调用（类似 Java AutoCloseable.close()）
            参数:
                exc_type: 异常类型（无异常时为 None）
                exc_val:  异常值
                exc_tb:   异常追踪信息
            返回:
                True  -> 吞掉异常（不推荐）
                False -> 让异常正常传播
            """
            elapsed = time.time() - self.start_time
            print(f"[{self.name}] 结束，耗时: {elapsed:.2f} 秒")
            return False  # 不吞掉异常

    print("--- 自定义上下文管理器（类实现）---")
    with Timer("Timer") as t:
        print("执行一些操作...")
        time.sleep(0.1)

    # --- contextlib.contextmanager（更简洁的方式）---
    @contextmanager
    def temp_directory(prefix: str = "demo_"):
        """临时目录上下文管理器

        使用 @contextmanager 装饰器，yield 之前是 __enter__，
        yield 之后是 __exit__（清理代码）。
        比写完整的类更简洁。
        """
        path = tempfile.mkdtemp(prefix=prefix)
        print(f"[TempDir] 创建临时目录: {path}")
        try:
            yield path  # yield 的值绑定到 as 变量
        finally:
            shutil.rmtree(path, ignore_errors=True)
            print(f"[TempDir] 清理临时目录: {path}")

    print("--- contextlib.contextmanager ---")
    with temp_directory() as tmpdir:
        print(f"在临时目录中工作...")
        # tmpdir 会在 with 块结束后自动删除

    print()


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数：依次演示所有异常处理知识点"""
    demo_try_except()
    demo_multiple_exceptions()
    demo_exception_chaining()
    demo_custom_exceptions()
    demo_context_manager()


if __name__ == "__main__":
    main()
