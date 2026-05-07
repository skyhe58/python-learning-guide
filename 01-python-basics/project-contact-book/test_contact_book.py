#!/usr/bin/env python3
"""
命令行通讯录 — 单元测试

模块: 01-python-basics / project-contact-book
知识点: 综合练习项目测试
Python 版本: >= 3.9
最后验证: 2025-07-14

运行方式:
    pytest test_contact_book.py -v

描述:
    使用 pytest 测试 Contact 和 ContactBook 类的核心功能，
    包括添加、搜索、删除、保存/加载等操作。
"""

import json
import os
import tempfile

import pytest

from contact_book import Contact, ContactBook


# ============================================================
# Contact 类测试
# ============================================================

class TestContact:
    """测试 Contact 数据类。"""

    def test_create_contact(self):
        """测试创建联系人。"""
        c = Contact(name="张三", phone="13800138000", email="zhangsan@example.com")
        assert c.name == "张三"
        assert c.phone == "13800138000"
        assert c.email == "zhangsan@example.com"

    def test_default_email(self):
        """测试邮箱默认值为空字符串。"""
        c = Contact(name="李四", phone="13900139000")
        assert c.email == ""

    def test_to_dict(self):
        """测试联系人转字典。"""
        c = Contact(name="王五", phone="13700137000", email="wangwu@test.com")
        d = c.to_dict()
        assert d == {"name": "王五", "phone": "13700137000", "email": "wangwu@test.com"}

    def test_from_dict(self):
        """测试从字典创建联系人。"""
        data = {"name": "赵六", "phone": "13600136000", "email": "zhaoliu@test.com"}
        c = Contact.from_dict(data)
        assert c.name == "赵六"
        assert c.phone == "13600136000"
        assert c.email == "zhaoliu@test.com"

    def test_from_dict_missing_email(self):
        """测试从缺少邮箱的字典创建联系人。"""
        data = {"name": "孙七", "phone": "13500135000"}
        c = Contact.from_dict(data)
        assert c.email == ""

    def test_equality(self):
        """测试 dataclass 自动生成的 __eq__。"""
        c1 = Contact(name="张三", phone="123")
        c2 = Contact(name="张三", phone="123")
        assert c1 == c2


# ============================================================
# ContactBook 类测试
# ============================================================

class TestContactBook:
    """测试 ContactBook 通讯录管理类。"""

    @pytest.fixture
    def book(self, tmp_path):
        """创建一个使用临时文件的通讯录实例。"""
        filepath = str(tmp_path / "test_contacts.json")
        return ContactBook(filepath=filepath)

    @pytest.fixture
    def sample_contacts(self):
        """提供示例联系人数据。"""
        return [
            Contact(name="张三", phone="13800138000", email="zhangsan@example.com"),
            Contact(name="李四", phone="13900139000", email="lisi@example.com"),
            Contact(name="王五", phone="13700137000"),
        ]

    # --- 添加功能 ---

    def test_add_contact(self, book, sample_contacts):
        """测试添加联系人。"""
        assert book.add(sample_contacts[0]) is True
        assert len(book) == 1

    def test_add_duplicate_name(self, book, sample_contacts):
        """测试添加重名联系人应失败。"""
        book.add(sample_contacts[0])
        duplicate = Contact(name="张三", phone="99999999")
        assert book.add(duplicate) is False
        assert len(book) == 1

    def test_add_multiple(self, book, sample_contacts):
        """测试添加多个联系人。"""
        for c in sample_contacts:
            book.add(c)
        assert len(book) == 3

    # --- 搜索功能 ---

    def test_search_found(self, book, sample_contacts):
        """测试搜索存在的联系人。"""
        for c in sample_contacts:
            book.add(c)
        results = book.search("张")
        assert len(results) == 1
        assert results[0].name == "张三"

    def test_search_case_insensitive(self, book):
        """测试搜索不区分大小写。"""
        book.add(Contact(name="Alice", phone="123"))
        book.add(Contact(name="Bob", phone="456"))
        results = book.search("alice")
        assert len(results) == 1
        assert results[0].name == "Alice"

    def test_search_not_found(self, book, sample_contacts):
        """测试搜索不存在的联系人。"""
        for c in sample_contacts:
            book.add(c)
        results = book.search("不存在")
        assert len(results) == 0

    def test_search_multiple_results(self, book):
        """测试搜索返回多个结果。"""
        book.add(Contact(name="张三", phone="111"))
        book.add(Contact(name="张四", phone="222"))
        book.add(Contact(name="李五", phone="333"))
        results = book.search("张")
        assert len(results) == 2

    # --- 删除功能 ---

    def test_delete_existing(self, book, sample_contacts):
        """测试删除存在的联系人。"""
        for c in sample_contacts:
            book.add(c)
        assert book.delete("李四") is True
        assert len(book) == 2

    def test_delete_nonexistent(self, book, sample_contacts):
        """测试删除不存在的联系人。"""
        for c in sample_contacts:
            book.add(c)
        assert book.delete("不存在") is False
        assert len(book) == 3

    # --- 保存/加载功能 ---

    def test_save_and_load(self, book, sample_contacts):
        """测试保存后重新加载数据一致。"""
        for c in sample_contacts:
            book.add(c)
        book.save()

        # 创建新实例加载数据
        new_book = ContactBook(filepath=book.filepath)
        count = new_book.load()
        assert count == 3
        assert len(new_book) == 3
        assert new_book.contacts[0].name == "张三"

    def test_save_empty_book(self, book):
        """测试保存空通讯录。"""
        book.save()
        new_book = ContactBook(filepath=book.filepath)
        count = new_book.load()
        assert count == 0

    def test_load_nonexistent_file(self, tmp_path):
        """测试加载不存在的文件应抛出异常。"""
        book = ContactBook(filepath=str(tmp_path / "nonexistent.json"))
        with pytest.raises(FileNotFoundError):
            book.load()

    def test_load_invalid_json(self, tmp_path):
        """测试加载格式错误的 JSON 文件应抛出异常。"""
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("这不是有效的 JSON", encoding="utf-8")
        book = ContactBook(filepath=str(bad_file))
        with pytest.raises(json.JSONDecodeError):
            book.load()

    # --- 其他 ---

    def test_contacts_property_returns_copy(self, book, sample_contacts):
        """测试 contacts 属性返回副本，修改不影响原数据。"""
        book.add(sample_contacts[0])
        contacts = book.contacts
        contacts.clear()
        assert len(book) == 1  # 原数据不受影响

    def test_repr(self, book):
        """测试 __repr__ 输出。"""
        r = repr(book)
        assert "ContactBook" in r
        assert "count=0" in r
