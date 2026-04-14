# 综合练习项目：命令行通讯录

> **模块：** 01-python-basics
> **难度：** 入门
> **前置知识：** 本模块所有知识点（01~09）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-14

## 项目简介

这是一个整合 Python 基础模块所有知识点的综合练习项目。通过实现一个命令行通讯录工具，将数据类型、面向对象编程、文件操作、异常处理、函数与装饰器、命令行交互等知识点融会贯通。

完成本项目后，说明你已掌握 Python 基础，可以进入第二阶段的学习。

## 涉及知识点

| 知识点 | 在项目中的应用 | 对应章节 |
|--------|---------------|----------|
| 数据类型（dict/list） | 存储和管理联系人数据 | [02-data-types](../02-data-types/) |
| 控制流 | 菜单循环、条件分支 | [03-control-flow](../03-control-flow/) |
| 函数与装饰器 | 功能模块化、日志装饰器 | [04-functions-decorators](../04-functions-decorators/) |
| 类与面向对象 | Contact 类（@dataclass）、ContactBook 类 | [05-oop](../05-oop/) |
| 模块与包管理 | 标准库 json/os/dataclasses 的使用 | [06-modules-packages](../06-modules-packages/) |
| 异常处理 | 文件不存在、输入错误、JSON 解析异常 | [07-exception-handling](../07-exception-handling/) |
| 文件操作 | JSON 文件持久化存储 | [08-file-operations](../08-file-operations/) |
| 列表推导式 | 联系人搜索过滤 | [09-comprehensions-generators](../09-comprehensions-generators/) |

## 功能列表

1. **添加联系人** — 输入姓名、电话、邮箱，创建新联系人
2. **查看所有联系人** — 以表格形式展示通讯录
3. **搜索联系人** — 按姓名关键字模糊搜索
4. **删除联系人** — 按姓名删除指定联系人
5. **保存到文件** — 将通讯录数据持久化为 JSON 文件
6. **从文件加载** — 启动时自动加载已保存的数据

## 运行方式

```bash
python contact_book.py
```

运行后会显示交互菜单：

```
========== 命令行通讯录 ==========
1. 添加联系人
2. 查看所有联系人
3. 搜索联系人
4. 删除联系人
5. 保存并退出
==================================
请选择操作 (1-5):
```

## 项目结构

```
project-contact-book/
├── README.md               # 项目说明（本文件）
├── contact_book.py         # 通讯录主程序
└── test_contact_book.py    # 单元测试
```

## 运行测试

```bash
pytest test_contact_book.py -v
```

## 预期输出示例

```
请选择操作 (1-5): 1
请输入姓名: 张三
请输入电话: 13800138000
请输入邮箱: zhangsan@example.com
✅ 联系人 '张三' 已添加

请选择操作 (1-5): 2
+------+-------------+----------------------+
| 姓名 | 电话        | 邮箱                 |
+------+-------------+----------------------+
| 张三 | 13800138000 | zhangsan@example.com |
+------+-------------+----------------------+
共 1 位联系人
```

> 💻 **完整可运行代码：** [contact_book.py](contact_book.py) | [test_contact_book.py](test_contact_book.py)
