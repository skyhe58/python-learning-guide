#!/usr/bin/env python3
"""
Python 控制流综合演示

模块: 01-Python 基础
知识点: 控制流（条件/循环）
Python 版本: >= 3.9（match-case 需要 >= 3.10）
最后验证: 2025-07-15

运行方式:
    python control_flow_demo.py

描述:
    演示 Python 控制流的所有核心特性：
    1. if/elif/else 条件判断
    2. for 循环（遍历 list、dict、range、enumerate、zip）
    3. while 循环
    4. match-case 模式匹配（Python 3.10+）
    5. break/continue/else
    6. 三元表达式（条件表达式）
    每个部分都在注释中与 Java 进行对比。
"""

import sys


def demo_if_elif_else():
    """if/elif/else 条件判断"""
    print("=" * 10, "if/elif/else 条件判断", "=" * 10)

    # Java: if (score >= 90) { grade = "A"; } else if (score >= 80) { ... }
    # Python: 不需要括号和花括号，用缩进定义代码块
    score = 85
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    else:
        grade = "D"
    print(f"分数 {score} 的等级: {grade}")

    # Java: boolean isAdult = (age >= 18);
    # Python: 条件判断更简洁
    age = 18
    if age >= 18:
        print(f"{age} 是成年人")
    else:
        print(f"{age} 是未成年人")
    print()


def demo_for_loop():
    """for 循环遍历"""
    print("=" * 10, "for 循环遍历", "=" * 10)

    # --- 遍历列表 ---
    # Java: for (String fruit : fruits) { System.out.println(fruit); }
    # Python: 语法更简洁
    print("--- 遍历列表 ---")
    fruits = ["apple", "banana", "cherry"]
    for fruit in fruits:
        print(f"水果: {fruit}")

    # --- 遍历字典 ---
    # Java: for (Map.Entry<String, Integer> entry : map.entrySet()) { ... }
    # Python: 直接解构键值对
    print("--- 遍历字典 ---")
    scores = {"Alice": 95, "Bob": 87, "Charlie": 92}
    for name, score in scores.items():
        print(f"{name}: {score}")

    # --- range() 生成序列 ---
    # Java: for (int i = 0; i < 5; i++) { ... }
    # Python: range(5) 生成 0, 1, 2, 3, 4
    print("--- range() 生成序列 ---")
    print(" ".join(str(i) for i in range(5)))

    # --- enumerate() 带索引遍历 ---
    # Java: 需要手动维护索引变量，或用 IntStream.range()
    # Python: enumerate() 同时获取索引和值
    print("--- enumerate() 带索引遍历 ---")
    for index, fruit in enumerate(fruits):
        print(f"索引 {index}: {fruit}")

    # --- zip() 并行遍历 ---
    # Java: 没有内置的并行遍历支持，需要用索引
    # Python: zip() 将多个可迭代对象打包
    print("--- zip() 并行遍历 ---")
    names = ["Alice", "Bob", "Charlie"]
    grades = [95, 87, 92]
    for name, grade in zip(names, grades):
        print(f"{name} 的成绩是 {grade}")
    print()


def demo_while_loop():
    """while 循环"""
    print("=" * 10, "while 循环", "=" * 10)

    # Java: while (count > 0) { System.out.println("倒计时: " + count); count--; }
    # Python: 不需要括号，用缩进
    count = 5
    while count > 0:
        print(f"倒计时: {count}")
        count -= 1  # Python 没有 count-- 语法
    print("发射！")

    # 注意：Python 没有 do-while 循环
    # Java: do { ... } while (condition);
    # Python 替代方案：while True + break
    # while True:
    #     user_input = input("请输入（q 退出）: ")
    #     if user_input == "q":
    #         break
    print()


def demo_match_case():
    """match-case 模式匹配（Python 3.10+）"""
    print("=" * 10, "match-case 模式匹配（Python 3.10+）", "=" * 10)

    # 检查 Python 版本
    if sys.version_info < (3, 10):
        print(f"当前 Python 版本 {sys.version} 不支持 match-case（需要 3.10+）")
        print("跳过 match-case 演示")
        print()
        return

    # --- 基本值匹配 ---
    # Java: switch (statusCode) { case 200: ... break; case 404: ... break; }
    # Python: match-case 不需要 break，不会 fall-through
    status_codes = [200, 404, 500, 302]
    for code in status_codes:
        match code:
            case 200:
                desc = "OK"
            case 404:
                desc = "Not Found"
            case 500:
                desc = "Server Error"
            case _:  # _ 是通配符，类似 Java 的 default
                desc = f"Unknown status: {code}"
        print(f"{code} -> {desc}")

    # --- 结构化模式匹配（Java switch 做不到！）---
    # Python match-case 可以匹配数据结构并解构
    print("--- 结构化模式匹配 ---")
    points = [(0, 0), (3, 0), (0, 5), (2, 7)]
    for point in points:
        match point:
            case (0, 0):
                desc = "原点"
            case (x, 0):
                desc = f"X 轴上，x={x}"
            case (0, y):
                desc = f"Y 轴上，y={y}"
            case (x, y):
                desc = f"点 ({x}, {y})"
        print(f"{point} -> {desc}")
    print()


def demo_break_continue_else():
    """break/continue/else"""
    print("=" * 10, "break/continue/else", "=" * 10)

    # --- break：提前退出循环 ---
    # Java 和 Python 的 break 用法基本一致
    print("--- break 示例 ---")
    fruits = ["apple", "banana", "cherry", "date"]
    for fruit in fruits:
        if fruit == "cherry":
            print(f"找到目标: {fruit}")
            break

    # --- continue：跳过当前迭代 ---
    # Java 和 Python 的 continue 用法基本一致
    print("--- continue 示例 ---")
    for i in range(1, 10):
        if i % 2 == 0:
            continue  # 跳过偶数
        print(f"奇数: {i}")

    # --- 循环 else：Java 中完全没有的特性！---
    # else 块在循环正常结束（没有被 break 中断）时执行
    # 常用于"搜索"场景：找到了就 break，没找到就执行 else
    print("--- 循环 else 示例 ---")

    # 场景 1：循环正常结束，else 执行
    numbers = [1, 3, 5, 7, 9]
    for n in numbers:
        if n < 0:
            print(f"找到负数: {n}")
            break
    else:
        # 循环没有被 break 中断，说明没找到负数
        print("在列表中未找到负数（循环正常结束）")

    # 场景 2：循环被 break 中断，else 不执行
    numbers_with_neg = [1, 3, -1, 7, 9]
    for n in numbers_with_neg:
        if n < 0:
            print(f"在列表中找到负数: {n}（循环被 break 中断，else 不执行）")
            break
    else:
        print("未找到负数")  # 不会执行
    print()


def demo_ternary_expression():
    """三元表达式（条件表达式）"""
    print("=" * 10, "三元表达式（条件表达式）", "=" * 10)

    # Java: String result = (score >= 60) ? "及格" : "不及格";
    # Python: result = "及格" if score >= 60 else "不及格"
    # 注意语序不同！Python 是 "值A if 条件 else 值B"
    score = 85
    result = "及格" if score >= 60 else "不及格"
    print(f"{score} 分 -> {result}")

    age = 15
    status = "成年" if age >= 18 else "未成年"
    print(f"{age} 岁 -> {status}")

    # 三元表达式可以嵌套，但不推荐（可读性差）
    # grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D"
    print()


def main():
    """主函数：依次演示所有控制流特性"""
    demo_if_elif_else()
    demo_for_loop()
    demo_while_loop()
    demo_match_case()
    demo_break_continue_else()
    demo_ternary_expression()


if __name__ == "__main__":
    main()
