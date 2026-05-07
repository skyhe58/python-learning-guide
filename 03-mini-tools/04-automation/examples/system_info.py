#!/usr/bin/env python3
"""
系统信息收集脚本

模块: 03-小工具开发
知识点: 自动化脚本
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python system_info.py [--output FILE] [--format text|json]

描述:
    收集当前系统的基本信息，包括操作系统、主机名、CPU、内存、
    磁盘使用情况和 Python 版本等。支持文本和 JSON 两种输出格式。
    仅使用 Python 标准库，无需第三方依赖。
"""

import argparse
import json
import os
import platform
import shutil
import sys
from datetime import datetime


def format_bytes(size_bytes: int) -> str:
    """将字节数格式化为可读的大小字符串。"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def collect_system_info() -> dict:
    """收集系统信息，返回字典。"""
    info = {}

    # 操作系统信息
    info["os"] = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
    }

    # 主机名
    info["hostname"] = platform.node()

    # Python 信息
    info["python"] = {
        "version": platform.python_version(),
        "implementation": platform.python_implementation(),
        "compiler": platform.python_compiler(),
        "executable": sys.executable,
    }

    # CPU 信息
    info["cpu"] = {
        "processor": platform.processor() or "未知",
        "cores_logical": os.cpu_count() or 0,
        "architecture": platform.machine(),
    }

    # 磁盘信息
    try:
        disk = shutil.disk_usage("/")
        info["disk"] = {
            "path": "/",
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent_used": round(disk.used / disk.total * 100, 1) if disk.total else 0,
        }
    except OSError:
        info["disk"] = {"error": "无法获取磁盘信息"}

    # 环境变量（部分）
    info["env"] = {
        "PATH_entries": len(os.environ.get("PATH", "").split(os.pathsep)),
        "HOME": os.environ.get("HOME") or os.environ.get("USERPROFILE", "未知"),
        "SHELL": os.environ.get("SHELL", "未知"),
        "LANG": os.environ.get("LANG", "未知"),
    }

    # 收集时间
    info["collected_at"] = datetime.now().isoformat()

    return info


def format_text(info: dict) -> str:
    """将系统信息格式化为文本。"""
    lines = ["=" * 40, "  系统信息报告", "=" * 40, ""]

    # 操作系统
    os_info = info["os"]
    lines.append(f"操作系统: {os_info['system']} {os_info['release']}")
    lines.append(f"平台: {os_info['platform']}")
    lines.append(f"主机名: {info['hostname']}")
    lines.append("")

    # Python
    py = info["python"]
    lines.append(f"Python 版本: {py['version']} ({py['implementation']})")
    lines.append(f"编译器: {py['compiler']}")
    lines.append(f"可执行文件: {py['executable']}")
    lines.append("")

    # CPU
    cpu = info["cpu"]
    lines.append(f"CPU: {cpu['processor']}")
    lines.append(f"逻辑核心数: {cpu['cores_logical']}")
    lines.append(f"架构: {cpu['architecture']}")
    lines.append("")

    # 磁盘
    disk = info["disk"]
    if "error" not in disk:
        lines.append(
            f"磁盘 {disk['path']}: "
            f"{format_bytes(disk['total'])} 总计, "
            f"{format_bytes(disk['used'])} 已用 ({disk['percent_used']}%), "
            f"{format_bytes(disk['free'])} 可用"
        )
    else:
        lines.append(f"磁盘: {disk['error']}")
    lines.append("")

    # 环境
    env = info["env"]
    lines.append(f"HOME: {env['HOME']}")
    lines.append(f"SHELL: {env['SHELL']}")
    lines.append(f"PATH 条目数: {env['PATH_entries']}")
    lines.append("")

    lines.append(f"收集时间: {info['collected_at']}")
    lines.append("=" * 40)

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(description="系统信息收集脚本")
    parser.add_argument("--output", help="输出文件路径（默认打印到终端）")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="输出格式（默认 text）",
    )
    return parser


def main():
    """主函数：收集系统信息并输出。"""
    parser = build_parser()
    args = parser.parse_args()

    info = collect_system_info()

    if args.format == "json":
        output = json.dumps(info, ensure_ascii=False, indent=2)
    else:
        output = format_text(info)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"系统信息已保存到: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
