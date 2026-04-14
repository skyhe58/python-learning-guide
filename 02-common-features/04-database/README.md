# 数据库操作

> **模块：** 02-常用功能
> **难度：** 进阶
> **前置知识：** Python 基础（01-python-basics）
> **Python 版本：** >= 3.9
> **最后验证日期：** 2025-07-15

## 概念说明

数据库操作是后端开发的核心技能。Python 通过标准库 `sqlite3` 提供对 SQLite 的原生支持，同时通过第三方库（`mysql-connector-python`、`psycopg2`）支持 MySQL 和 PostgreSQL。对于 Java 开发者来说，Python 的数据库操作比 JDBC 简洁得多——不需要加载驱动、不需要处理 `ResultSet` 迭代器，一个 `cursor.execute()` 加 `fetchall()` 就能完成查询。

Python 数据库编程遵循 DB-API 2.0 规范（PEP 249），所有数据库驱动都实现相同的接口：`connect()` 建立连接、`cursor()` 创建游标、`execute()` 执行 SQL、`fetchone()/fetchall()` 获取结果、`commit()/rollback()` 管理事务。这意味着切换数据库时，代码改动极小。

安全方面，**参数化查询**是防止 SQL 注入的关键——永远不要用字符串拼接构造 SQL。Python 使用 `?`（SQLite）或 `%s`（MySQL/PostgreSQL）作为占位符，将参数与 SQL 语句分离。

### 三大数据库对比

| 特性 | SQLite | MySQL | PostgreSQL |
|------|--------|-------|------------|
| 类型 | 嵌入式（文件/内存） | 客户端-服务器 | 客户端-服务器 |
| Python 模块 | `sqlite3`（标准库） | `mysql-connector-python` | `psycopg2` |
| 适用场景 | 开发测试、小型应用、移动端 | Web 应用、中小型项目 | 大型项目、复杂查询、GIS |
| 安装要求 | 无需安装 | 需安装 MySQL Server | 需安装 PostgreSQL Server |
| 占位符语法 | `?` | `%s` | `%s` |
| 事务支持 | 自动开启（需手动 commit） | 支持 | 支持（MVCC） |
| Java 对应 | SQLite JDBC | MySQL Connector/J | PostgreSQL JDBC |

### DB-API 2.0 核心接口

| 操作 | 方法 | 说明 |
|------|------|------|
| 建立连接 | `connect(...)` | 返回 Connection 对象 |
| 创建游标 | `conn.cursor()` | 返回 Cursor 对象 |
| 执行 SQL | `cursor.execute(sql, params)` | 执行单条 SQL |
| 批量执行 | `cursor.executemany(sql, seq)` | 批量执行 SQL |
| 获取一行 | `cursor.fetchone()` | 返回元组或 None |
| 获取所有 | `cursor.fetchall()` | 返回元组列表 |
| 提交事务 | `conn.commit()` | 提交当前事务 |
| 回滚事务 | `conn.rollback()` | 回滚当前事务 |
| 关闭连接 | `conn.close()` | 释放资源 |


## Java 对比

| 特性 | Java (JDBC) | Python (DB-API) |
|------|-------------|-----------------|
| 驱动加载 | `Class.forName("com.mysql.jdbc.Driver")` | 无需手动加载 |
| 连接方式 | `DriverManager.getConnection(url)` | `sqlite3.connect(db)` |
| 执行查询 | `PreparedStatement` + `executeQuery()` | `cursor.execute(sql, params)` |
| 获取结果 | `ResultSet` 逐行迭代 | `fetchall()` 直接获取列表 |
| 参数绑定 | `ps.setString(1, value)` | `cursor.execute(sql, (value,))` |
| 资源管理 | try-with-resources | `with` 语句 |
| ORM | MyBatis / Hibernate | SQLAlchemy / Django ORM |

**Java 写法：**
```java
// Java JDBC：步骤繁琐，需要手动管理资源
import java.sql.*;

try (Connection conn = DriverManager.getConnection(
        "jdbc:sqlite:test.db")) {
    String sql = "SELECT * FROM users WHERE age > ?";
    try (PreparedStatement ps = conn.prepareStatement(sql)) {
        ps.setInt(1, 18);
        try (ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                System.out.println(rs.getString("name"));
            }
        }
    }
} catch (SQLException e) {
    e.printStackTrace();
}
```

**Python 写法：**
```python
import sqlite3

# Python：简洁直观，with 语句自动管理资源
with sqlite3.connect("test.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE age > ?", (18,))
    for row in cursor.fetchall():
        print(row[0])  # name
```

## 实战代码

### 示例：SQLite 完整演示

**文件：** `examples/sqlite_demo.py`

演示 SQLite 数据库的完整操作流程：连接（内存数据库）、建表、CRUD 操作、参数化查询、事务处理、错误处理。使用 `:memory:` 内存数据库，无需额外安装，可直接运行。

**运行方式：**
```bash
python examples/sqlite_demo.py
```

**预期输出：**
```
========== 建表与插入 ==========
插入成功，最后插入的 ID: 3
所有用户:
  (1, '张三', 28, 'zhangsan@example.com')
  (2, '李四', 35, 'lisi@example.com')
  (3, '王五', 22, 'wangwu@example.com')

========== 参数化查询 ==========
年龄大于 25 的用户:
  张三 (28岁)
  李四 (35岁)
按邮箱查找: ('李四', 35)

========== 更新与删除 ==========
更新后: ('张三', 30, 'zhangsan_new@example.com')
删除后剩余用户数: 2

========== 批量插入 ==========
批量插入后总用户数: 5

========== 事务处理 ==========
事务回滚成功，用户数未变: 5

========== 聚合查询 ==========
用户统计: 总数=5, 平均年龄=29.60, 最大年龄=35, 最小年龄=22

========== Row Factory ==========
使用 Row 对象访问:
  name=李四, email=lisi@example.com
```

### 数据库初始化脚本

**文件：** `init_db.sql`

提供标准的数据库初始化 SQL 脚本，包含建表语句和示例数据，可用于 SQLite/MySQL/PostgreSQL。

## 常见陷阱

### 1. 字符串拼接导致 SQL 注入

这是最严重的安全问题，Java 开发者在 Python 中同样需要警惕。

```python
# ✗ 危险：字符串拼接，存在 SQL 注入风险！
name = "'; DROP TABLE users; --"
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")

# ✓ 安全：参数化查询
cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
```

### 2. 忘记 commit 导致数据丢失

SQLite 默认开启事务，INSERT/UPDATE/DELETE 后必须 `commit()`。

```python
# ✗ 数据不会持久化！
cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (1, "Alice", 25))
conn.close()  # 数据丢失！

# ✓ 使用 with 语句自动 commit
with sqlite3.connect("test.db") as conn:
    conn.execute("INSERT INTO users VALUES (?, ?, ?)", (1, "Alice", 25))
    # with 块结束时自动 commit（无异常时）
```

### 3. 单元素元组的逗号

参数化查询传入单个参数时，必须使用 `(value,)` 而非 `(value)`。

```python
# ✗ 错误：(name) 不是元组，只是加了括号的字符串
cursor.execute("SELECT * FROM users WHERE name = ?", (name))

# ✓ 正确：(name,) 才是单元素元组
cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
```

### 4. 连接未关闭导致资源泄漏

```python
# ✗ 不推荐：手动管理连接容易忘记关闭
conn = sqlite3.connect("test.db")
cursor = conn.cursor()
# ... 操作 ...
conn.close()  # 如果中间抛异常，这行不会执行

# ✓ 推荐：使用 with 语句（上下文管理器）
with sqlite3.connect("test.db") as conn:
    cursor = conn.cursor()
    # ... 操作 ...
    # 自动关闭连接
```

> 💻 **完整可运行代码：** [sqlite_demo.py](examples/sqlite_demo.py) | [init_db.sql](init_db.sql)

## 参考资料

- [Python 官方文档 - sqlite3](https://docs.python.org/zh-cn/3/library/sqlite3.html)
- [PEP 249 - DB-API 2.0 规范](https://peps.python.org/pep-0249/)
- [mysql-connector-python 文档](https://dev.mysql.com/doc/connector-python/en/)
- [psycopg2 文档](https://www.psycopg.org/docs/)
- [Real Python - SQLite in Python](https://realpython.com/python-sqlite-sqlalchemy/)
