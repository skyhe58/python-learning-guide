#!/usr/bin/env python3
"""
YAML 数据处理演示

模块: 02-常用功能
知识点: 数据格式处理
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    pip install pyyaml
    python yaml_demo.py

描述:
    演示 PyYAML 库的核心功能：
    1. YAML 解析（safe_load）— 字符串转 Python 对象
    2. YAML 生成（dump）— Python 对象转字符串
    3. YAML 文件读写
    4. 多文档处理（safe_load_all）
    5. YAML 特有功能（多行文本、锚点引用等）
"""

import tempfile
import os

try:
    import yaml
except ImportError:
    print("请先安装 PyYAML: pip install pyyaml")
    exit(1)


# ============================================================
# 1. YAML 解析（safe_load）
# ============================================================

def demo_safe_load():
    """yaml.safe_load：YAML 字符串 -> Python 对象"""
    print("=" * 10, "YAML 解析 (safe_load)", "=" * 10)

    # 基本解析
    yaml_text = """
name: Alice
age: 30
skills:
  - Python
  - Java
  - Docker
address:
  city: 北京
  district: 海淀
active: true
score: 95.5
"""
    data = yaml.safe_load(yaml_text)
    print(f"解析结果: {data}")
    print(f"类型: {type(data)}")
    print(f"姓名: {data['name']}, 技能: {data['skills']}")

    # YAML 类型自动推断
    type_demo = """
string: hello
integer: 42
float: 3.14
boolean: true
null_value: null
date: 2025-07-15
list: [1, 2, 3]
"""
    parsed = yaml.safe_load(type_demo)
    print("\nYAML 类型推断:")
    for key, value in parsed.items():
        print(f"  {key}: {value!r} ({type(value).__name__})")

    print()


# ============================================================
# 2. YAML 生成（dump）
# ============================================================

def demo_dump():
    """yaml.dump：Python 对象 -> YAML 字符串"""
    print("=" * 10, "YAML 生成 (dump)", "=" * 10)

    data = {
        "project": "Python 学习知识库",
        "version": "1.0",
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "mydb",
        },
        "features": ["正则表达式", "日期处理", "数据格式"],
    }

    # 默认输出
    result = yaml.dump(data, allow_unicode=True)
    print(f"默认输出:\n{result}")

    # 自定义输出格式
    result2 = yaml.dump(
        data,
        allow_unicode=True,
        default_flow_style=False,  # 块样式（非行内样式）
        sort_keys=False,           # 保持键的原始顺序
        indent=2,
    )
    print(f"自定义格式:\n{result2}")

    print()


# ============================================================
# 3. YAML 文件读写
# ============================================================

def demo_file_io():
    """YAML 文件读写"""
    print("=" * 10, "YAML 文件读写", "=" * 10)

    config = {
        "server": {
            "host": "0.0.0.0",
            "port": 8080,
            "debug": False,
        },
        "logging": {
            "level": "INFO",
            "file": "app.log",
        },
    }

    # 写入 YAML 文件
    tmp_file = os.path.join(tempfile.gettempdir(), "demo_config.yaml")
    with open(tmp_file, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
    print(f"写入文件: {tmp_file}")

    # 读取 YAML 文件
    with open(tmp_file, "r", encoding="utf-8") as f:
        loaded = yaml.safe_load(f)
    print(f"读取结果: {loaded}")
    print(f"数据一致: {loaded == config}")

    # 清理临时文件
    os.remove(tmp_file)

    print()


# ============================================================
# 4. 多文档处理
# ============================================================

def demo_multi_document():
    """YAML 多文档处理（用 --- 分隔）"""
    print("=" * 10, "多文档处理", "=" * 10)

    # YAML 支持在一个文件中包含多个文档，用 --- 分隔
    # 常见于 Kubernetes 配置文件
    multi_doc = """
---
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
---
kind: Service
metadata:
  name: web-service
spec:
  port: 80
---
kind: ConfigMap
metadata:
  name: app-config
data:
  key: value
"""

    # safe_load_all 返回生成器，逐个解析文档
    docs = list(yaml.safe_load_all(multi_doc))
    print(f"文档数量: {len(docs)}")
    for i, doc in enumerate(docs):
        print(f"  文档 {i + 1}: kind={doc['kind']}, name={doc['metadata']['name']}")

    print()


# ============================================================
# 5. YAML 特有功能
# ============================================================

def demo_yaml_features():
    """YAML 特有功能：多行文本、锚点引用"""
    print("=" * 10, "YAML 特有功能", "=" * 10)

    # --- 多行文本 ---
    print("--- 多行文本 ---")
    multiline_yaml = """
# | 保留换行符（literal block）
description_literal: |
  这是第一行
  这是第二行
  这是第三行

# > 折叠换行符为空格（folded block）
description_folded: >
  这是一段很长的文本
  会被折叠成一行
  中间用空格连接
"""
    data = yaml.safe_load(multiline_yaml)
    print(f"literal (|): {data['description_literal']!r}")
    print(f"folded  (>): {data['description_folded']!r}")

    # --- 锚点和引用 ---
    print("--- 锚点和引用 ---")
    anchor_yaml = """
defaults: &defaults
  timeout: 30
  retries: 3
  log_level: INFO

development:
  <<: *defaults
  debug: true

production:
  <<: *defaults
  log_level: WARNING
  retries: 5
"""
    config = yaml.safe_load(anchor_yaml)
    print(f"development: {config['development']}")
    print(f"production:  {config['production']}")

    print()


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数：依次演示所有 YAML 处理知识点"""
    demo_safe_load()
    demo_dump()
    demo_file_io()
    demo_multi_document()
    demo_yaml_features()


if __name__ == "__main__":
    main()
