#!/usr/bin/env python3
"""
Python 列表推导式与生成器完整演示

模块: 01-Python 基础
知识点: 列表推导式与生成器
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python comprehensions_demo.py

描述:
    演示 Python 推导式与生成器的核心知识：
    1. 列表推导式（含条件过滤、嵌套）
    2. 字典推导式
    3. 集合推导式
    4. 生成器函数（yield）
    5. 生成器表达式
    6. itertools 常用函数
    每个部分都在注释中与 Java Stream API 对比。
"""

import sys
import itertools


# ============================================================
# 1. 列表推导式
# ============================================================

def demo_list_comprehension():
    """列表推导式"""
    print("=" * 10, "列表推导式", "=" * 10)

    # Java Stream 等价写法在注释中对比

    # --- 基本用法 ---
    print("--- 基本用法 ---")
    # Java: IntStream.rangeClosed(1, 5).map(x -> x * x).boxed().toList()
    squares = [x * x for x in range(1, 6)]
    print(f"平方数: {squares}")

    # --- 条件过滤 ---
    print("--- 条件过滤 ---")
    # Java: IntStream.rangeClosed(1, 10).filter(x -> x % 2 == 0)
    #           .map(x -> x * x).boxed().toList()
    even_squares = [x * x for x in range(1, 11) if x % 2 == 0]
    print(f"偶数平方: {even_squares}")

    # --- 嵌套推导式 ---
    print("--- 嵌套推导式 ---")
    # Java: nested.stream().flatMap(Collection::stream).toList()
    nested = [[1, 2], [3, 4], [5, 6]]
    flat = [x for sublist in nested for x in sublist]
    print(f"扁平化: {flat}")

    # 九九乘法表（部分）
    # Java: 需要嵌套 flatMap
    multiplication = [f"{i}x{j}={i*j}" for i in range(1, 4) for j in range(i, 4)]
    print(f"九九乘法（部分）: {multiplication}")

    # --- 条件表达式（三元运算符）---
    print("--- 条件表达式 ---")
    # Java: stream.map(x -> x % 2 == 0 ? "偶" : "奇").toList()
    labels = ["奇" if x % 2 != 0 else "偶" for x in range(1, 6)]
    print(f"奇偶标记: {labels}")

    print()


# ============================================================
# 2. 字典推导式
# ============================================================

def demo_dict_comprehension():
    """字典推导式"""
    print("=" * 10, "字典推导式", "=" * 10)

    # Java: stream.collect(Collectors.toMap(x -> x, x -> x * x))

    # 数字 → 平方
    square_dict = {x: x * x for x in range(1, 6)}
    print(f"平方字典: {square_dict}")

    # 单词 → 长度
    words = ["hello", "world", "python"]
    word_lengths = {w: len(w) for w in words}
    print(f"单词长度: {word_lengths}")

    # 键值互换
    original = {"a": 1, "b": 2, "c": 3}
    swapped = {v: k for k, v in original.items()}
    print(f"键值互换: {swapped}")

    print()


# ============================================================
# 3. 集合推导式
# ============================================================

def demo_set_comprehension():
    """集合推导式"""
    print("=" * 10, "集合推导式", "=" * 10)

    # Java: stream.collect(Collectors.toSet())

    # 提取首字母（自动去重）
    languages = ["Python", "Java", "Go", "JavaScript", "PHP"]
    first_chars = {lang[0] for lang in languages}
    print(f"首字母集合: {first_chars}")

    # 去重
    numbers = [-3, -2, -1, 0, 1, 2, 3]
    unique_squares = {x * x for x in numbers}
    print(f"去重平方: {sorted(unique_squares)}")

    print()


# ============================================================
# 4. 生成器函数 (yield)
# ============================================================

def demo_generator_function():
    """生成器函数（yield）"""
    print("=" * 10, "生成器函数 (yield)", "=" * 10)

    # Java:
    #   // Java 没有 yield 关键字
    #   // 最接近的是 Stream.iterate() 或自定义 Spliterator
    #   Stream<Integer> countdown = Stream.iterate(5, n -> n > 0, n -> n - 1);

    # --- 基本生成器 ---
    print("--- 基本生成器 ---")

    def countdown(n):
        """倒计时生成器"""
        while n > 0:
            yield n  # 暂停并产出值，下次调用从这里继续
            n -= 1

    print("倒计时:", end=" ")
    for num in countdown(5):
        print(num, end=" ")
    print()

    # --- 斐波那契生成器 ---
    print("--- 斐波那契生成器 ---")

    def fibonacci():
        """无限斐波那契数列生成器"""
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    # Java: Stream.iterate(new int[]{0,1}, f -> new int[]{f[1], f[0]+f[1]})
    #           .map(f -> f[0]).limit(10).toList()
    fib_10 = list(itertools.islice(fibonacci(), 10))
    print(f"前 10 个斐波那契数: {fib_10}")

    # --- yield from（委托生成器，Python 3.3+）---
    print("--- yield from ---")

    def flatten(nested_list):
        """递归扁平化嵌套列表"""
        for item in nested_list:
            if isinstance(item, list):
                yield from flatten(item)  # 委托给子生成器
            else:
                yield item

    nested = [[1, 2], [3, [4, 5]], 6]
    print(f"扁平化结果: {list(flatten(nested))}")

    print()


# ============================================================
# 5. 生成器表达式
# ============================================================

def demo_generator_expression():
    """生成器表达式"""
    print("=" * 10, "生成器表达式", "=" * 10)

    # 生成器表达式 = 列表推导式的惰性版本
    # 把 [] 换成 () 就行

    # 列表推导式：立即计算，占用内存
    list_comp = [x * x for x in range(10)]

    # 生成器表达式：惰性计算，几乎不占内存
    gen_expr = (x * x for x in range(10))
    print(f"生成器对象: {gen_expr}")

    # 生成器表达式常用于聚合函数
    # Java: IntStream.rangeClosed(1, 10).filter(x -> x % 2 != 0)
    #           .map(x -> x * x).sum()
    total = sum(x * x for x in range(1, 11) if x % 2 != 0)
    print(f"求和（惰性）: {total}")

    # --- 内存对比 ---
    print("--- 内存对比 ---")
    list_size = sys.getsizeof([x for x in range(1000)])
    gen_size = sys.getsizeof(x for x in range(1000))
    print(f"列表占用: {list_size} 字节, 生成器占用: {gen_size} 字节")

    print()


# ============================================================
# 6. itertools 常用函数
# ============================================================

def demo_itertools():
    """itertools 常用函数"""
    print("=" * 10, "itertools 常用函数", "=" * 10)

    # itertools 提供高效的迭代器工具
    # 类似 Java Stream 的各种中间操作

    # --- chain（链接多个迭代器）---
    print("--- chain（链接多个迭代器）---")
    # Java: Stream.concat(stream1, stream2)
    result = list(itertools.chain([1, 2, 3], ["a", "b", "c"]))
    print(f"chain: {result}")

    # --- islice（切片）---
    print("--- islice（切片）---")
    # Java: stream.skip(0).limit(5)
    result = list(itertools.islice(range(100), 5))
    print(f"islice: {result}")

    # --- product（笛卡尔积）---
    print("--- product（笛卡尔积）---")
    # Java: 需要嵌套 flatMap
    result = list(itertools.product(["A", "B"], [1, 2]))
    print(f"product: {result}")

    # --- groupby（分组）---
    print("--- groupby（分组）---")
    # Java: stream.collect(Collectors.groupingBy(...))
    # 注意：groupby 要求输入已排序！
    numbers = [1, 2, 3, 4, 5, 6]
    for key, group in itertools.groupby(sorted(numbers), key=lambda x: x % 2 == 0):
        print(f"  {'偶数' if key else '奇数'}: {list(group)}")

    # --- accumulate（累积）---
    print("--- accumulate（累积）---")
    # Java: 无直接等价，需要自定义 reduce
    result = list(itertools.accumulate([1, 2, 3, 4, 5]))
    print(f"累积和: {result}")

    # --- combinations / permutations ---
    print("--- combinations / permutations ---")
    # Java: 无内置支持
    items = ["a", "b", "c"]
    combos = list(itertools.combinations(items, 2))
    perms = list(itertools.permutations(items, 2))
    print(f"组合 C(3,2): {combos}")
    print(f"排列 P(3,2): {perms}")

    print()


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数：依次演示所有推导式与生成器知识点"""
    demo_list_comprehension()
    demo_dict_comprehension()
    demo_set_comprehension()
    demo_generator_function()
    demo_generator_expression()
    demo_itertools()


if __name__ == "__main__":
    main()
