#!/usr/bin/env python3
"""
数据格式往返一致性验证

模块: 02-常用功能
知识点: 数据格式处理
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    pip install pyyaml
    python roundtrip_test.py

描述:
    验证 parse(format(data)) == data 的往返一致性（roundtrip consistency）。
    即：将 Python 数据序列化为 JSON/YAML 字符串后，再反序列化回来，
    数据应与原始数据完全一致。

    测试覆盖：
    1. JSON 往返一致性（基本类型、嵌套结构）
    2. YAML 往返一致性（基本类型、嵌套结构）
    3. 边界情况（空数据、深层嵌套、特殊字符）
"""

import json

try:
    import yaml
except ImportError:
    yaml = None
    print("提示: 未安装 PyYAML，YAML 测试将跳过 (pip install pyyaml)")


# ============================================================
# 测试数据
# ============================================================

# 基本类型测试数据
BASIC_TEST_CASES = [
    ("字符串", "Hello, 世界!"),
    ("整数", 42),
    ("浮点数", 3.14),
    ("布尔值 True", True),
    ("布尔值 False", False),
    ("None/null", None),
    ("空字符串", ""),
    ("零", 0),
    ("负数", -100),
    ("大数", 10**18),
]

# 复合类型测试数据
COMPLEX_TEST_CASES = [
    ("简单列表", [1, 2, 3, "四", "五"]),
    ("简单字典", {"name": "张三", "age": 30}),
    ("空列表", []),
    ("空字典", {}),
    ("嵌套字典", {
        "user": {
            "name": "Alice",
            "profile": {
                "city": "北京",
                "hobbies": ["编程", "阅读"],
            },
        },
    }),
    ("混合列表", [1, "two", 3.0, True, None, {"key": "value"}]),
    ("深层嵌套", {"a": {"b": {"c": {"d": {"e": "深层值"}}}}}),
    ("特殊字符", {"text": 'He said "hello" & <goodbye>'}),
    ("Unicode", {"emoji": "你好世界", "mixed": "abc中文123"}),
    ("数字键（字符串）", {"1": "one", "2": "two", "100": "hundred"}),
]


# ============================================================
# JSON 往返测试
# ============================================================

def test_json_roundtrip():
    """验证 JSON 的往返一致性：json.loads(json.dumps(data)) == data"""
    print("=" * 10, "JSON 往返一致性", "=" * 10)

    passed = 0
    failed = 0

    all_cases = BASIC_TEST_CASES + COMPLEX_TEST_CASES
    for name, data in all_cases:
        try:
            # 序列化 -> 反序列化
            json_str = json.dumps(data, ensure_ascii=False)
            restored = json.loads(json_str)

            if restored == data:
                passed += 1
                status = "✓"
            else:
                failed += 1
                status = "✗"
                print(f"  {status} {name}: 原始={data!r}, 还原={restored!r}")
        except Exception as e:
            failed += 1
            print(f"  ✗ {name}: 异常 - {e}")

    print(f"\nJSON 测试结果: {passed} 通过, {failed} 失败, 共 {passed + failed} 项")
    if failed == 0:
        print("  所有 JSON 往返测试通过! ✓")

    print()
    return failed == 0


# ============================================================
# YAML 往返测试
# ============================================================

def test_yaml_roundtrip():
    """验证 YAML 的往返一致性：yaml.safe_load(yaml.dump(data)) == data"""
    print("=" * 10, "YAML 往返一致性", "=" * 10)

    if yaml is None:
        print("  跳过: PyYAML 未安装")
        print()
        return True

    passed = 0
    failed = 0

    all_cases = BASIC_TEST_CASES + COMPLEX_TEST_CASES
    for name, data in all_cases:
        try:
            # 序列化 -> 反序列化
            yaml_str = yaml.dump(data, allow_unicode=True)
            restored = yaml.safe_load(yaml_str)

            if restored == data:
                passed += 1
                status = "✓"
            else:
                failed += 1
                status = "✗"
                print(f"  {status} {name}: 原始={data!r}, 还原={restored!r}")
        except Exception as e:
            failed += 1
            print(f"  ✗ {name}: 异常 - {e}")

    print(f"\nYAML 测试结果: {passed} 通过, {failed} 失败, 共 {passed + failed} 项")
    if failed == 0:
        print("  所有 YAML 往返测试通过! ✓")

    print()
    return failed == 0


# ============================================================
# 交叉格式测试
# ============================================================

def test_cross_format():
    """验证 JSON 和 YAML 对同一数据的解析结果一致"""
    print("=" * 10, "JSON/YAML 交叉一致性", "=" * 10)

    if yaml is None:
        print("  跳过: PyYAML 未安装")
        print()
        return True

    passed = 0
    failed = 0

    # 只测试两种格式都支持的数据类型
    cross_cases = [
        ("字符串", "hello"),
        ("整数", 42),
        ("布尔值", True),
        ("None", None),
        ("列表", [1, 2, 3]),
        ("字典", {"a": 1, "b": 2}),
        ("嵌套结构", {"users": [{"name": "Alice"}, {"name": "Bob"}]}),
    ]

    for name, data in cross_cases:
        try:
            # JSON 往返
            json_result = json.loads(json.dumps(data))
            # YAML 往返
            yaml_result = yaml.safe_load(yaml.dump(data))

            if json_result == yaml_result == data:
                passed += 1
            else:
                failed += 1
                print(f"  ✗ {name}: JSON={json_result!r}, YAML={yaml_result!r}")
        except Exception as e:
            failed += 1
            print(f"  ✗ {name}: 异常 - {e}")

    print(f"\n交叉测试结果: {passed} 通过, {failed} 失败, 共 {passed + failed} 项")
    if failed == 0:
        print("  所有交叉一致性测试通过! ✓")

    print()
    return failed == 0


# ============================================================
# 主函数
# ============================================================

def main():
    """运行所有往返一致性测试"""
    print("数据格式往返一致性验证")
    print("=" * 50)
    print()

    results = []
    results.append(("JSON 往返", test_json_roundtrip()))
    results.append(("YAML 往返", test_yaml_roundtrip()))
    results.append(("交叉一致性", test_cross_format()))

    # 汇总结果
    print("=" * 50)
    print("测试汇总:")
    all_passed = True
    for name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False

    print()
    if all_passed:
        print("所有往返一致性测试通过! ✓")
    else:
        print("部分测试失败，请检查上方详细信息。")


if __name__ == "__main__":
    main()
