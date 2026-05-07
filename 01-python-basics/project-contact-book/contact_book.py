#!/usr/bin/env python3
"""
命令行通讯录工具

模块: 01-python-basics / project-contact-book
知识点: 综合练习（数据类型、OOP、文件操作、异常处理、函数与装饰器、命令行交互）
Python 版本: >= 3.9
最后验证: 2025-07-14

运行方式:
    python contact_book.py

描述:
    一个基于命令行的通讯录管理工具，整合 Python 基础模块的所有核心知识点。
    支持添加、查看、搜索、删除联系人，并通过 JSON 文件实现数据持久化。
"""

import json
import os
import functools
from dataclasses import dataclass, field, asdict
from typing import Optional


# ============================================================
# 装饰器：功能模块化（知识点：04-functions-decorators）
# ============================================================

def log_operation(func):
    """操作日志装饰器，记录每次操作的执行情况。"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\n--- 执行操作: {func.__doc__ or func.__name__} ---")
        result = func(*args, **kwargs)
        return result
    return wrapper


# ============================================================
# 数据类：Contact（知识点：05-oop, @dataclass）
# ============================================================

@dataclass
class Contact:
    """联系人数据类。

    使用 @dataclass 自动生成 __init__、__repr__、__eq__ 等方法。
    """
    name: str
    phone: str
    email: str = ""

    def to_dict(self) -> dict:
        """将联系人转换为字典（用于 JSON 序列化）。"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Contact":
        """从字典创建联系人实例。"""
        return cls(
            name=data.get("name", ""),
            phone=data.get("phone", ""),
            email=data.get("email", ""),
        )


# ============================================================
# 通讯录类：ContactBook（知识点：05-oop, 02-data-types）
# ============================================================

class ContactBook:
    """通讯录管理类。

    使用 list 存储联系人，提供增删查功能，
    支持 JSON 文件持久化。
    """

    DEFAULT_FILE = "contacts.json"

    def __init__(self, filepath: Optional[str] = None):
        """初始化通讯录。

        Args:
            filepath: 数据文件路径，默认为当前目录下的 contacts.json
        """
        self._contacts: list[Contact] = []
        self._filepath = filepath or self.DEFAULT_FILE

    @property
    def contacts(self) -> list[Contact]:
        """获取所有联系人列表（只读属性）。"""
        return list(self._contacts)

    @property
    def filepath(self) -> str:
        """获取数据文件路径。"""
        return self._filepath

    def add(self, contact: Contact) -> bool:
        """添加联系人。

        Args:
            contact: 要添加的联系人

        Returns:
            添加成功返回 True，姓名重复返回 False
        """
        # 检查是否已存在同名联系人
        if any(c.name == contact.name for c in self._contacts):
            return False
        self._contacts.append(contact)
        return True

    def search(self, keyword: str) -> list[Contact]:
        """按姓名关键字搜索联系人（知识点：09-comprehensions-generators）。

        Args:
            keyword: 搜索关键字（模糊匹配）

        Returns:
            匹配的联系人列表
        """
        # 使用列表推导式进行模糊搜索
        return [c for c in self._contacts if keyword.lower() in c.name.lower()]

    def delete(self, name: str) -> bool:
        """按姓名删除联系人。

        Args:
            name: 要删除的联系人姓名

        Returns:
            删除成功返回 True，未找到返回 False
        """
        for i, contact in enumerate(self._contacts):
            if contact.name == name:
                self._contacts.pop(i)
                return True
        return False

    def save(self, filepath: Optional[str] = None) -> None:
        """保存通讯录到 JSON 文件（知识点：08-file-operations）。

        Args:
            filepath: 保存路径，默认使用初始化时的路径

        Raises:
            IOError: 文件写入失败时抛出
        """
        target = filepath or self._filepath
        data = [c.to_dict() for c in self._contacts]
        try:
            with open(target, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            raise IOError(f"保存文件失败: {target}") from e

    def load(self, filepath: Optional[str] = None) -> int:
        """从 JSON 文件加载通讯录（知识点：07-exception-handling）。

        Args:
            filepath: 文件路径，默认使用初始化时的路径

        Returns:
            加载的联系人数量

        Raises:
            FileNotFoundError: 文件不存在时抛出
            json.JSONDecodeError: JSON 格式错误时抛出
        """
        target = filepath or self._filepath
        if not os.path.exists(target):
            raise FileNotFoundError(f"文件不存在: {target}")

        try:
            with open(target, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"JSON 格式错误: {target}", e.doc, e.pos
            ) from e

        self._contacts = [Contact.from_dict(item) for item in data]
        return len(self._contacts)

    def __len__(self) -> int:
        """返回联系人数量。"""
        return len(self._contacts)

    def __repr__(self) -> str:
        return f"ContactBook(count={len(self._contacts)}, file='{self._filepath}')"


# ============================================================
# 命令行交互界面（知识点：03-control-flow）
# ============================================================

MENU = """
========== 命令行通讯录 ==========
1. 添加联系人
2. 查看所有联系人
3. 搜索联系人
4. 删除联系人
5. 保存并退出
=================================="""


def print_contacts(contacts: list[Contact]) -> None:
    """以表格形式打印联系人列表。"""
    if not contacts:
        print("📭 通讯录为空")
        return

    # 计算列宽
    name_width = max(len(c.name) for c in contacts)
    phone_width = max(len(c.phone) for c in contacts)
    email_width = max(len(c.email) for c in contacts)
    name_width = max(name_width, 4)   # 最小宽度：表头
    phone_width = max(phone_width, 4)
    email_width = max(email_width, 4)

    # 打印表格
    separator = f"+{'-' * (name_width + 2)}+{'-' * (phone_width + 2)}+{'-' * (email_width + 2)}+"
    header = f"| {'姓名'.ljust(name_width)} | {'电话'.ljust(phone_width)} | {'邮箱'.ljust(email_width)} |"
    print(separator)
    print(header)
    print(separator)
    for c in contacts:
        row = f"| {c.name.ljust(name_width)} | {c.phone.ljust(phone_width)} | {c.email.ljust(email_width)} |"
        print(row)
    print(separator)
    print(f"共 {len(contacts)} 位联系人")


@log_operation
def handle_add(book: ContactBook) -> None:
    """添加联系人"""
    name = input("请输入姓名: ").strip()
    if not name:
        print("❌ 姓名不能为空")
        return

    phone = input("请输入电话: ").strip()
    email = input("请输入邮箱 (可选，直接回车跳过): ").strip()

    contact = Contact(name=name, phone=phone, email=email)
    if book.add(contact):
        print(f"✅ 联系人 '{name}' 已添加")
    else:
        print(f"❌ 联系人 '{name}' 已存在")


@log_operation
def handle_list(book: ContactBook) -> None:
    """查看所有联系人"""
    print_contacts(book.contacts)


@log_operation
def handle_search(book: ContactBook) -> None:
    """搜索联系人"""
    keyword = input("请输入搜索关键字: ").strip()
    if not keyword:
        print("❌ 关键字不能为空")
        return

    results = book.search(keyword)
    if results:
        print(f"找到 {len(results)} 个匹配结果：")
        print_contacts(results)
    else:
        print(f"❌ 未找到包含 '{keyword}' 的联系人")


@log_operation
def handle_delete(book: ContactBook) -> None:
    """删除联系人"""
    name = input("请输入要删除的联系人姓名: ").strip()
    if not name:
        print("❌ 姓名不能为空")
        return

    if book.delete(name):
        print(f"✅ 联系人 '{name}' 已删除")
    else:
        print(f"❌ 未找到联系人 '{name}'")


def main():
    """通讯录主程序入口。"""
    book = ContactBook()

    # 启动时尝试加载已有数据（知识点：07-exception-handling）
    try:
        count = book.load()
        print(f"📂 已从 {book.filepath} 加载 {count} 位联系人")
    except FileNotFoundError:
        print("📝 未找到已有数据，将创建新通讯录")
    except json.JSONDecodeError:
        print("⚠️ 数据文件格式错误，将创建新通讯录")

    # 操作映射表（知识点：02-data-types, dict）
    actions = {
        "1": handle_add,
        "2": handle_list,
        "3": handle_search,
        "4": handle_delete,
    }

    # 主循环（知识点：03-control-flow）
    while True:
        print(MENU)
        choice = input("请选择操作 (1-5): ").strip()

        if choice == "5":
            try:
                book.save()
                print(f"💾 数据已保存到 {book.filepath}")
            except IOError as e:
                print(f"⚠️ 保存失败: {e}")
            print("👋 再见！")
            break

        action = actions.get(choice)
        if action:
            action(book)
        else:
            print("❌ 无效选择，请输入 1-5")


if __name__ == "__main__":
    main()
