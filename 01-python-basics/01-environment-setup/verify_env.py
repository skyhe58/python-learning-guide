#!/usr/bin/env python3
"""
Python 环境验证脚本

模块: 01-Python 基础
知识点: 环境搭建
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python verify_env.py

描述:
    逐项检查 Python 环境配置是否正确，包括 Python 版本、pip 可用性、
    常用标准库模块的安装状态，并输出清晰的状态信息。
"""

import sys
import importlib
import subprocess


# 需要检查的标准库模块列表
STANDARD_MODULES = [
    ("json", "JSON 数据处理"),
    ("os", "操作系统接口"),
    ("sys", "系统参数与函数"),
    ("pathlib", "面向对象的文件路径"),
    ("datetime", "日期时间处理"),
    ("re", "正则表达式"),
    ("collections", "容器数据类型"),
    ("typing", "类型提示"),
    ("unittest", "单元测试框架"),
    ("logging", "日志记录"),
    ("argparse", "命令行参数解析"),
    ("sqlite3", "SQLite 数据库接口"),
    ("csv", "CSV 文件读写"),
    ("math", "数学函数"),
    ("functools", "高阶函数工具"),
]

REQUIRED_PYTHON_VERSION = (3, 9)


def check_python_version() -> bool:
    """检查 Python 版本是否 >= 3.9"""
    version = sys.version_info
    if version >= REQUIRED_PYTHON_VERSION:
        print(f"  [PASS] Python 版本: {sys.version.split()[0]}")
        return True
    else:
        print(
            f"  [FAIL] Python 版本过低: {sys.version.split()[0]}"
            f" (需要 >= {REQUIRED_PYTHON_VERSION[0]}.{REQUIRED_PYTHON_VERSION[1]})"
        )
        return False


def check_pip() -> bool:
    """检查 pip 是否可用"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            pip_version = result.stdout.strip().split()[1]
            print(f"  [PASS] pip 可用: {pip_version}")
            return True
        else:
            print("  [FAIL] pip 不可用")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError, IndexError):
        print("  [FAIL] pip 不可用")
        return False


def check_module(module_name: str, description: str) -> bool:
    """检查指定模块是否可以导入"""
    try:
        importlib.import_module(module_name)
        print(f"  [PASS] {module_name:<15} -- {description}")
        return True
    except ImportError:
        print(f"  [FAIL] {module_name:<15} -- {description} (导入失败)")
        return False


def check_venv() -> bool:
    """检查是否在虚拟环境中运行"""
    in_venv = (
        hasattr(sys, "real_prefix")
        or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
    )
    if in_venv:
        print(f"  [PASS] 当前在虚拟环境中运行: {sys.prefix}")
    else:
        print("  [WARN] 当前未使用虚拟环境 (建议为每个项目创建独立虚拟环境)")
    return in_venv


def main():
    """主函数: 执行所有环境检查"""
    print("=" * 60)
    print("  Python 环境验证工具")
    print("=" * 60)

    passed = 0
    total = 0

    # 1. 检查 Python 版本
    print("\n[Python 版本检查]")
    total += 1
    if check_python_version():
        passed += 1

    # 2. 检查 pip
    print("\n[pip 包管理器检查]")
    total += 1
    if check_pip():
        passed += 1

    # 3. 检查虚拟环境
    print("\n[虚拟环境检查]")
    check_venv()  # 仅提示，不计入通过/失败

    # 4. 检查标准库模块
    print("\n[标准库模块检查]")
    for module_name, description in STANDARD_MODULES:
        total += 1
        if check_module(module_name, description):
            passed += 1

    # 输出汇总
    print("\n" + "=" * 60)
    if passed == total:
        print(f"  环境检查完成: {passed}/{total} 项通过 -- 一切就绪!")
    else:
        failed = total - passed
        print(f"  环境检查完成: {passed}/{total} 项通过, {failed} 项失败")
        print("  请根据上方提示修复失败项后重新运行本脚本。")
    print("=" * 60)


if __name__ == "__main__":
    main()
