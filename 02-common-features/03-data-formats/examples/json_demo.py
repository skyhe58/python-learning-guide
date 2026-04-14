#!/usr/bin/env python3
"""
JSON 数据处理演示

模块: 02-常用功能
知识点: 数据格式处理
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python json_demo.py

描述:
    演示 Python json 模块的核心功能：
    1. JSON 解析（loads）— 字符串转 Python 对象
    2. JSON 生成（dumps）— Python 对象转字符串
    3. JSON 文件读写（load/dump）
    4. 自定义序列化（处理 datetime 等类型）
    5. 格式化输出与中文支持
"""

import json
import tempfile
import os
from datetime import datetime, date


# ============================================================
# 1. JSON 解析（loads）
# ============================================================

def demo_loads():
    """json.loads：JSON 字符串 -> Python 对象"""
    print("=" * 10, "JSON 解析 (loads)", "=" * 10)

    # 基本解析
    # 类似 Java: new ObjectMapper().readValue(json, Map.class)
    json_str = '{"name": "Alice", "age": 30, "skills": ["Python", "Java"]}'
    data = json.loads(json_str)
    print(f"解析结果: {data}")
    print(f"类型: {type(data)}")  # <class 'dict'>
    print(f"姓名: {data['name']}, 技能: {data['skills']}")

    # JSON 类型映射
    type_demo = '{"str": "hello", "int": 42, "float": 3.14, "bool": true, "null": null}'
    parsed = json.loads(type_demo)
    for key, value in parsed.items():
        print(f"  {key}: {value!r} ({type(value).__name__})")

    print()


# ============================================================
# 2. JSON 生成（dumps）
# ============================================================

def demo_dumps():
    """json.dumps：Python 对象 -> JSON 字符串"""
    print("=" * 10, "JSON 生成 (dumps)", "=" * 10)

    data = {
        "name": "张三",
        "age": 25,
        "hobbies": ["编程", "阅读"],
        "address": {"city": "北京", "district": "海淀"},
    }

    # 基本序列化
    json_str = json.dumps(data)
    print(f"默认输出: {json_str}")

    # 格式化输出（缩进）
    pretty = json.dumps(data, indent=2, ensure_ascii=False)
    print(f"格式化输出:\n{pretty}")

    # 排序键名
    sorted_json = json.dumps(data, sort_keys=True, ensure_ascii=False)
    print(f"排序键名: {sorted_json}")

    # 紧凑输出（去除空格）
    compact = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    print(f"紧凑输出: {compact}")

    print()


# ============================================================
# 3. JSON 文件读写
# ============================================================

def demo_file_io():
    """json.load/dump：JSON 文件读写"""
    print("=" * 10, "JSON 文件读写", "=" * 10)

    data = {
        "project": "Python 学习知识库",
        "version": "1.0",
        "modules": ["基础", "常用功能", "小工具"],
    }

    # 写入 JSON 文件
    tmp_file = os.path.join(tempfile.gettempdir(), "demo_config.json")
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"写入文件: {tmp_file}")

    # 读取 JSON 文件
    with open(tmp_file, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    print(f"读取结果: {loaded}")
    print(f"数据一致: {loaded == data}")

    # 清理临时文件
    os.remove(tmp_file)

    print()


# ============================================================
# 4. 自定义序列化
# ============================================================

def demo_custom_serializer():
    """处理 json 默认不支持的类型（datetime、set 等）"""
    print("=" * 10, "自定义序列化", "=" * 10)

    # --- 方式 1：自定义 JSONEncoder ---
    class CustomEncoder(json.JSONEncoder):
        """扩展 JSON 编码器，支持 datetime 和 set"""
        def default(self, obj):
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()
            if isinstance(obj, set):
                return sorted(list(obj))
            return super().default(obj)

    data = {
        "event": "Python 学习",
        "date": date(2025, 7, 15),
        "created_at": datetime(2025, 7, 15, 14, 30, 0),
        "tags": {"入门", "实战", "基础"},
    }

    result = json.dumps(data, cls=CustomEncoder, ensure_ascii=False, indent=2)
    print(f"自定义编码器:\n{result}")

    # --- 方式 2：使用 default 参数 ---
    def custom_default(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, set):
            return sorted(list(obj))
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    result2 = json.dumps(data, default=custom_default, ensure_ascii=False)
    print(f"\ndefault 参数: {result2}")

    print()


# ============================================================
# 5. 实用技巧
# ============================================================

def demo_tips():
    """JSON 处理实用技巧"""
    print("=" * 10, "实用技巧", "=" * 10)

    # --- 安全解析（处理无效 JSON）---
    print("--- 安全解析 ---")
    invalid_inputs = ['{"valid": true}', "not json", "", "null"]
    for text in invalid_inputs:
        try:
            result = json.loads(text)
            print(f"  '{text}' -> {result}")
        except json.JSONDecodeError as e:
            print(f"  '{text}' -> 解析失败: {e.msg}")

    # --- 嵌套数据访问 ---
    print("--- 嵌套数据安全访问 ---")
    config = {"database": {"host": "localhost", "port": 5432}}

    # 安全访问嵌套键（避免 KeyError）
    host = config.get("database", {}).get("host", "unknown")
    missing = config.get("cache", {}).get("host", "未配置")
    print(f"  数据库主机: {host}")
    print(f"  缓存主机: {missing}")

    print()


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数：依次演示所有 JSON 处理知识点"""
    demo_loads()
    demo_dumps()
    demo_file_io()
    demo_custom_serializer()
    demo_tips()


if __name__ == "__main__":
    main()
