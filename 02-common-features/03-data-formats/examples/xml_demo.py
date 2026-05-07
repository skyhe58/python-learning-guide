#!/usr/bin/env python3
"""
XML 数据处理演示

模块: 02-常用功能
知识点: 数据格式处理
Python 版本: >= 3.9
最后验证: 2025-07-15

运行方式:
    python xml_demo.py

描述:
    演示 xml.etree.ElementTree 模块的核心功能：
    1. XML 解析（fromstring / parse）
    2. XML 生成（Element / SubElement / tostring）
    3. XPath 查询
    4. 属性操作
    5. XML 文件读写
"""

import xml.etree.ElementTree as ET
import tempfile
import os


# ============================================================
# 1. XML 解析
# ============================================================

def demo_parse():
    """解析 XML 字符串和遍历元素"""
    print("=" * 10, "XML 解析", "=" * 10)

    xml_text = """<?xml version="1.0" encoding="UTF-8"?>
<bookstore>
    <book category="编程" lang="zh">
        <title>Python 入门</title>
        <author>张三</author>
        <price>59.90</price>
        <year>2025</year>
    </book>
    <book category="编程" lang="en">
        <title>Fluent Python</title>
        <author>Luciano Ramalho</author>
        <price>89.00</price>
        <year>2022</year>
    </book>
    <book category="文学" lang="zh">
        <title>三体</title>
        <author>刘慈欣</author>
        <price>45.00</price>
        <year>2008</year>
    </book>
</bookstore>"""

    # 解析 XML 字符串
    # 类似 Java: DocumentBuilder.parse() 或 SAXParser
    root = ET.fromstring(xml_text)
    print(f"根元素: {root.tag}")
    print(f"子元素数量: {len(root)}")

    # 遍历子元素
    print("\n所有书籍:")
    for book in root:
        title = book.find("title").text
        author = book.find("author").text
        price = book.find("price").text
        category = book.get("category")  # 获取属性
        print(f"  [{category}] {title} - {author} ¥{price}")

    print()
    return root


# ============================================================
# 2. XPath 查询
# ============================================================

def demo_xpath(root):
    """使用 XPath 查询 XML 元素"""
    print("=" * 10, "XPath 查询", "=" * 10)

    # find：查找第一个匹配
    first_book = root.find("book")
    print(f"第一本书: {first_book.find('title').text}")

    # findall：查找所有匹配
    all_titles = root.findall("book/title")
    print(f"所有书名: {[t.text for t in all_titles]}")

    # 带条件的 XPath 查询
    # 查找 category="编程" 的书
    programming_books = root.findall("book[@category='编程']")
    print(f"编程类书籍: {[b.find('title').text for b in programming_books]}")

    # 查找价格大于 50 的书（XPath 不支持数值比较，需手动过滤）
    expensive = [
        book.find("title").text
        for book in root.findall("book")
        if float(book.find("price").text) > 50
    ]
    print(f"价格>50的书: {expensive}")

    # 查找中文书籍
    zh_books = root.findall("book[@lang='zh']")
    print(f"中文书籍: {[b.find('title').text for b in zh_books]}")

    print()


# ============================================================
# 3. XML 生成
# ============================================================

def demo_generate():
    """使用 Element 和 SubElement 生成 XML"""
    print("=" * 10, "XML 生成", "=" * 10)

    # 创建根元素
    # 类似 Java: Document doc = builder.newDocument();
    root = ET.Element("config")
    root.set("version", "1.0")

    # 添加子元素
    # 类似 Java: Element child = doc.createElement("server");
    server = ET.SubElement(root, "server")

    host = ET.SubElement(server, "host")
    host.text = "localhost"

    port = ET.SubElement(server, "port")
    port.text = "8080"

    # 添加数据库配置
    database = ET.SubElement(root, "database")
    database.set("type", "postgresql")

    db_host = ET.SubElement(database, "host")
    db_host.text = "localhost"

    db_port = ET.SubElement(database, "port")
    db_port.text = "5432"

    db_name = ET.SubElement(database, "name")
    db_name.text = "mydb"

    # 转为字符串
    xml_str = ET.tostring(root, encoding="unicode", xml_declaration=True)
    print(f"生成的 XML:\n{xml_str}")

    # 格式化输出（Python 3.9+）
    ET.indent(root, space="  ")
    pretty_xml = ET.tostring(root, encoding="unicode", xml_declaration=True)
    print(f"\n格式化 XML:\n{pretty_xml}")

    print()
    return root


# ============================================================
# 4. 属性操作
# ============================================================

def demo_attributes():
    """XML 元素属性的读取、设置和删除"""
    print("=" * 10, "属性操作", "=" * 10)

    xml_text = '<user id="1" name="Alice" role="admin" active="true"/>'
    elem = ET.fromstring(xml_text)

    # 读取属性
    print(f"id: {elem.get('id')}")
    print(f"name: {elem.get('name')}")
    print(f"所有属性: {elem.attrib}")

    # 设置属性
    elem.set("email", "alice@example.com")
    print(f"添加属性后: {elem.attrib}")

    # 删除属性
    del elem.attrib["active"]
    print(f"删除属性后: {elem.attrib}")

    # 带默认值的属性读取
    phone = elem.get("phone", "未设置")
    print(f"phone (默认值): {phone}")

    print()


# ============================================================
# 5. XML 文件读写
# ============================================================

def demo_file_io():
    """XML 文件的读取和写入"""
    print("=" * 10, "XML 文件读写", "=" * 10)

    # 构建 XML 树
    root = ET.Element("employees")
    employees = [
        {"name": "张三", "dept": "技术部", "salary": "15000"},
        {"name": "李四", "dept": "产品部", "salary": "12000"},
        {"name": "王五", "dept": "技术部", "salary": "18000"},
    ]
    for emp in employees:
        elem = ET.SubElement(root, "employee")
        for key, value in emp.items():
            child = ET.SubElement(elem, key)
            child.text = value

    ET.indent(root, space="  ")

    # 写入文件
    tmp_file = os.path.join(tempfile.gettempdir(), "demo_employees.xml")
    tree = ET.ElementTree(root)
    tree.write(tmp_file, encoding="unicode", xml_declaration=True)
    print(f"写入文件: {tmp_file}")

    # 读取文件
    loaded_tree = ET.parse(tmp_file)
    loaded_root = loaded_tree.getroot()
    print(f"读取到 {len(loaded_root)} 名员工:")
    for emp in loaded_root:
        name = emp.find("name").text
        dept = emp.find("dept").text
        print(f"  {name} - {dept}")

    # 清理临时文件
    os.remove(tmp_file)

    print()


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数：依次演示所有 XML 处理知识点"""
    root = demo_parse()
    demo_xpath(root)
    demo_generate()
    demo_attributes()
    demo_file_io()


if __name__ == "__main__":
    main()
