#!/usr/bin/env python3
"""
Python 文件操作完整演示

模块: 01-Python 基础
知识点: 文件操作
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python file_ops_demo.py

描述:
    演示 Python 文件操作的核心知识：
    1. 文件读写（open/read/write）
    2. with 语句自动管理资源
    3. pathlib 路径操作
    4. os.walk 目录遍历
    5. CSV/JSON 文件读写
    6. 错误处理（FileNotFoundError 等）
    每个部分都在注释中与 Java 进行对比。
"""

import os
import csv
import json
from pathlib import Path


# ============================================================
# 1. 文件读写基础
# ============================================================

def demo_file_rw():
    """文件读写基础"""
    print("=" * 10, "文件读写基础", "=" * 10)

    # Java:
    #   // 传统方式：层层包装
    #   BufferedReader reader = new BufferedReader(
    #       new InputStreamReader(new FileInputStream("f.txt"), "UTF-8"));
    #   // NIO 方式（Java 11+）
    #   String content = Files.readString(Path.of("f.txt"));
    #
    # Python: 一个 open() 搞定

    test_file = "demo_output.txt"

    # --- 写入文件 ---
    print("--- 写入文件 ---")
    # 模式: "w" = 写入（覆盖），"a" = 追加，"x" = 排他创建
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("Python 文件操作演示\n")
        f.write("第1行: 这是测试内容\n")
        f.write("第2行: Hello, World!\n")
        f.write("第3行: 你好，世界！\n")
    print(f"文件写入成功: {test_file}")

    # --- 读取文件（三种方式）---
    print("--- 读取文件（三种方式）---")

    # 方式 1: read() — 一次性读取全部内容
    with open(test_file, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"read(): {content[:30]}...")

    # 方式 2: readline() — 逐行读取
    with open(test_file, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()
    print(f"readline(): {first_line}")

    # 方式 3: readlines() — 读取所有行到列表
    with open(test_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    print(f"readlines(): {lines[:2]}...")

    # --- 逐行迭代（最推荐，内存友好）---
    print("--- 逐行迭代（内存友好）---")
    # 类似 Java: while ((line = reader.readLine()) != null)
    # 但 Python 的 for 循环更简洁
    with open(test_file, "r", encoding="utf-8") as f:
        for line in f:  # 文件对象本身就是迭代器
            print(f"> {line.strip()}")

    # --- 追加写入 ---
    print("--- 追加写入 ---")
    with open(test_file, "a", encoding="utf-8") as f:
        f.write("第4行: 追加的内容\n")
    print("追加写入成功")

    print()


# ============================================================
# 2. pathlib 路径操作
# ============================================================

def demo_pathlib():
    """pathlib 路径操作"""
    print("=" * 10, "pathlib 路径操作", "=" * 10)

    # Java:
    #   Path path = Path.of("src", "main", "App.java");
    #   path.getFileName();    // App.java
    #   path.getParent();      // src/main
    #   Files.exists(path);    // true/false
    #
    # Python pathlib: 更直观的面向对象 API

    # --- 路径基本操作 ---
    print("--- 路径基本操作 ---")
    current = Path(__file__).resolve()
    print(f"当前文件: {current}")
    print(f"文件名: {current.name}")          # Java: path.getFileName()
    print(f"父目录: {current.parent}")        # Java: path.getParent()
    print(f"扩展名: {current.suffix}")        # Java 没有内置方法！
    print(f"无扩展名: {current.stem}")        # file_ops_demo

    # --- 路径拼接（/ 运算符）---
    print("--- 路径拼接（/ 运算符）---")
    # Java: Path.of("data", "output").resolve("result.csv")
    # Python: 用 / 运算符，更直观
    output_path = Path("data") / "output" / "result.csv"
    print(f"拼接结果: {output_path}")

    # --- 文件查找 ---
    print("--- 文件查找 ---")
    # Java: Files.walk(path).filter(p -> p.toString().endsWith(".py"))
    # Python: Path.glob() 或 Path.rglob()（递归）
    current_dir = Path(".")
    py_files = list(current_dir.glob("*.py"))
    print(f"当前目录下的 .py 文件: {[f.name for f in py_files]}")

    print()


# ============================================================
# 3. os.walk 目录遍历
# ============================================================

def demo_os_walk():
    """os.walk 目录遍历"""
    print("=" * 10, "os.walk 目录遍历", "=" * 10)

    # Java:
    #   Files.walk(Path.of("."))
    #       .forEach(p -> System.out.println(p));
    #
    # Python: os.walk() 返回 (目录路径, 子目录列表, 文件列表) 三元组

    # 只遍历当前目录（不递归深入）
    for dirpath, dirnames, filenames in os.walk("."):
        print(f"目录: {dirpath}")
        if dirnames:
            print(f"  子目录: {dirnames[:5]}{'...' if len(dirnames) > 5 else ''}")
        if filenames:
            print(f"  文件: {filenames[:5]}{'...' if len(filenames) > 5 else ''}")
        break  # 只看第一层

    print()


# ============================================================
# 4. CSV 文件读写
# ============================================================

def demo_csv():
    """CSV 文件读写"""
    print("=" * 10, "CSV 文件读写", "=" * 10)

    # Java:
    #   // 需要第三方库：Apache Commons CSV 或 OpenCSV
    #   CSVParser parser = CSVFormat.DEFAULT.parse(reader);
    #   for (CSVRecord record : parser) { ... }
    #
    # Python: 标准库自带 csv 模块，无需第三方库

    csv_file = "demo_data.csv"

    # --- 写入 CSV ---
    print("--- 写入 CSV ---")
    data = [
        ["姓名", "年龄", "语言"],
        ["张三", "25", "Python"],
        ["李四", "30", "Java"],
        ["王五", "28", "Go"],
    ]
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data)  # 一次写入多行
    print(f"CSV 写入成功: {csv_file}")

    # --- 读取 CSV ---
    print("--- 读取 CSV ---")
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  # 跳过表头
        for row in reader:
            print(f"{row[0]}, {row[1]}, {row[2]}")

    # --- DictReader/DictWriter（更方便）---
    # 类似 Java 中用 Map 表示每一行
    with open(csv_file, "r", encoding="utf-8") as f:
        dict_reader = csv.DictReader(f)
        # 每行是一个字典：{"姓名": "张三", "年龄": "25", "语言": "Python"}

    print()


# ============================================================
# 5. JSON 文件读写
# ============================================================

def demo_json():
    """JSON 文件读写"""
    print("=" * 10, "JSON 文件读写", "=" * 10)

    # Java:
    #   // 需要第三方库：Jackson 或 Gson
    #   ObjectMapper mapper = new ObjectMapper();
    #   MyClass obj = mapper.readValue(jsonStr, MyClass.class);
    #   String json = mapper.writeValueAsString(obj);
    #
    # Python: 标准库自带 json 模块

    json_file = "demo_data.json"

    # --- 写入 JSON ---
    print("--- 写入 JSON ---")
    data = {
        "name": "张三",
        "age": 25,
        "skills": ["Python", "Java"],
        "address": {"city": "北京", "district": "海淀区"},
    }
    with open(json_file, "w", encoding="utf-8") as f:
        # ensure_ascii=False 保留中文，indent=2 格式化
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"JSON 写入成功: {json_file}")

    # --- 读取 JSON ---
    print("--- 读取 JSON ---")
    with open(json_file, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    print(f"姓名: {loaded['name']}, 技能: {loaded['skills']}")

    # --- 字符串与 JSON 互转 ---
    # json.dumps() — Python 对象 → JSON 字符串
    # json.loads() — JSON 字符串 → Python 对象
    json_str = json.dumps(data, ensure_ascii=False)
    parsed = json.loads(json_str)
    assert parsed == data  # 往返一致性

    print()


# ============================================================
# 6. 错误处理
# ============================================================

def demo_error_handling():
    """文件操作错误处理"""
    print("=" * 10, "错误处理", "=" * 10)

    # Java:
    #   try { ... }
    #   catch (FileNotFoundException e) { ... }
    #   catch (IOException e) { ... }
    #
    # Python: 对应的异常类型不同，但模式类似

    # --- FileNotFoundError ---
    print("--- FileNotFoundError ---")
    try:
        with open("不存在的文件.txt", "r") as f:
            content = f.read()
    except FileNotFoundError as e:
        # 类似 Java: FileNotFoundException
        print(f"文件不存在: {e}")

    # --- PermissionError ---
    print("--- PermissionError ---")
    print("（跳过权限测试）")
    # try:
    #     with open("/root/secret.txt", "r") as f:
    #         content = f.read()
    # except PermissionError as e:
    #     print(f"权限不足: {e}")

    # --- 编码错误处理 ---
    print("--- 编码错误处理 ---")
    # errors 参数：'strict'(默认,抛异常), 'replace'(替换), 'ignore'(忽略)
    print("使用 errors='replace' 处理编码错误")
    # with open("binary_file", "r", encoding="utf-8", errors="replace") as f:
    #     content = f.read()  # 无法解码的字节替换为 ?

    print()


# ============================================================
# 7. 清理临时文件
# ============================================================

def cleanup():
    """清理演示过程中创建的临时文件"""
    print("=" * 10, "清理临时文件", "=" * 10)
    temp_files = ["demo_output.txt", "demo_data.csv", "demo_data.json"]
    for f in temp_files:
        try:
            os.remove(f)
        except FileNotFoundError:
            pass
    print("临时文件已清理")


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数：依次演示所有文件操作知识点"""
    demo_file_rw()
    demo_pathlib()
    demo_os_walk()
    demo_csv()
    demo_json()
    demo_error_handling()
    cleanup()


if __name__ == "__main__":
    main()
