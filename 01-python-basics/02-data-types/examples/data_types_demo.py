#!/usr/bin/env python3
"""
Python 数据类型演示

模块: 01-Python 基础
知识点: 数据类型与变量
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python data_types_demo.py

描述:
    演示 Python 所有内置数据类型的创建、操作和类型检查，
    包括 int、float、str、bool、list、dict、tuple、set、None，
    以及 type()、isinstance() 类型检查和类型转换。
"""


def demo_numeric_types():
    """数值类型演示：int、float、bool"""
    print("=" * 10, "数值类型", "=" * 10)

    # int — 整数（无大小限制，不像 Java 的 int/long 有范围限制）
    x = 42
    print(f"整数: {x}, 类型: {type(x)}")

    # Python 整数可以任意大，不会溢出
    big = 999999999999999999999
    print(f"大整数: {big}, 类型: {type(big)}")

    # float — 浮点数（双精度，等同于 Java 的 double）
    pi = 3.14
    print(f"浮点数: {pi}, 类型: {type(pi)}")

    # bool — 布尔值（注意首字母大写：True/False，不是 Java 的 true/false）
    flag = True
    print(f"布尔值: {flag}, 类型: {type(flag)}")

    # Python 中 bool 是 int 的子类！True == 1, False == 0
    print(f"布尔值是 int 的子类: {issubclass(bool, int)}")
    print()


def demo_string_type():
    """字符串类型演示"""
    print("=" * 10, "字符串类型", "=" * 10)

    # str — 字符串（不可变，Unicode 编码）
    s = "Hello, Python!"
    print(f"字符串: {s}, 类型: {type(s)}")
    print(f"长度: {len(s)}")

    # 常用字符串方法
    print(f"大写: {s.upper()}")
    print(f"切片 [0:5]: {s[0:5]}")  # 类似 Java 的 substring(0, 5)

    # f-string 格式化（Python 3.6+，推荐方式）
    name, age = "Alice", 25
    print(f"f-string: 我叫 {name}，今年 {age} 岁")
    print()


def demo_list_type():
    """列表类型演示"""
    print("=" * 10, "列表（list）", "=" * 10)

    # list — 有序、可变、可重复、可混合类型
    # 类似 Java 的 ArrayList<Object>
    mixed_list = [1, "hello", 3.14, True]
    print(f"列表: {mixed_list}, 类型: {type(mixed_list)}")
    print(f"第一个元素: {mixed_list[0]}")

    # 常用操作
    mixed_list.append("new")
    print(f"追加后: {mixed_list}")
    print("列表可以混合类型（Java ArrayList<Object> 类似）")
    print()


def demo_dict_type():
    """字典类型演示"""
    print("=" * 10, "字典（dict）", "=" * 10)

    # dict — 键值对映射，类似 Java 的 HashMap
    # Python 3.7+ 保持插入顺序（Java LinkedHashMap 类似）
    person = {"name": "Alice", "age": 25, "city": "北京"}
    print(f"字典: {person}, 类型: {type(person)}")
    print(f"name = {person['name']}")

    # 遍历字典
    items = []
    for key, value in person.items():
        items.append(f"{key} -> {value}")
    print(f"遍历: {', '.join(items)}")
    print()


def demo_tuple_type():
    """元组类型演示"""
    print("=" * 10, "元组（tuple）", "=" * 10)

    # tuple — 有序、不可变、可重复
    # 类似 Java 中的不可变数组，常用于函数返回多个值
    t = (1, 2, 3, "hello")
    print(f"元组: {t}, 类型: {type(t)}")
    print("元组不可变，类似 Java 的不可变数组")
    print()


def demo_set_type():
    """集合类型演示"""
    print("=" * 10, "集合（set）", "=" * 10)

    # set — 无序、不重复，类似 Java 的 HashSet
    s1 = {1, 2, 3, 4, 5}
    s2 = {3, 4, 5, 6, 7}
    print(f"集合: {s1}, 类型: {type(s1)}")

    # 集合运算
    print(f"交集: {s1 & s2}")
    print(f"并集: {s1 | s2}")
    print()


def demo_none_type():
    """None 类型演示"""
    print("=" * 10, "None 类型", "=" * 10)

    # None — Python 的空值，类似 Java 的 null
    x = None
    print(f"None 值: {x}, 类型: {type(x)}")

    # 判断 None 用 is（不要用 ==）
    print(f"判断 None 用 is: {x is None}")
    print()


def demo_type_checking_and_conversion():
    """类型检查与转换演示"""
    print("=" * 10, "类型检查与转换", "=" * 10)

    # type() — 获取精确类型
    print(f"type(42) = {type(42)}")

    # isinstance() — 检查是否为某类型（支持继承关系）
    print(f"isinstance(42, int) = {isinstance(42, int)}")
    print(f"isinstance(True, int) = {isinstance(True, int)}（bool 是 int 的子类！）")

    # 类型转换
    print(f"int('123') = {int('123')}")
    print(f"str(456) = '{str(456)}'")
    print(f"list('abc') = {list('abc')}")
    print()


def main():
    """主函数：依次演示所有数据类型"""
    demo_numeric_types()
    demo_string_type()
    demo_list_type()
    demo_dict_type()
    demo_tuple_type()
    demo_set_type()
    demo_none_type()
    demo_type_checking_and_conversion()


if __name__ == "__main__":
    main()
