#!/usr/bin/env python3
"""
Python 模块与包管理完整演示

模块: 01-Python 基础
知识点: 模块与包管理
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python modules_demo.py

描述:
    演示 Python 模块与包管理的核心知识：
    1. import 的各种方式（vs Java import）
    2. 标准库模块使用（os, sys, json, pathlib, datetime）
    3. __name__ == "__main__" 的作用
    4. 模块搜索路径 sys.path
    5. dir() 查看模块内容
    6. 创建和使用自定义模块的说明
    每个部分都在注释中与 Java 进行对比。
"""

import os
import sys
import json
import math
from pathlib import Path
from datetime import datetime, timedelta


# ============================================================
# 1. import 的各种方式
# ============================================================

def demo_import_styles():
    """import 的各种方式"""
    print("=" * 10, "import 的各种方式", "=" * 10)

    # Java:
    #   import java.io.File;                    // 导入单个类
    #   import java.util.*;                     // 通配符导入
    #   import static java.lang.Math.PI;        // 静态导入
    #   // Java 不支持别名导入
    #
    # Python: 更灵活，支持多种导入方式和别名

    # --- 方式 1: import 模块 ---
    print("--- import 模块 ---")
    # import os          # 已在文件顶部导入
    # import sys         # 已在文件顶部导入
    # 使用时需要加模块名前缀：os.getcwd()
    # 类似 Java 中不用 import，直接写 java.io.File
    print(f"当前工作目录: {os.getcwd()}")
    print(f"操作系统: {os.name}")

    # --- 方式 2: from 模块 import 对象 ---
    print("--- from 模块 import 对象 ---")
    # from datetime import datetime, timedelta  # 已在文件顶部导入
    # 类似 Java: import java.util.Date;
    # 但 Python 可以导入函数、变量等任何对象，Java 只能导入类
    now = datetime.now()
    one_week_later = now + timedelta(weeks=1)
    print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"一周后: {one_week_later.strftime('%Y-%m-%d %H:%M:%S')}")

    # --- 方式 3: as 别名 ---
    print("--- as 别名 ---")
    # Java 不支持 import 别名，Python 可以用 as 设置别名
    # 常见约定：import numpy as np, import pandas as pd
    from pathlib import Path as P  # 别名导入
    current = P(".")
    print(f"当前目录: {current.resolve()}")
    py_files = list(current.glob("*.py"))
    print(f"目录下的 .py 文件: {[f.name for f in py_files]}")

    # --- 不推荐的方式: from module import * ---
    # from os import *  # 不推荐！会污染命名空间
    # Java 的 import java.util.* 只导入类名，相对安全
    # Python 的 import * 会导入所有公开名称，可能覆盖已有变量

    print()


# ============================================================
# 2. 标准库模块使用
# ============================================================

def demo_stdlib():
    """标准库模块使用"""
    print("=" * 10, "标准库模块使用", "=" * 10)

    # Java 标准库通过 java.* 和 javax.* 包组织
    # Python 标准库（"batteries included"）直接 import 即可
    # Python 标准库比 Java 更"开箱即用"，很多功能不需要第三方库

    # --- os 模块（类似 Java java.io.File + System.getenv）---
    print("--- os 模块 ---")
    # Java: System.getProperty("user.dir"), System.getenv("HOME")
    print(f"当前目录: {os.getcwd()}")
    print(f"环境变量 HOME: {os.environ.get('HOME', os.environ.get('USERPROFILE', '未设置'))}")

    # --- sys 模块（类似 Java System 类）---
    print("--- sys 模块 ---")
    # Java: System.getProperty("java.version"), System.getProperty("os.name")
    print(f"Python 版本: {sys.version.split()[0]}")
    print(f"平台: {sys.platform}")

    # --- json 模块（类似 Java Jackson/Gson）---
    print("--- json 模块 ---")
    # Java: 需要第三方库（Jackson、Gson、org.json）
    # Python: 标准库自带 json 模块，无需额外安装
    data = {"name": "张三", "age": 25, "skills": ["Python", "Java"]}
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    print(f"JSON 字符串: {json.dumps(data, ensure_ascii=False)}")
    parsed = json.loads(json_str)
    print(f"解析回来: {parsed}")

    # --- pathlib 模块（类似 Java java.nio.file.Path，Python 3.4+）---
    print("--- pathlib 模块 ---")
    # Java: Path path = Paths.get("file.txt"); path.getParent();
    # Python: pathlib 是面向对象的路径操作，比 os.path 更现代
    current_file = Path(__file__).resolve()
    print(f"当前文件: {current_file}")
    print(f"父目录: {current_file.parent}")
    print(f"文件是否存在: {current_file.exists()}")

    # --- datetime 模块（类似 Java java.time 包）---
    print("--- datetime 模块 ---")
    # Java 8+: LocalDateTime.now(), DateTimeFormatter
    # Python: datetime 模块功能类似，但 API 更简洁
    now = datetime.now()
    print(f"现在: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"格式化: {now.strftime('%Y年%m月%d日 %H:%M:%S')}")

    print()


# ============================================================
# 3. __name__ == "__main__"
# ============================================================

def demo_name_main():
    """__name__ == '__main__' 的作用"""
    print("=" * 10, '__name__ == "__main__"', "=" * 10)

    # Java:
    #   public static void main(String[] args) { }
    #   // Java 的 main 方法是程序入口，由 JVM 调用
    #
    # Python:
    #   if __name__ == "__main__":
    #       main()
    #   // 这个模式让文件既可以作为脚本直接运行，也可以作为模块被导入
    #   // 直接运行时 __name__ 为 "__main__"
    #   // 被 import 时 __name__ 为模块名（如 "modules_demo"）

    print(f"当前模块的 __name__: {__name__}")
    print("说明: 直接运行此脚本时 __name__ 为 '__main__'")
    print("说明: 被其他模块 import 时 __name__ 为模块名")

    # 典型用法示例（伪代码）：
    # ─────────────────────────────
    # # my_utils.py
    # def add(a, b):
    #     return a + b
    #
    # def test_add():
    #     assert add(1, 2) == 3
    #     print("测试通过！")
    #
    # if __name__ == "__main__":
    #     # 直接运行 my_utils.py 时执行测试
    #     test_add()
    #
    # # 被其他文件 import 时，test_add() 不会自动执行
    # # other.py
    # from my_utils import add  # 只导入 add 函数，不会运行测试
    # ─────────────────────────────

    print()


# ============================================================
# 4. 模块搜索路径 sys.path
# ============================================================

def demo_sys_path():
    """模块搜索路径 sys.path"""
    print("=" * 10, "模块搜索路径 sys.path", "=" * 10)

    # Java:
    #   类路径（classpath）决定 JVM 在哪里查找类
    #   通过 -cp 参数或 CLASSPATH 环境变量设置
    #
    # Python:
    #   sys.path 是一个列表，Python 按顺序在这些路径中查找模块
    #   搜索顺序：
    #   1. 当前脚本所在目录（或空字符串表示当前工作目录）
    #   2. PYTHONPATH 环境变量中的路径
    #   3. 标准库路径
    #   4. site-packages（第三方包安装目录）

    print("Python 模块搜索路径（前 5 个）:")
    for i, path in enumerate(sys.path[:5], 1):
        print(f"  {i}. {path or '（当前目录）'}")
    if len(sys.path) > 5:
        print(f"  ... 共 {len(sys.path)} 个路径")

    # 动态添加搜索路径（Java 中需要修改 classpath）
    # sys.path.insert(0, "/path/to/my/modules")
    # 添加后就可以 import 该路径下的模块了

    print()


# ============================================================
# 5. dir() 查看模块内容
# ============================================================

def demo_dir():
    """dir() 查看模块内容"""
    print("=" * 10, "dir() 查看模块内容", "=" * 10)

    # Java:
    #   没有直接等价物，需要用反射（Reflection）查看类的方法和字段
    #   Class<?> cls = Math.class;
    #   Method[] methods = cls.getMethods();
    #
    # Python:
    #   dir(module) 返回模块中所有名称的列表
    #   比 Java 反射简单得多

    # --- 查看 math 模块 ---
    print("--- math 模块的常用属性 ---")
    print(f"常量: pi={math.pi}, e={math.e}")

    # 过滤掉双下划线开头的内部属性，只看公开的函数和常量
    public_attrs = [name for name in dir(math) if not name.startswith("_")]
    print(f"函数: {public_attrs[:10]}...")

    # --- 查看任意对象的属性 ---
    print("--- 查看对象的所有属性 ---")
    text = "hello"
    str_methods = [m for m in dir(text) if not m.startswith("_")]
    print(f"字符串的方法数量: {len(dir(text))}")
    print(f"常用字符串方法: {str_methods[:10]}...")

    print()


# ============================================================
# 6. 自定义模块说明
# ============================================================

def demo_custom_module():
    """自定义模块的创建和使用说明"""
    print("=" * 10, "自定义模块说明", "=" * 10)

    # Java:
    #   1. 创建 .java 文件，声明 package
    #   2. 编译为 .class 文件
    #   3. 确保在 classpath 中
    #   4. import com.example.MyClass;
    #
    # Python:
    #   1. 创建 .py 文件（这就是一个模块了！）
    #   2. 不需要编译
    #   3. 确保在 sys.path 中（同目录下自动可用）
    #   4. import my_module

    print("--- 创建自定义模块 ---")
    print("1. 创建 my_utils.py 文件，定义函数和类")
    print("2. 在同目录下的其他文件中 import my_utils")
    print("3. 使用 my_utils.function_name() 调用")

    # 示例：假设有一个 my_utils.py
    # ─────────────────────────────
    # # my_utils.py
    # """我的工具模块"""
    #
    # def greet(name):
    #     return f"你好, {name}!"
    #
    # class Calculator:
    #     def add(self, a, b):
    #         return a + b
    #
    # PI = 3.14159
    # ─────────────────────────────
    #
    # # main.py（同目录下）
    # import my_utils
    # print(my_utils.greet("张三"))
    # calc = my_utils.Calculator()
    # print(calc.add(1, 2))
    # print(my_utils.PI)
    #
    # # 或者
    # from my_utils import greet, Calculator, PI
    # print(greet("张三"))

    print()
    print("--- 创建包 ---")
    print("1. 创建目录 mypackage/")
    print("2. 添加 __init__.py（可以为空）")
    print("3. 添加模块文件 mypackage/utils.py")
    print("4. 使用 from mypackage import utils")

    # 包结构示例：
    # ─────────────────────────────
    # mypackage/
    # ├── __init__.py        # 包初始化，可以定义 __all__ 控制 import *
    # ├── utils.py           # from mypackage.utils import helper
    # ├── models.py          # from mypackage.models import User
    # └── sub_package/       # 子包
    #     ├── __init__.py
    #     └── helpers.py     # from mypackage.sub_package.helpers import func
    # ─────────────────────────────
    #
    # __init__.py 的作用：
    # 1. 标识目录为 Python 包
    # 2. 包被导入时自动执行
    # 3. 可以定义 __all__ 列表，控制 from package import * 的行为
    # 4. 可以在包级别导入常用对象，简化外部使用
    #
    # 示例 __init__.py:
    # from .utils import helper
    # from .models import User
    # __all__ = ["helper", "User"]

    print()


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数：依次演示所有模块与包管理知识点"""
    demo_import_styles()
    demo_stdlib()
    demo_name_main()
    demo_sys_path()
    demo_dir()
    demo_custom_module()


if __name__ == "__main__":
    main()
